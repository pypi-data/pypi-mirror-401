# Complexity Test

Test package for **Multicouche architecture**: KQV Attention + INL Dynamics + Token-Routed MLP.

## Structure

```
complexity-test/
├── complexity_test/
│   ├── core/
│   │   ├── normalization.py   # RMSNorm
│   │   ├── dynamics.py        # INL Dynamics
│   │   ├── attention.py       # KQV Attention (GQA + QK-Norm)
│   │   ├── mlp.py             # Token-Routed MLP + Standard MLP
│   │   └── block.py           # MulticoucheBlock + StandardBlock
│   ├── cuda/
│   │   └── triton_dynamics.py # Triton-accelerated INL Dynamics
│   └── tests/
│       ├── test_forward.py    # Forward pass tests
│       ├── test_backward.py   # Backward pass (gradients)
│       ├── test_benchmark.py  # Speed benchmark
│       ├── test_cuda.py       # CUDA compatibility
│       └── test_triton.py     # Triton kernels
├── run_tests.py               # Main test runner
└── setup.py
```

## Usage

```bash
# Run all tests
python run_tests.py

# CPU only
python run_tests.py --cpu

# Verbose output
python run_tests.py --verbose
```

## Tests

1. **Forward Pass**: Test all components (RMSNorm, INLDynamics, KQVAttention, TokenRoutedMLP, MulticoucheBlock)
2. **Backward Pass**: Test gradient flow through all components
3. **Speed Benchmark**: Compare Multicouche vs Standard transformer
4. **Training Speed**: Full training step benchmark
5. **CUDA Compatibility**: Memory usage and GPU training
6. **Triton Kernels**: Test Triton-accelerated INL Dynamics

## Architecture

```
MulticoucheBlock:
    1. KQV Attention (perception)
       - GQA (Grouped Query Attention)
       - QK-Norm (stable training)
       - SDPA (Flash Attention)

    2. INL Dynamics (control)
       - Velocity tracking
       - Adaptive controller (alpha, beta, gate)
       - Learnable equilibrium (mu)

    3. Token-Routed MLP (transformation)
       - 4 experts with routing
       - SwiGLU activation
```

## Expected Results

- Forward pass: All components should work
- Backward pass: All gradients should flow
- Speed overhead: < 50% vs standard transformer
- CUDA: Should work with reasonable memory
- Triton: 2-3x speedup on INL Dynamics
