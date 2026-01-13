"""
INL Dynamics - Robotics-grade control with velocity tracking.

Equations:
    error = h - mu                      # deviation from equilibrium
    v_next = alpha * v - beta * error   # velocity update
    h_next = h + dt * gate * v_next     # position update
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple


class INLDynamics(nn.Module):
    """
    Full INL Dynamics with velocity tracking.
    """

    def __init__(
        self,
        hidden_size: int,
        dt: float = 0.1,
        controller_hidden: int = 64,
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.dt = dt

        # Learnable equilibrium
        self.mu = nn.Parameter(torch.zeros(hidden_size))

        # Controller MLP: [h, v] -> [alpha, beta, gate]
        self.controller = nn.Sequential(
            nn.Linear(hidden_size * 2, controller_hidden),
            nn.SiLU(),
            nn.Linear(controller_hidden, hidden_size * 3),
        )

        # Initialize for stable dynamics
        self._init_controller()

    def _init_controller(self):
        with torch.no_grad():
            bias = self.controller[-1].bias
            # alpha ~ 0.9 (high inertia)
            bias[:self.hidden_size].fill_(2.2)
            # beta ~ 0.1 (low correction)
            bias[self.hidden_size:self.hidden_size*2].fill_(-2.2)
            # gate ~ 0.5 (medium amplitude)
            bias[self.hidden_size*2:].fill_(0.0)
            # Small weights
            self.controller[-1].weight.normal_(0, 0.01)

    def forward(
        self,
        h: torch.Tensor,
        v: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Apply dynamics update.

        Args:
            h: Hidden states [B, N, D]
            v: Velocity states [B, N, D] (None = zeros)

        Returns:
            h_next, v_next
        """
        if v is None:
            v = torch.zeros_like(h)

        # Controller
        ctx = torch.cat([h, v], dim=-1)
        out = self.controller(ctx)

        alpha_raw, beta_raw, gate_raw = torch.split(out, self.hidden_size, dim=-1)
        alpha = torch.sigmoid(alpha_raw)
        beta = F.softplus(beta_raw)
        gate = torch.sigmoid(gate_raw)

        # Dynamics
        error = h - self.mu
        v_next = alpha * v - beta * error
        h_next = h + self.dt * gate * v_next

        return h_next, v_next
