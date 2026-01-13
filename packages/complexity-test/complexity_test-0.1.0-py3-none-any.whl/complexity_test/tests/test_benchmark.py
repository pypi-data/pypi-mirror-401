"""
Speed benchmark: Multicouche vs Standard transformer.
"""

import torch
import time
from complexity_test.core import MulticoucheBlock, StandardBlock


def test_speed_benchmark(device: str = "cpu", num_runs: int = 50, verbose: bool = True):
    """Benchmark Multicouche vs Standard block."""
    if verbose:
        print("\n" + "="*60)
        print("TEST: Speed Benchmark")
        print("="*60)

    hidden_size = 512
    intermediate_size = 1408
    batch_size = 8
    seq_len = 512

    # Create blocks
    multicouche = MulticoucheBlock(
        hidden_size, intermediate_size,
        use_dynamics=True,
        use_token_routed_mlp=True,
    ).to(device)

    standard = StandardBlock(
        hidden_size, intermediate_size,
    ).to(device)

    x = torch.randn(batch_size, seq_len, hidden_size, device=device)

    # Warmup
    for _ in range(10):
        _ = multicouche(x)
        _ = standard(x)

    if device == "cuda":
        torch.cuda.synchronize()

    # Benchmark Multicouche
    start = time.perf_counter()
    for _ in range(num_runs):
        _ = multicouche(x)
    if device == "cuda":
        torch.cuda.synchronize()
    multicouche_time = (time.perf_counter() - start) / num_runs * 1000

    # Benchmark Standard
    start = time.perf_counter()
    for _ in range(num_runs):
        _ = standard(x)
    if device == "cuda":
        torch.cuda.synchronize()
    standard_time = (time.perf_counter() - start) / num_runs * 1000

    overhead = ((multicouche_time / standard_time) - 1) * 100

    if verbose:
        print(f"  Device: {device}")
        print(f"  Batch: {batch_size}, Seq: {seq_len}, Hidden: {hidden_size}")
        print(f"  Standard block:    {standard_time:.2f} ms")
        print(f"  Multicouche block: {multicouche_time:.2f} ms")
        print(f"  Overhead: {overhead:+.1f}%")

        if overhead < 30:
            print("  EXCELLENT: Overhead < 30%")
        elif overhead < 50:
            print("  GOOD: Overhead < 50%")
        else:
            print("  WARNING: Overhead > 50%")

    return {
        "standard_ms": standard_time,
        "multicouche_ms": multicouche_time,
        "overhead_percent": overhead,
    }


def test_training_speed(device: str = "cpu", num_steps: int = 20, verbose: bool = True):
    """Benchmark training step speed."""
    if verbose:
        print("\n" + "="*60)
        print("TEST: Training Speed")
        print("="*60)

    hidden_size = 512
    intermediate_size = 1408
    batch_size = 8
    seq_len = 512
    num_layers = 6

    # Create model
    class TestModel(torch.nn.Module):
        def __init__(self, use_multicouche: bool):
            super().__init__()
            if use_multicouche:
                self.layers = torch.nn.ModuleList([
                    MulticoucheBlock(hidden_size, intermediate_size)
                    for _ in range(num_layers)
                ])
            else:
                self.layers = torch.nn.ModuleList([
                    StandardBlock(hidden_size, intermediate_size)
                    for _ in range(num_layers)
                ])
            self.use_multicouche = use_multicouche

        def forward(self, x):
            v = None
            for layer in self.layers:
                if self.use_multicouche:
                    x, v = layer(x, v)
                else:
                    x = layer(x)
            return x

    multicouche_model = TestModel(use_multicouche=True).to(device)
    standard_model = TestModel(use_multicouche=False).to(device)

    opt_multi = torch.optim.AdamW(multicouche_model.parameters(), lr=1e-4)
    opt_std = torch.optim.AdamW(standard_model.parameters(), lr=1e-4)

    # Warmup
    x = torch.randn(batch_size, seq_len, hidden_size, device=device)
    for _ in range(3):
        opt_multi.zero_grad()
        multicouche_model(x).sum().backward()
        opt_multi.step()

        opt_std.zero_grad()
        standard_model(x).sum().backward()
        opt_std.step()

    if device == "cuda":
        torch.cuda.synchronize()

    # Benchmark Multicouche training
    start = time.perf_counter()
    for _ in range(num_steps):
        x = torch.randn(batch_size, seq_len, hidden_size, device=device)
        opt_multi.zero_grad()
        loss = multicouche_model(x).sum()
        loss.backward()
        opt_multi.step()
    if device == "cuda":
        torch.cuda.synchronize()
    multi_time = (time.perf_counter() - start) / num_steps * 1000

    # Benchmark Standard training
    start = time.perf_counter()
    for _ in range(num_steps):
        x = torch.randn(batch_size, seq_len, hidden_size, device=device)
        opt_std.zero_grad()
        loss = standard_model(x).sum()
        loss.backward()
        opt_std.step()
    if device == "cuda":
        torch.cuda.synchronize()
    std_time = (time.perf_counter() - start) / num_steps * 1000

    overhead = ((multi_time / std_time) - 1) * 100

    if verbose:
        print(f"  Layers: {num_layers}")
        print(f"  Standard training:    {std_time:.2f} ms/step")
        print(f"  Multicouche training: {multi_time:.2f} ms/step")
        print(f"  Training overhead: {overhead:+.1f}%")

    return {
        "standard_ms": std_time,
        "multicouche_ms": multi_time,
        "overhead_percent": overhead,
    }


if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    test_speed_benchmark(device)
    test_training_speed(device)
