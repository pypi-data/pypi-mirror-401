"""
Test CUDA compatibility.
"""

import torch
from complexity_test.core import MulticoucheBlock


def test_cuda_compatibility(verbose: bool = True):
    """Test CUDA compatibility and memory usage."""
    if verbose:
        print("\n" + "="*60)
        print("TEST: CUDA Compatibility")
        print("="*60)

    if not torch.cuda.is_available():
        if verbose:
            print("  SKIP: CUDA not available")
        return None

    device = "cuda"

    if verbose:
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

    torch.cuda.reset_peak_memory_stats()

    hidden_size = 768
    intermediate_size = 2048
    batch_size = 8
    seq_len = 1024
    num_layers = 12

    try:
        # Create model
        layers = torch.nn.ModuleList([
            MulticoucheBlock(hidden_size, intermediate_size)
            for _ in range(num_layers)
        ]).to(device)

        x = torch.randn(batch_size, seq_len, hidden_size, device=device)

        # Forward
        v = None
        for layer in layers:
            x, v = layer(x, v)

        peak_memory = torch.cuda.max_memory_allocated() / 1e9
        num_params = sum(p.numel() for p in layers.parameters()) / 1e6

        if verbose:
            print(f"  Layers: {num_layers}")
            print(f"  Batch: {batch_size}, Seq: {seq_len}, Hidden: {hidden_size}")
            print(f"  Parameters: {num_params:.1f}M")
            print(f"  Peak memory: {peak_memory:.2f} GB")
            print("  PASS")

        return {
            "peak_memory_gb": peak_memory,
            "num_params_m": num_params,
        }

    except Exception as e:
        if verbose:
            print(f"  FAIL: {e}")
        return False


def test_cuda_training(verbose: bool = True):
    """Test CUDA training step."""
    if verbose:
        print("\n" + "="*60)
        print("TEST: CUDA Training Step")
        print("="*60)

    if not torch.cuda.is_available():
        if verbose:
            print("  SKIP: CUDA not available")
        return None

    device = "cuda"
    hidden_size = 512
    intermediate_size = 1408
    batch_size = 8
    seq_len = 512
    num_layers = 4

    try:
        # Model
        class TestModel(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.embed = torch.nn.Embedding(1000, hidden_size)
                self.layers = torch.nn.ModuleList([
                    MulticoucheBlock(hidden_size, intermediate_size)
                    for _ in range(num_layers)
                ])
                self.head = torch.nn.Linear(hidden_size, 1000)

            def forward(self, x):
                x = self.embed(x)
                v = None
                for layer in self.layers:
                    x, v = layer(x, v)
                return self.head(x)

        model = TestModel().to(device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

        # Training step
        input_ids = torch.randint(0, 1000, (batch_size, seq_len), device=device)
        labels = torch.randint(0, 1000, (batch_size, seq_len), device=device)

        # Forward
        logits = model(input_ids)
        loss = torch.nn.functional.cross_entropy(
            logits.view(-1, 1000), labels.view(-1)
        )

        # Backward
        optimizer.zero_grad()
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        if verbose:
            print(f"  Loss: {loss.item():.4f}")
            print(f"  Grad norm: {grad_norm.item():.4f}")
            print("  PASS")

        return True

    except Exception as e:
        if verbose:
            print(f"  FAIL: {e}")
            import traceback
            traceback.print_exc()
        return False


if __name__ == "__main__":
    test_cuda_compatibility()
    test_cuda_training()
