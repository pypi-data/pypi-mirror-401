"""
Test Triton kernels.
"""

import torch


def test_triton_kernels(verbose: bool = True):
    """Test Triton kernel availability and correctness."""
    if verbose:
        print("\n" + "="*60)
        print("TEST: Triton Kernels")
        print("="*60)

    # Check Triton availability
    try:
        import triton
        import triton.language as tl
        has_triton = True
        if verbose:
            print(f"  Triton version: {triton.__version__}")
    except ImportError:
        has_triton = False
        if verbose:
            print("  SKIP: Triton not installed")
        return None

    if not torch.cuda.is_available():
        if verbose:
            print("  SKIP: CUDA not available")
        return None

    # Test simple Triton kernel
    try:
        @triton.jit
        def add_kernel(x_ptr, y_ptr, out_ptr, n, BLOCK: tl.constexpr):
            pid = tl.program_id(0)
            offs = pid * BLOCK + tl.arange(0, BLOCK)
            mask = offs < n
            x = tl.load(x_ptr + offs, mask=mask)
            y = tl.load(y_ptr + offs, mask=mask)
            tl.store(out_ptr + offs, x + y, mask=mask)

        n = 1024
        x = torch.randn(n, device="cuda")
        y = torch.randn(n, device="cuda")
        out = torch.empty_like(x)

        grid = (triton.cdiv(n, 256),)
        add_kernel[grid](x, y, out, n, BLOCK=256)

        expected = x + y
        if torch.allclose(out, expected, atol=1e-5):
            if verbose:
                print("  Simple kernel: PASS")
        else:
            if verbose:
                print("  Simple kernel: FAIL (output mismatch)")
            return False

    except Exception as e:
        if verbose:
            print(f"  Simple kernel: FAIL - {e}")
        return False

    # Test INL Dynamics Triton kernel
    try:
        from complexity_test.cuda import triton_inl_dynamics, TritonINLDynamics

        hidden_size = 512
        batch_size = 4
        seq_len = 256

        dynamics = TritonINLDynamics(hidden_size, use_triton=True).cuda()
        x = torch.randn(batch_size, seq_len, hidden_size, device="cuda")

        h_out, v_out = dynamics(x)

        assert h_out.shape == x.shape
        assert v_out.shape == x.shape

        if verbose:
            print("  INL Dynamics Triton: PASS")

    except Exception as e:
        if verbose:
            print(f"  INL Dynamics Triton: FAIL - {e}")
        return False

    # Benchmark Triton vs PyTorch
    try:
        import time

        dynamics_triton = TritonINLDynamics(hidden_size, use_triton=True).cuda()
        dynamics_pytorch = TritonINLDynamics(hidden_size, use_triton=False).cuda()

        x = torch.randn(batch_size, seq_len, hidden_size, device="cuda")

        # Warmup
        for _ in range(10):
            _ = dynamics_triton(x)
            _ = dynamics_pytorch(x)
        torch.cuda.synchronize()

        # Benchmark
        num_runs = 100

        start = time.perf_counter()
        for _ in range(num_runs):
            _ = dynamics_triton(x)
        torch.cuda.synchronize()
        triton_time = (time.perf_counter() - start) / num_runs * 1000

        start = time.perf_counter()
        for _ in range(num_runs):
            _ = dynamics_pytorch(x)
        torch.cuda.synchronize()
        pytorch_time = (time.perf_counter() - start) / num_runs * 1000

        speedup = pytorch_time / triton_time

        if verbose:
            print(f"  PyTorch: {pytorch_time:.3f} ms")
            print(f"  Triton:  {triton_time:.3f} ms")
            print(f"  Speedup: {speedup:.2f}x")

    except Exception as e:
        if verbose:
            print(f"  Benchmark: FAIL - {e}")

    return True


if __name__ == "__main__":
    test_triton_kernels()
