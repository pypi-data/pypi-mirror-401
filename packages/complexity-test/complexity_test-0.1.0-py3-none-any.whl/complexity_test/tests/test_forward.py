"""
Test forward pass for all components.
"""

import torch
from complexity_test.core import (
    RMSNorm,
    INLDynamics,
    KQVAttention,
    TokenRoutedMLP,
    MulticoucheBlock,
)


def test_forward_pass(device: str = "cpu", verbose: bool = True):
    """Test forward pass for all components."""
    results = {}

    if verbose:
        print("\n" + "="*60)
        print("TEST: Forward Pass")
        print("="*60)

    hidden_size = 512
    intermediate_size = 1408
    batch_size = 4
    seq_len = 256

    # Test RMSNorm
    try:
        norm = RMSNorm(hidden_size).to(device)
        x = torch.randn(batch_size, seq_len, hidden_size, device=device)
        out = norm(x)
        assert out.shape == x.shape
        results["RMSNorm"] = True
        if verbose:
            print(f"  RMSNorm: PASS")
    except Exception as e:
        results["RMSNorm"] = False
        if verbose:
            print(f"  RMSNorm: FAIL - {e}")

    # Test INLDynamics
    try:
        dynamics = INLDynamics(hidden_size).to(device)
        x = torch.randn(batch_size, seq_len, hidden_size, device=device)
        h, v = dynamics(x)
        assert h.shape == x.shape
        assert v.shape == x.shape
        results["INLDynamics"] = True
        if verbose:
            print(f"  INLDynamics: PASS")
    except Exception as e:
        results["INLDynamics"] = False
        if verbose:
            print(f"  INLDynamics: FAIL - {e}")

    # Test KQVAttention
    try:
        attn = KQVAttention(hidden_size, num_heads=8, num_kv_heads=2).to(device)
        x = torch.randn(batch_size, seq_len, hidden_size, device=device)
        out = attn(x)
        assert out.shape == x.shape
        results["KQVAttention"] = True
        if verbose:
            print(f"  KQVAttention: PASS")
    except Exception as e:
        results["KQVAttention"] = False
        if verbose:
            print(f"  KQVAttention: FAIL - {e}")

    # Test TokenRoutedMLP
    try:
        mlp = TokenRoutedMLP(hidden_size, intermediate_size, num_experts=4).to(device)
        x = torch.randn(batch_size, seq_len, hidden_size, device=device)
        out = mlp(x)
        assert out.shape == x.shape
        results["TokenRoutedMLP"] = True
        if verbose:
            print(f"  TokenRoutedMLP: PASS")
    except Exception as e:
        results["TokenRoutedMLP"] = False
        if verbose:
            print(f"  TokenRoutedMLP: FAIL - {e}")

    # Test MulticoucheBlock
    try:
        block = MulticoucheBlock(
            hidden_size, intermediate_size,
            num_heads=8, num_kv_heads=2, num_experts=4,
        ).to(device)
        x = torch.randn(batch_size, seq_len, hidden_size, device=device)
        out, velocity = block(x)
        assert out.shape == x.shape
        assert velocity.shape == x.shape
        results["MulticoucheBlock"] = True
        if verbose:
            print(f"  MulticoucheBlock: PASS")
    except Exception as e:
        results["MulticoucheBlock"] = False
        if verbose:
            print(f"  MulticoucheBlock: FAIL - {e}")

    return results


if __name__ == "__main__":
    import sys
    device = "cuda" if torch.cuda.is_available() else "cpu"
    results = test_forward_pass(device)
    passed = sum(results.values())
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    sys.exit(0 if passed == total else 1)
