"""
KQV Attention with GQA and QK-Norm (Llama-style)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from complexity_test.core.normalization import RMSNorm


class KQVAttention(nn.Module):
    """
    KQV Attention with:
    - GQA (Grouped Query Attention)
    - QK-Norm (2024 innovation)
    - SDPA (Flash Attention)
    """

    def __init__(
        self,
        hidden_size: int,
        num_heads: int = 8,
        num_kv_heads: int = 2,
        use_qk_norm: bool = True,
        dropout: float = 0.0,
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.head_dim = hidden_size // num_heads
        self.kv_dim = self.head_dim * num_kv_heads
        self.use_qk_norm = use_qk_norm

        # Projections
        self.q_proj = nn.Linear(hidden_size, hidden_size, bias=False)
        self.k_proj = nn.Linear(hidden_size, self.kv_dim, bias=False)
        self.v_proj = nn.Linear(hidden_size, self.kv_dim, bias=False)
        self.out_proj = nn.Linear(hidden_size, hidden_size, bias=False)

        # QK Normalization
        if use_qk_norm:
            self.q_norm = RMSNorm(self.head_dim)
            self.k_norm = RMSNorm(self.head_dim)

        self.dropout = dropout

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, N, D = x.shape

        # Project
        q = self.q_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, N, self.num_kv_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, N, self.num_kv_heads, self.head_dim).transpose(1, 2)

        # QK-Norm
        if self.use_qk_norm:
            q = self.q_norm(q)
            k = self.k_norm(k)

        # GQA expansion
        num_rep = self.num_heads // self.num_kv_heads
        k = k.repeat_interleave(num_rep, dim=1)
        v = v.repeat_interleave(num_rep, dim=1)

        # SDPA (Flash Attention if available)
        out = F.scaled_dot_product_attention(
            q, k, v,
            dropout_p=self.dropout if self.training else 0.0
        )

        out = out.transpose(1, 2).contiguous().view(B, N, D)
        return self.out_proj(out)
