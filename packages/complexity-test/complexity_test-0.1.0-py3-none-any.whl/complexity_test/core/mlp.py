"""
MLP layers: Token-Routed MLP and Standard SwiGLU MLP
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class TokenRoutedMLP(nn.Module):
    """
    Token-Routed MLP with experts (Complexity innovation).

    Routes tokens to specialized experts based on content.
    """

    def __init__(
        self,
        hidden_size: int,
        intermediate_size: int,
        num_experts: int = 4,
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_experts = num_experts

        # Router
        self.router = nn.Linear(hidden_size, num_experts, bias=False)

        # Expert MLPs (SwiGLU)
        self.experts_gate = nn.ModuleList([
            nn.Linear(hidden_size, intermediate_size, bias=False)
            for _ in range(num_experts)
        ])
        self.experts_up = nn.ModuleList([
            nn.Linear(hidden_size, intermediate_size, bias=False)
            for _ in range(num_experts)
        ])
        self.experts_down = nn.ModuleList([
            nn.Linear(intermediate_size, hidden_size, bias=False)
            for _ in range(num_experts)
        ])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, N, D = x.shape

        # Router weights
        router_weights = F.softmax(self.router(x), dim=-1)

        # Expert outputs
        expert_outputs = []
        for i in range(self.num_experts):
            gate = F.silu(self.experts_gate[i](x))
            up = self.experts_up[i](x)
            out = self.experts_down[i](gate * up)
            expert_outputs.append(out)

        # Weighted sum
        expert_outputs = torch.stack(expert_outputs, dim=-1)  # [B, N, D, E]
        output = torch.einsum("bnde,bne->bnd", expert_outputs, router_weights)

        return output


class StandardMLP(nn.Module):
    """Standard SwiGLU MLP (baseline)."""

    def __init__(self, hidden_size: int, intermediate_size: int):
        super().__init__()
        self.gate_proj = nn.Linear(hidden_size, intermediate_size, bias=False)
        self.up_proj = nn.Linear(hidden_size, intermediate_size, bias=False)
        self.down_proj = nn.Linear(intermediate_size, hidden_size, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
