"""
Transformer Blocks: Multicouche and Standard
"""

import torch
import torch.nn as nn
from typing import Optional, Tuple

from complexity_test.core.normalization import RMSNorm
from complexity_test.core.dynamics import INLDynamics
from complexity_test.core.attention import KQVAttention
from complexity_test.core.mlp import TokenRoutedMLP, StandardMLP


class MulticoucheBlock(nn.Module):
    """
    Multicouche Block: KQV + INL Dynamics + Token-Routed MLP

    Architecture:
        1. KQV Attention (perception)
        2. INL Dynamics (control)
        3. Token-Routed MLP (transformation)
    """

    def __init__(
        self,
        hidden_size: int,
        intermediate_size: int,
        num_heads: int = 8,
        num_kv_heads: int = 2,
        num_experts: int = 4,
        use_token_routed_mlp: bool = True,
        use_dynamics: bool = True,
        use_qk_norm: bool = True,
    ):
        super().__init__()
        self.use_dynamics = use_dynamics
        self.use_token_routed_mlp = use_token_routed_mlp

        # Norms
        self.norm1 = RMSNorm(hidden_size)
        self.norm2 = RMSNorm(hidden_size)

        # 1. KQV Attention
        self.attn = KQVAttention(
            hidden_size, num_heads, num_kv_heads, use_qk_norm
        )

        # 2. INL Dynamics
        if use_dynamics:
            self.dynamics = INLDynamics(hidden_size)

        # 3. MLP
        if use_token_routed_mlp:
            self.mlp = TokenRoutedMLP(hidden_size, intermediate_size, num_experts)
        else:
            self.mlp = StandardMLP(hidden_size, intermediate_size)

    def forward(
        self,
        x: torch.Tensor,
        v: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        Forward pass.

        Args:
            x: [B, N, D]
            v: velocity [B, N, D] (optional)

        Returns:
            x, v
        """
        # 1. KQV Attention
        residual = x
        x = self.norm1(x)
        x = self.attn(x)

        # 2. INL Dynamics
        if self.use_dynamics:
            x, v = self.dynamics(x, v)

        x = residual + x

        # 3. MLP
        residual = x
        x = self.norm2(x)
        x = self.mlp(x)
        x = residual + x

        return x, v


class StandardBlock(nn.Module):
    """Standard Transformer Block (baseline for comparison)."""

    def __init__(
        self,
        hidden_size: int,
        intermediate_size: int,
        num_heads: int = 8,
    ):
        super().__init__()
        self.norm1 = RMSNorm(hidden_size)
        self.norm2 = RMSNorm(hidden_size)
        self.attn = KQVAttention(hidden_size, num_heads, num_heads, use_qk_norm=False)
        self.mlp = StandardMLP(hidden_size, intermediate_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.norm1(x))
        x = x + self.mlp(self.norm2(x))
        return x
