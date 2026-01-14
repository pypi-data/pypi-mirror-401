#!/usr/bin/env python3
"""
Standalone training script for erosolar v0.01

This is a standalone version that doesn't use mini_the_agentic_cli.py.
Trains the first version of erosolar with infini-small preset.

Usage:
    python train_v001.py                    # Full training
    python train_v001.py --benchmark        # Quick benchmark to estimate time
    python train_v001.py --epochs 5         # Override epochs
"""

import argparse
import json
import math
import time
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from torch.optim.lr_scheduler import LambdaLR

# Colors
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
MAGENTA = "\033[95m"


def setup_device(seed: int = 42) -> torch.device:
    """Setup compute device with preference for MPS on Apple Silicon."""
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        device = torch.device("cuda")
        torch.cuda.manual_seed_all(seed)
        print(f"{GREEN}Using CUDA: {torch.cuda.get_device_name()}{RESET}")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = torch.device("mps")
        print(f"{GREEN}Using Apple Silicon MPS{RESET}")
    else:
        device = torch.device("cpu")
        print(f"{YELLOW}Using CPU (this will be slow){RESET}")

    return device


@dataclass
class ModelConfig:
    """Model architecture for infini-small (v0.01)."""
    vocab_size: int = 8000
    max_seq_len: int = 1024
    embed_dim: int = 384
    num_heads: int = 6
    num_layers: int = 6
    ff_dim: int = 1024
    dropout: float = 0.1
    use_infini_attention: bool = True
    segment_size: int = 256
    use_delta_rule: bool = True
    use_rope: bool = True


class SimpleDataset(Dataset):
    """Dataset that loads training data from all JSONL files in data_store."""

    def __init__(self, data_path: Path, tokenizer, seq_len: int):
        self.tokenizer = tokenizer
        self.seq_len = seq_len
        self.examples = []

        # Load from all training JSONL files in data_store directory
        data_dir = data_path.parent
        jsonl_patterns = [
            "*_training_data.jsonl",
            "*_training.jsonl"
        ]

        loaded_files = set()
        total_loaded = 0

        for pattern in jsonl_patterns:
            for data_file in data_dir.glob(pattern):
                if data_file.name in loaded_files:
                    continue
                loaded_files.add(data_file.name)

                file_count = 0
                print(f"{DIM}  Loading from {data_file.name}...{RESET}")
                try:
                    with open(data_file) as f:
                        for line in f:
                            try:
                                record = json.loads(line)
                                msgs = record.get("messages", [])
                                if len(msgs) >= 2:
                                    prompt = msgs[0].get("content", "")
                                    response = msgs[1].get("content", "")
                                    text = f"<|user|>\n{prompt}\n<|end_turn|>\n<|assistant|>\n{response}\n<|end_turn|>"
                                    tokens = tokenizer.encode(text)
                                    if len(tokens) > 10:
                                        self.examples.append(tokens)
                                        file_count += 1
                            except:
                                continue
                    print(f"{GREEN}    → {file_count:,} examples from {data_file.name}{RESET}")
                    total_loaded += file_count
                except Exception as e:
                    print(f"{RED}    Error loading {data_file.name}: {e}{RESET}")

        print(f"{GREEN}  Total loaded: {len(self.examples):,} examples from {len(loaded_files)} files{RESET}")

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        tokens = self.examples[idx]
        if len(tokens) > self.seq_len + 1:
            tokens = tokens[:self.seq_len + 1]
        else:
            tokens = tokens + [0] * (self.seq_len + 1 - len(tokens))
        x = torch.tensor(tokens[:-1], dtype=torch.long)
        y = torch.tensor(tokens[1:], dtype=torch.long)
        return x, y


def get_lr_scheduler(optimizer, warmup_steps: int, total_steps: int, min_lr_ratio: float = 0.1):
    """Learning rate scheduler with warmup and cosine decay."""
    def lr_lambda(step):
        if step < warmup_steps:
            return step / max(1, warmup_steps)
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return min_lr_ratio + 0.5 * (1.0 - min_lr_ratio) * (1.0 + math.cos(math.pi * progress))
    return LambdaLR(optimizer, lr_lambda)


def format_time(seconds: float) -> str:
    """Format seconds to human readable."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins, secs = divmod(int(seconds), 60)
        return f"{mins}m {secs}s"
    else:
        hours, remainder = divmod(int(seconds), 3600)
        mins, secs = divmod(remainder, 60)
        return f"{hours}h {mins}m {secs}s"


def build_corpus_for_tokenizer(data_path: Path) -> str:
    """Build corpus text for tokenizer training."""
    texts = []
    with open(data_path) as f:
        for line in f:
            try:
                record = json.loads(line)
                msgs = record.get("messages", [])
                if len(msgs) >= 2:
                    prompt = msgs[0].get("content", "")
                    response = msgs[1].get("content", "")
                    text = f"<|user|>\n{prompt}\n<|end_turn|>\n<|assistant|>\n{response}\n<|end_turn|>"
                    texts.append(text)
            except:
                continue
    return "\n\n".join(texts)


def run_benchmark(model, tokenizer, config, device, data_path: Path, epochs: int) -> dict:
    """Run a quick benchmark to estimate total training time."""
    print(f"\n{BOLD}{CYAN}{'═' * 60}{RESET}")
    print(f"{BOLD}{CYAN}  BENCHMARK MODE - Estimating Training Time{RESET}")
    print(f"{BOLD}{CYAN}{'═' * 60}{RESET}")

    dataset = SimpleDataset(data_path, tokenizer, config.max_seq_len)

    if len(dataset) == 0:
        print(f"{RED}No data to benchmark{RESET}")
        return {}

    batch_size = 8
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0)

    optimizer = AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
    criterion = nn.CrossEntropyLoss(ignore_index=0)

    model.train()

    # Warmup
    print(f"{DIM}  Warmup pass...{RESET}")
    warmup_batches = min(5, len(loader))
    for batch_idx, (x, y) in enumerate(loader):
        if batch_idx >= warmup_batches:
            break
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        if hasattr(model, 'memory_manager'):
            logits = model(x, use_memory=False, update_memory=False)
        else:
            logits = model(x)
        loss = criterion(logits.view(-1, logits.size(-1)), y.view(-1))
        loss.backward()
        optimizer.step()

    # Benchmark
    print(f"{DIM}  Timing benchmark batches...{RESET}")
    benchmark_batches = min(20, len(loader))

    start_time = time.time()
    tokens_processed = 0

    for batch_idx, (x, y) in enumerate(loader):
        if batch_idx >= benchmark_batches:
            break
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        if hasattr(model, 'memory_manager'):
            logits = model(x, use_memory=False, update_memory=False)
        else:
            logits = model(x)
        loss = criterion(logits.view(-1, logits.size(-1)), y.view(-1))
        loss.backward()
        optimizer.step()
        tokens_processed += (y != 0).sum().item()

    elapsed = time.time() - start_time

    time_per_batch = elapsed / benchmark_batches
    tokens_per_second = tokens_processed / elapsed

    total_batches = len(loader) * epochs
    estimated_total = time_per_batch * total_batches

    print(f"\n{BOLD}{GREEN}{'═' * 60}{RESET}")
    print(f"{BOLD}{GREEN}  BENCHMARK RESULTS{RESET}")
    print(f"{GREEN}{'═' * 60}{RESET}")
    print(f"{DIM}  Device: {device}{RESET}")
    print(f"{DIM}  Training examples: {len(dataset):,}{RESET}")
    print(f"{DIM}  Batch size: {batch_size}{RESET}")
    print(f"{DIM}  Batches per epoch: {len(loader):,}{RESET}")
    print(f"{DIM}  Epochs: {epochs}{RESET}")
    print(f"{DIM}  Total batches: {total_batches:,}{RESET}")
    print()
    print(f"{CYAN}  Time per batch: {time_per_batch*1000:.1f} ms{RESET}")
    print(f"{CYAN}  Tokens/second: {tokens_per_second:.0f}{RESET}")
    print()
    print(f"{BOLD}  ESTIMATED TOTAL TRAINING TIME: {format_time(estimated_total)}{RESET}")
    print(f"{GREEN}{'═' * 60}{RESET}")

    return {
        'device': str(device),
        'examples': len(dataset),
        'batches_per_epoch': len(loader),
        'epochs': epochs,
        'total_batches': total_batches,
        'time_per_batch_ms': time_per_batch * 1000,
        'tokens_per_second': tokens_per_second,
        'estimated_total_seconds': estimated_total,
        'estimated_total_formatted': format_time(estimated_total)
    }


def train(model, tokenizer, config, device, data_path: Path, epochs: int) -> float:
    """Full training loop."""
    print(f"\n{BOLD}{CYAN}{'═' * 60}{RESET}")
    print(f"{BOLD}{CYAN}  TRAINING{RESET}")
    print(f"{BOLD}{CYAN}{'═' * 60}{RESET}")

    dataset = SimpleDataset(data_path, tokenizer, config.max_seq_len)

    if len(dataset) == 0:
        print(f"{RED}No training data!{RESET}")
        return 0.0

    batch_size = 8
    loader = DataLoader(
        dataset, batch_size=batch_size, shuffle=True,
        num_workers=0, pin_memory=(device.type == 'cuda')
    )

    total_steps = len(loader) * epochs

    optimizer = AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
    scheduler = get_lr_scheduler(optimizer, warmup_steps=100, total_steps=total_steps)
    criterion = nn.CrossEntropyLoss(ignore_index=0)

    print(f"{DIM}  Examples: {len(dataset):,}{RESET}")
    print(f"{DIM}  Batch size: {batch_size}{RESET}")
    print(f"{DIM}  Batches/epoch: {len(loader):,}{RESET}")
    print(f"{DIM}  Epochs: {epochs}{RESET}")
    print(f"{DIM}  Total steps: {total_steps:,}{RESET}")
    print()

    model.train()
    training_start = time.time()
    total_tokens = 0
    best_loss = float('inf')

    for epoch in range(epochs):
        epoch_start = time.time()
        epoch_loss = 0.0
        epoch_tokens = 0

        for batch_idx, (x, y) in enumerate(loader):
            x, y = x.to(device), y.to(device)

            optimizer.zero_grad()

            if hasattr(model, 'memory_manager'):
                logits = model(x, use_memory=False, update_memory=False)
            else:
                logits = model(x)

            loss = criterion(logits.view(-1, logits.size(-1)), y.view(-1))
            loss.backward()

            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()

            batch_tokens = (y != 0).sum().item()
            epoch_loss += loss.item() * batch_tokens
            epoch_tokens += batch_tokens
            total_tokens += batch_tokens

            if (batch_idx + 1) % 50 == 0:
                elapsed = time.time() - training_start
                tok_per_sec = total_tokens / elapsed if elapsed > 0 else 0
                progress = (epoch * len(loader) + batch_idx + 1) / total_steps
                eta = (elapsed / progress - elapsed) if progress > 0 else 0
                lr = scheduler.get_last_lr()[0]

                print(f"\r{DIM}Epoch {epoch+1}/{epochs} Batch {batch_idx+1}/{len(loader)} | "
                      f"Loss: {epoch_loss/max(epoch_tokens,1):.4f} | LR: {lr:.2e} | "
                      f"Tok/s: {tok_per_sec:.0f} | ETA: {format_time(eta)}{RESET}    ",
                      end='', flush=True)

        epoch_time = time.time() - epoch_start
        avg_loss = epoch_loss / max(epoch_tokens, 1)

        if avg_loss < best_loss:
            best_loss = avg_loss

        print(f"\n{GREEN}Epoch {epoch+1}/{epochs} complete: Loss {avg_loss:.4f} ({format_time(epoch_time)}){RESET}")

    total_time = time.time() - training_start

    print(f"\n{BOLD}{GREEN}{'═' * 60}{RESET}")
    print(f"{BOLD}{GREEN}  TRAINING COMPLETE{RESET}")
    print(f"{GREEN}{'═' * 60}{RESET}")
    print(f"{DIM}  Best loss: {best_loss:.4f}{RESET}")
    print(f"{DIM}  Total time: {format_time(total_time)}{RESET}")
    print(f"{DIM}  Total tokens: {total_tokens:,}{RESET}")
    print(f"{DIM}  Avg tokens/sec: {total_tokens/total_time:.0f}{RESET}")

    return best_loss


def main():
    parser = argparse.ArgumentParser(description="Train erosolar v0.01 (standalone)")
    parser.add_argument("--benchmark", action="store_true",
                       help="Run quick benchmark to estimate training time, then exit")
    parser.add_argument("--epochs", type=int, default=5,
                       help="Number of epochs (default: 5)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--data", type=str, default="data_store/generated_training_data.jsonl",
                       help="Path to training data JSONL")
    args = parser.parse_args()

    print(f"\n{BOLD}{CYAN}{'═' * 60}{RESET}")
    print(f"{BOLD}{CYAN}  EROSOLAR v0.01 - Standalone Training{RESET}")
    print(f"{BOLD}{CYAN}{'═' * 60}{RESET}")
    print(f"{DIM}  Preset: infini-small (~10M params){RESET}")
    print(f"{DIM}  Architecture: Infini-attention with compressive memory{RESET}")
    print(f"{DIM}  Segment size: 256 tokens{RESET}")
    print()

    # Setup device
    device = setup_device(args.seed)

    # Data path
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"{RED}ERROR: Training data not found at {data_path}{RESET}")
        sys.exit(1)

    # Count records
    with open(data_path) as f:
        num_records = sum(1 for _ in f)
    print(f"{GREEN}Training data: {num_records:,} records{RESET}")

    # Train tokenizer
    print(f"\n{DIM}Training tokenizer...{RESET}")
    from tokenizer import BPETokenizer
    tokenizer = BPETokenizer()

    corpus = build_corpus_for_tokenizer(data_path)
    print(f"{DIM}  Corpus size: {len(corpus):,} chars{RESET}")

    tokenizer.train(corpus, vocab_size=8000)
    print(f"{GREEN}  Tokenizer trained: {tokenizer.vocab_size} tokens{RESET}")

    # Create model config
    config = ModelConfig()
    config.vocab_size = tokenizer.vocab_size

    # Create model
    print(f"\n{DIM}Creating model...{RESET}")
    from model import ModelConfig as MC, create_model
    model_config = MC(
        vocab_size=config.vocab_size,
        max_seq_len=config.max_seq_len,
        embed_dim=config.embed_dim,
        num_heads=config.num_heads,
        num_layers=config.num_layers,
        ff_dim=config.ff_dim,
        dropout=config.dropout,
        use_infini_attention=config.use_infini_attention,
        segment_size=config.segment_size,
        use_delta_rule=config.use_delta_rule,
        use_rope=config.use_rope
    )
    model = create_model(model_config, device)

    num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"{GREEN}  Model created: {num_params:,} parameters (~{num_params/1e6:.1f}M){RESET}")

    # Benchmark mode
    if args.benchmark:
        results = run_benchmark(model, tokenizer, config, device, data_path, args.epochs)
        print(f"\n{BOLD}Benchmark complete. Exiting.{RESET}")
        return

    # Full training
    best_loss = train(model, tokenizer, config, device, data_path, args.epochs)

    # Save model
    print(f"\n{DIM}Saving model to registry...{RESET}")
    from registry import get_registry
    from config import get_preset

    registry = get_registry()
    full_config = get_preset("infini-small")
    full_config.vocab_size = tokenizer.vocab_size

    info = registry.save_model(
        name="erosolar",
        description="erosolar v0.01 - trained with standalone script",
        model=model,
        tokenizer=tokenizer,
        config=full_config,
        epochs=args.epochs,
        loss=best_loss,
        training_time=0,
        tags=["v0.01", "infini-small", "standalone"],
        preset="infini-small"
    )

    print(f"{GREEN}  Saved: {info.name}{RESET}")
    print(f"\n{DIM}  Use: python generate.py --model erosolar{RESET}")


if __name__ == "__main__":
    main()
