"""
Test backward pass (gradients) for all components.
"""

import torch
from complexity_test.core import MulticoucheBlock


def test_backward_pass(device: str = "cpu", verbose: bool = True):
    """Test backward pass and gradient flow."""
    if verbose:
        print("\n" + "="*60)
        print("TEST: Backward Pass (Gradients)")
        print("="*60)

    hidden_size = 512
    intermediate_size = 1408
    batch_size = 4
    seq_len = 256

    block = MulticoucheBlock(
        hidden_size, intermediate_size,
        use_dynamics=True,
        use_token_routed_mlp=True,
    ).to(device)

    x = torch.randn(batch_size, seq_len, hidden_size, device=device, requires_grad=True)

    try:
        # Forward
        out, _ = block(x)
        loss = out.sum()

        # Backward
        loss.backward()

        # Check input gradient
        assert x.grad is not None, "Input gradient is None"
        input_grad_norm = x.grad.norm().item()

        # Check parameter gradients
        params_with_grad = 0
        params_without_grad = 0
        for name, param in block.named_parameters():
            if param.grad is not None:
                params_with_grad += 1
            else:
                params_without_grad += 1

        if verbose:
            print(f"  Loss: {loss.item():.4f}")
            print(f"  Input grad norm: {input_grad_norm:.4f}")
            print(f"  Params with grad: {params_with_grad}")
            print(f"  Params without grad: {params_without_grad}")

        if params_without_grad > 0:
            if verbose:
                print(f"  WARNING: {params_without_grad} params have no gradient")

        if verbose:
            print("  PASS")

        return True

    except Exception as e:
        if verbose:
            print(f"  FAIL: {e}")
            import traceback
            traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    device = "cuda" if torch.cuda.is_available() else "cpu"
    result = test_backward_pass(device)
    sys.exit(0 if result else 1)
