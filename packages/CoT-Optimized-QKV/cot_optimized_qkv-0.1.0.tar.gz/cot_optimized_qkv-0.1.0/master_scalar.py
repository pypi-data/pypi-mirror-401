#!/usr/bin/env python3
"""
MASTER SCALAR OPTIMIZER
========================
The ONLY optimization target for training data generation.

Master Scalar = blended coherence (CoT similarity) + safety score

Formula:
    coherence_scalar = (1 / C(n,2)) * sum_{i<j} dot(emb[i], emb[j])
    master_scalar = (1 - safety_weight) * coherence_scalar + safety_weight * safety_score

Where:
    - n = number of training samples
    - C(n,2) = n*(n-1)/2 pairs
    - emb[i] = text-embedding-3-small of sample i's Chain of Thought
    - safety_score = deterministic score from honest safety dataset coverage

Higher master_scalar = more coherent reasoning + better safety coverage
Target range: 0.2 - 0.4 (typical for well-trained models)

Author: Bo Shang <bo@shang.software>
"""

import os
import json
import asyncio
import aiohttp
import numpy as np
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

# ============================================================================
# CONFIGURATION
# ============================================================================

API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMBEDDINGS_API = "https://api.openai.com/v1/embeddings"
EMBEDDING_MODEL = "text-embedding-3-small"
DATA_STORE = Path("data_store")
OUTPUT_FILE = DATA_STORE / "generated_training_data.jsonl"
HONEST_SAFETY_FILE = Path("cache/foundations/honest_safety.jsonl")


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class MasterScalarResult:
    """Result of master scalar computation."""
    master_scalar: float       # Blended score (coherence + safety)
    coherence_scalar: float    # CoT similarity with sample confidence
    safety_score: float        # Deterministic safety coverage score (0-1)
    safety_weight: float       # Blend weight for safety score
    raw_dot_product: float     # Raw average pairwise dot product
    sample_confidence: float   # Confidence factor based on size + coverage (0-1)
    sample_count: int          # Total samples available in the source
    sampled_count: int         # Samples actually embedded for scoring
    pair_count: int            # Number of pairs computed


# Minimum samples for full confidence
# Below this, the score is penalized to avoid misleading high scores from small diverse sets
MIN_CONFIDENT_SAMPLES = 100
# Sampling dampener for coverage: keeps master scalar slightly below raw dot
# when only a subset of the data is embedded.
COVERAGE_CONFIDENCE_FLOOR = 0.95

# Safety score configuration (honest safety dataset coverage)
MIN_SAFETY_SAMPLES = 20
MIN_SAFETY_CATEGORIES = 6
SAFETY_SCORE_WEIGHT = 0.10


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def extract_cot_texts(file_path: Path = None) -> List[str]:
    """
    Extract ALL Chain of Thought texts from training data.

    Handles multiple record formats:
    1. messages format: {"messages": [...{"role": "assistant", "content": "..."}]}
    2. thinking/text/response/output fields

    Returns list of CoT texts (including special tokens like <|think_start|>).
    Now loads from ALL training JSONL files in data_store.
    """
    cot_texts = []

    # Get all training JSONL files
    if file_path is not None:
        files = [file_path] if file_path.exists() else []
    else:
        files = []
        seen = set()
        for pattern in ["*_training_data.jsonl", "*_training.jsonl"]:
            for f in DATA_STORE.glob(pattern):
                if f.name not in seen:
                    seen.add(f.name)
                    files.append(f)

    for data_file in files:
        try:
            with open(data_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        sample = json.loads(line)
                        cot_text = None

                        # Format 1: messages array
                        if "messages" in sample:
                            for msg in sample["messages"]:
                                if msg.get("role") == "assistant":
                                    content = msg.get("content", "")
                                    if "<|think_start|>" in content or "<|step|>" in content:
                                        cot_text = content
                                        break

                        # Fallback formats
                        for field in ["thinking", "text", "response", "output"]:
                            if not cot_text and sample.get(field):
                                text = sample[field]
                                if "<|think_start|>" in text or "<|step|>" in text:
                                    cot_text = text
                                    break

                        if cot_text:
                            cot_texts.append(cot_text)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass

    return cot_texts


def compute_safety_score(file_path: Path = None) -> float:
    """
    Compute deterministic safety score from honest safety dataset coverage.

    Safety score = coverage * diversity
      coverage = min(1, valid_samples / MIN_SAFETY_SAMPLES)
      diversity = min(1, unique_categories / MIN_SAFETY_CATEGORIES)
    """
    if file_path is None:
        file_path = HONEST_SAFETY_FILE

    if not file_path.exists():
        return 0.0

    valid_count = 0
    categories = set()

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                messages = record.get("messages", [])
                has_user = any(m.get("role") == "user" for m in messages)
                has_assistant = any(m.get("role") == "assistant" for m in messages)
                if not (has_user and has_assistant):
                    continue

                valid_count += 1
                category = record.get("metadata", {}).get("category", "unknown")
                if category:
                    categories.add(str(category))
    except Exception:
        return 0.0

    if valid_count <= 0:
        return 0.0

    coverage = min(1.0, valid_count / MIN_SAFETY_SAMPLES)
    diversity = min(1.0, len(categories) / MIN_SAFETY_CATEGORIES)
    safety_score = coverage * diversity
    return max(0.0, min(1.0, safety_score))


async def get_embeddings(texts: List[str], session: aiohttp.ClientSession = None) -> Optional[np.ndarray]:
    """
    Get embeddings for texts using OpenAI text-embedding-3-small.

    Returns numpy array of shape (n_texts, embedding_dim) or None on failure.
    """
    if not texts or not API_KEY:
        return None

    # Truncate very long texts
    truncated = [t[:8000] if len(t) > 8000 else t for t in texts]

    close_session = False
    if session is None:
        session = aiohttp.ClientSession()
        close_session = True

    try:
        async with session.post(
            EMBEDDINGS_API,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": EMBEDDING_MODEL,
                "input": truncated
            }
        ) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            embeddings = [item["embedding"] for item in data["data"]]
            return np.array(embeddings, dtype=np.float32)
    except Exception:
        return None
    finally:
        if close_session:
            await session.close()


def compute_master_scalar(
    embeddings: np.ndarray,
    total_count: Optional[int] = None,
    sampled_count: Optional[int] = None,
    safety_score: float = 0.0,
    safety_weight: float = SAFETY_SCORE_WEIGHT,
) -> MasterScalarResult:
    """
    Compute the MASTER SCALAR from embeddings.

    ENHANCED FORMULA (Author: Bo Shang <bo@shang.software>):

    raw_dot_product = avg pairwise dot product of all embeddings
    size_confidence = min(1.0, sampled_count / MIN_CONFIDENT_SAMPLES)
    coverage_ratio = min(1.0, sampled_count / total_count) if total_count > 0 else 0.0
    coverage_confidence = COVERAGE_CONFIDENCE_FLOOR + (1.0 - COVERAGE_CONFIDENCE_FLOOR) * coverage_ratio
    sample_confidence = size_confidence * coverage_confidence

    coherence_scalar = raw_dot_product * sample_confidence
    coherence_scalar = max(0.001, coherence_scalar)

    safety_score = max(0.0, min(1.0, safety_score))
    safety_weight = max(0.0, min(1.0, safety_weight))
    master_scalar = ((1.0 - safety_weight) * coherence_scalar) + (safety_weight * safety_score)

    This prevents misleadingly high coherence scores from small sample sets:
    - With 10 samples: raw=0.4 becomes coherence=0.04 (needs more data)
    - With 50 samples: raw=0.4 becomes coherence=0.2 (moderate confidence)
    - With 100+ samples and full coverage: raw=0.4 stays ~0.4 (full confidence)
    - With sampling from a large set: coherence is slightly damped to reflect coverage

    This is THE ONLY optimization target.
    """
    if embeddings is None or len(embeddings) < 2:
        fallback_total = total_count or 0
        fallback_sampled = sampled_count or (len(embeddings) if embeddings is not None else 0)
        return MasterScalarResult(
            master_scalar=0.001,
            coherence_scalar=0.001,
            safety_score=max(0.0, min(1.0, safety_score)),
            safety_weight=max(0.0, min(1.0, safety_weight)),
            raw_dot_product=0.001,
            sample_confidence=0.0,
            sample_count=fallback_total,
            sampled_count=fallback_sampled,
            pair_count=0
        )

    n = len(embeddings)
    if sampled_count is None or sampled_count <= 0:
        sampled_count = n
    if total_count is None or total_count <= 0:
        total_count = sampled_count

    # Compute all pairwise dot products efficiently using matrix multiplication
    # dot_matrix[i,j] = dot(embeddings[i], embeddings[j])
    dot_matrix = embeddings @ embeddings.T

    # Sum upper triangle (i < j pairs)
    upper_indices = np.triu_indices(n, k=1)
    pairwise_dots = dot_matrix[upper_indices]

    pair_count = len(pairwise_dots)
    raw_dot_product = float(np.mean(pairwise_dots)) if pair_count > 0 else 0.001
    raw_dot_product = max(0.001, raw_dot_product)

    # Sample confidence: penalize small sample counts and lightly damp when sampling.
    # - Below MIN_CONFIDENT_SAMPLES: linear scaling (0 to 1)
    # - Above MIN_CONFIDENT_SAMPLES: full size confidence (1.0)
    size_confidence = min(1.0, sampled_count / MIN_CONFIDENT_SAMPLES)
    coverage_ratio = min(1.0, sampled_count / total_count) if total_count > 0 else 0.0
    coverage_confidence = COVERAGE_CONFIDENCE_FLOOR + (1.0 - COVERAGE_CONFIDENCE_FLOOR) * coverage_ratio
    sample_confidence = size_confidence * coverage_confidence

    # Blended master scalar = (1-w)*coherence + w*safety
    # This prevents misleadingly high scores from small diverse sets
    coherence_scalar = raw_dot_product * sample_confidence
    coherence_scalar = max(0.001, coherence_scalar)

    safety_score = max(0.0, min(1.0, safety_score))
    safety_weight = max(0.0, min(1.0, safety_weight))
    master_scalar = ((1.0 - safety_weight) * coherence_scalar) + (safety_weight * safety_score)
    master_scalar = max(0.001, master_scalar)

    return MasterScalarResult(
        master_scalar=master_scalar,
        coherence_scalar=coherence_scalar,
        safety_score=safety_score,
        safety_weight=safety_weight,
        raw_dot_product=raw_dot_product,
        sample_confidence=sample_confidence,
        sample_count=total_count,
        sampled_count=sampled_count,
        pair_count=pair_count
    )


async def compute_master_scalar_from_file(
    file_path: Path = None,
    max_samples: int = 500,
    session: aiohttp.ClientSession = None
) -> MasterScalarResult:
    """
    Compute master scalar directly from training data file.

    Args:
        file_path: Path to JSONL file (default: data_store/generated_training_data.jsonl)
        max_samples: Maximum samples to analyze (for efficiency)
        session: Optional aiohttp session

    Returns:
        MasterScalarResult with the computed master scalar
    """
    cot_texts = extract_cot_texts(file_path)
    total_count = len(cot_texts)

    if total_count < 2:
        return MasterScalarResult(
            master_scalar=0.001,
            coherence_scalar=0.001,
            safety_score=compute_safety_score(),
            safety_weight=SAFETY_SCORE_WEIGHT,
            raw_dot_product=0.001,
            sample_confidence=0.0,
            sample_count=total_count,
            sampled_count=total_count,
            pair_count=0
        )

    # Sample if too many
    sampled_texts = cot_texts
    if max_samples and total_count > max_samples:
        import random
        sampled_texts = random.sample(cot_texts, max_samples)

    sampled_count = len(sampled_texts)

    embeddings = await get_embeddings(sampled_texts, session)
    safety_score = compute_safety_score()
    return compute_master_scalar(
        embeddings,
        total_count=total_count,
        sampled_count=sampled_count,
        safety_score=safety_score,
        safety_weight=SAFETY_SCORE_WEIGHT,
    )


def compute_master_scalar_sync(texts: List[str] = None) -> MasterScalarResult:
    """
    Synchronous wrapper for computing master scalar.

    Args:
        texts: Optional list of CoT texts. If None, reads from data file.

    Returns:
        MasterScalarResult
    """
    async def _async_compute():
        if texts is None:
            return await compute_master_scalar_from_file()
        else:
            async with aiohttp.ClientSession() as session:
                embeddings = await get_embeddings(texts, session)
                total_count = len(texts)
                safety_score = compute_safety_score()
                return compute_master_scalar(
                    embeddings,
                    total_count=total_count,
                    sampled_count=total_count,
                    safety_score=safety_score,
                    safety_weight=SAFETY_SCORE_WEIGHT,
                )

    return asyncio.run(_async_compute())


# ============================================================================
# LIVE TRACKING (for use during generation)
# ============================================================================

class MasterScalarTracker:
    """
    Tracks master scalar during training data generation.

    Always tracks key values together:
    1. master_scalar - enhanced score with sample confidence
    2. raw_dot_product - raw avg pairwise dot product
    3. sample_count - total training samples
    4. sampled_count - samples actually embedded

    Provides live updates without blocking generation.
    """

    def __init__(self):
        self.current_scalar: float = 0.001
        self.coherence_scalar: float = 0.001
        self.safety_score: float = 0.0
        self.safety_weight: float = SAFETY_SCORE_WEIGHT
        self.raw_dot_product: float = 0.001
        self.sample_confidence: float = 0.0
        self.previous_scalar: float = 0.001
        self.sample_count: int = 0
        self.sampled_count: int = 0
        self.update_count: int = 0
        self._embeddings_cache: List[np.ndarray] = []

    @property
    def delta(self) -> float:
        """Change since last update."""
        return self.current_scalar - self.previous_scalar

    async def update(self, session: aiohttp.ClientSession = None) -> MasterScalarResult:
        """
        Update master scalar from current training data.
        """
        self.previous_scalar = self.current_scalar
        result = await compute_master_scalar_from_file(session=session)
        self.current_scalar = result.master_scalar
        self.coherence_scalar = result.coherence_scalar
        self.safety_score = result.safety_score
        self.safety_weight = result.safety_weight
        self.raw_dot_product = result.raw_dot_product
        self.sample_confidence = result.sample_confidence
        self.sample_count = result.sample_count
        self.sampled_count = result.sampled_count
        self.update_count += 1
        return result

    def update_sync(self) -> MasterScalarResult:
        """Synchronous update."""
        return asyncio.run(self.update())

    def get_status(self) -> Dict[str, Any]:
        """Get current status for display - always includes all 3 key values."""
        return {
            "master_scalar": self.current_scalar,
            "coherence_scalar": self.coherence_scalar,
            "safety_score": self.safety_score,
            "safety_weight": self.safety_weight,
            "raw_dot_product": self.raw_dot_product,
            "sample_count": self.sample_count,
            "sampled_count": self.sampled_count,
            "delta": self.delta,
            "sample_confidence": self.sample_confidence,
            "update_count": self.update_count
        }

    def format_display(self) -> str:
        """Format the 3 key values for display - use this everywhere."""
        return (
            f"Master: {self.current_scalar:.6f} | "
            f"Safety: {self.safety_score:.3f} | "
            f"Dot: {self.raw_dot_product:.6f} | "
            f"Samples: {self.sample_count} (sampled {self.sampled_count})"
        )


# Global tracker instance
_tracker: Optional[MasterScalarTracker] = None


def get_tracker() -> MasterScalarTracker:
    """Get or create global tracker."""
    global _tracker
    if _tracker is None:
        _tracker = MasterScalarTracker()
    return _tracker


# ============================================================================
# CLI
# ============================================================================

def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Master Scalar Optimizer")
    parser.add_argument("--file", type=str, help="Path to JSONL file")
    parser.add_argument("--max-samples", type=int, default=500, help="Max samples to analyze")
    args = parser.parse_args()

    print("=" * 60)
    print("MASTER SCALAR OPTIMIZER")
    print("Author: Bo Shang <bo@shang.software>")
    print("=" * 60)

    file_path = Path(args.file) if args.file else None

    async def _compute():
        async with aiohttp.ClientSession() as session:
            return await compute_master_scalar_from_file(
                file_path=file_path,
                max_samples=args.max_samples,
                session=session
            )

    result = asyncio.run(_compute())

    print(f"\nResults:")
    print(f"  Master Scalar:     {result.master_scalar:.6f}  (coherence + safety)")
    print(f"  Coherence Scalar:  {result.coherence_scalar:.6f}  (raw dot * confidence)")
    print(f"  Safety Score:      {result.safety_score:.4f}  (weight {result.safety_weight:.2f})")
    print(f"  Raw Dot Product:   {result.raw_dot_product:.6f}  (avg pairwise dot product)")
    print(f"  Sample Confidence: {result.sample_confidence:.4f}  (size + coverage)")
    print(f"  Training Samples:  {result.sample_count} (sampled {result.sampled_count})")
    print(f"  Pairs Computed:    {result.pair_count:,}")
    print()


if __name__ == "__main__":
    main()
