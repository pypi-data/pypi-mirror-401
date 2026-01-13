"""
Complexity Test - Test package for Multicouche architecture.

Tests KQV Attention + INL Dynamics + Token-Routed MLP with Triton.
"""

__version__ = "0.1.0"

from complexity_test.core import (
    RMSNorm,
    INLDynamics,
    KQVAttention,
    TokenRoutedMLP,
    MulticoucheBlock,
)

__all__ = [
    "RMSNorm",
    "INLDynamics",
    "KQVAttention",
    "TokenRoutedMLP",
    "MulticoucheBlock",
]
