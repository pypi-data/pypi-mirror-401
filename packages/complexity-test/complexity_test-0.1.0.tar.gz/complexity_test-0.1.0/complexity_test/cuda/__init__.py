"""
CUDA/Triton kernels for Complexity Test
"""

HAS_TRITON = False
HAS_CUDA = False

import torch
HAS_CUDA = torch.cuda.is_available()

try:
    import triton
    import triton.language as tl
    HAS_TRITON = True
except ImportError:
    triton = None
    tl = None

from complexity_test.cuda.triton_dynamics import (
    triton_inl_dynamics,
    TritonINLDynamics,
)

__all__ = [
    "HAS_TRITON",
    "HAS_CUDA",
    "triton_inl_dynamics",
    "TritonINLDynamics",
]
