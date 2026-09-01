import torch
from torch import nn

class NeuroForgeConfig:
    def __init__(self, vocab_size=32000, hidden_size=768, layers=16, heads=12, intermediate=2048):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.layers = layers
        self.heads = heads
        self.intermediate = intermediate

class NeuroForgeNetwork(nn.Module):
    """Decoder-style neural network scaffold for the ~100-150M parameter target."""
    def __init__(self, cfg: NeuroForgeConfig):
        super().__init__()
        self.embed = nn.Embedding(cfg.vocab_size, cfg.hidden_size)
        block = nn.TransformerEncoderLayer(
            d_model=cfg.hidden_size,
            nhead=cfg.heads,
            dim_feedforward=cfg.intermediate,
            batch_first=True,
            norm_first=True,
            activation="gelu",
        )
        self.blocks = nn.TransformerEncoder(block, num_layers=cfg.layers)
        self.norm = nn.LayerNorm(cfg.hidden_size)
        self.lm_head = nn.Linear(cfg.hidden_size, cfg.vocab_size, bias=False)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        x = self.embed(input_ids)
        x = self.blocks(x)
        return self.lm_head(self.norm(x))


def count_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())
