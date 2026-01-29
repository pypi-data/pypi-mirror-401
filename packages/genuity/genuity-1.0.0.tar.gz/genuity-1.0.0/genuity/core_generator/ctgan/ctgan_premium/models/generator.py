import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List
from ..config.config import CTGANPremiumConfig


class ResidualBlock(nn.Module):
    """Improved residual block with better gradient flow"""

    def __init__(self, dim_in: int, dim_out: int, use_spectral_norm: bool = True):
        super().__init__()

        if use_spectral_norm:
            self.fc1 = nn.utils.spectral_norm(nn.Linear(dim_in, dim_out))
            self.fc2 = nn.utils.spectral_norm(nn.Linear(dim_out, dim_out))
        else:
            self.fc1 = nn.Linear(dim_in, dim_out)
            self.fc2 = nn.Linear(dim_out, dim_out)

        self.ln1 = nn.LayerNorm(dim_out)
        self.ln2 = nn.LayerNorm(dim_out)
        self.act = nn.LeakyReLU(0.2, inplace=True)
        self.dropout = nn.Dropout(0.1)

        if dim_in != dim_out:
            if use_spectral_norm:
                self.skip = nn.utils.spectral_norm(nn.Linear(dim_in, dim_out))
            else:
                self.skip = nn.Linear(dim_in, dim_out)
        else:
            self.skip = nn.Identity()

    def forward(self, x):
        residual = self.skip(x)
        out = self.fc1(x)
        out = self.ln1(out)
        out = self.act(out)
        out = self.dropout(out)
        out = self.fc2(out)
        out = self.ln2(out)
        return self.act(out + residual)


class CTGANPremiumGenerator(nn.Module):
    """CTGAN generator with correct output dimensions"""

    def __init__(self, config: CTGANPremiumConfig, output_info: List[dict] = None):
        super().__init__()
        self.config = config
        self.latent_dim = config.latent_dim
        self.hidden_dim = config.hidden_dim
        
        # Store metadata for correct activation
        self.output_info = output_info if output_info is not None else []

        # Use actual counts from config
        self.n_continuous = config.n_continuous
        self.n_categorical = config.n_categorical
        self.output_dim = config.output_dim  # total columns to generate

        # Conditional information
        # Sum of all categorical dimensions
        # This assumes config.n_categorical is the total one-hot count
        self.cond_dim = config.n_categorical 
        
        # Core network
        blocks = []
        # Input is Latent + Condition
        in_dim = self.latent_dim + self.cond_dim

        for i in range(config.num_layers):
            blocks.append(
                ResidualBlock(in_dim, self.hidden_dim, use_spectral_norm=config.use_spectral_norm)
            )
            in_dim = self.hidden_dim

        self.core = nn.Sequential(*blocks)

        # Output layer - produces exact number of columns as input
        if config.use_spectral_norm:
            self.output_layer = nn.utils.spectral_norm(
                nn.Linear(self.hidden_dim, self.output_dim)
            )
        else:
            self.output_layer = nn.Linear(self.hidden_dim, self.output_dim)

    def forward(self, z: torch.Tensor, cond: torch.Tensor = None, hard_categorical: bool = False) -> torch.Tensor:
        """
        Generate synthetic data from latent vector + condition.
        Uses Gumbel-Softmax for categorical (training) or Softmax (inference).
        """
        # Concatenate z and cond
        if cond is not None:
             inp = torch.cat([z, cond], dim=1)
        else:
             if self.cond_dim > 0:
                 cond = torch.zeros(z.size(0), self.cond_dim, device=z.device)
                 inp = torch.cat([z, cond], dim=1)
             else:
                 inp = z

        x = self.core(inp)
        output = self.output_layer(x)

        # Split output into continuous and categorical parts
        # If output_info is missing, we fall back to the old split
        # but output_info is REQUIRED for correct Softmax grouping
        
        if not self.output_info:
            # Fallback (Incorrect strictly speaking, but safe for un-configured usage)
            continuous_part = output[:, :self.n_continuous]
            categorical_part = output[:, self.n_continuous:]
            continuous_part = torch.sigmoid(continuous_part)
            categorical_part = torch.sigmoid(categorical_part) # WRONG but fallback
            return torch.cat([continuous_part, categorical_part], dim=1)

        # 1. Continuous Part (Always at the start)
        continuous_part = output[:, :self.n_continuous]
        continuous_part = torch.sigmoid(continuous_part)
        
        # 2. Categorical Parts (Iterate over spans)
        # The generator output for categoricals starts at index n_continuous
        
        categorical_tensors = []
        current_idx = self.n_continuous
        
        for info in self.output_info:
            n_cats = info['num_categories']
            logits = output[:, current_idx : current_idx + n_cats]
            
            if self.training:
                # Gumbel Softmax for differentiable sampling during training
                # This allows gradient to flow from Discriminator through the discrete choice
                activated = F.gumbel_softmax(logits, tau=self.config.gumbel_tau, hard=False)
            else:
                # Standard Softmax for Inference
                probs = F.softmax(logits, dim=1)
                if hard_categorical:
                    # One-hot encoding
                    idx = torch.argmax(probs, dim=1)
                    activated = F.one_hot(idx, num_classes=n_cats).float()
                else:
                    activated = probs
            
            categorical_tensors.append(activated)
            current_idx += n_cats
            
        categorical_part = torch.cat(categorical_tensors, dim=1)

        # Concatenate back
        return torch.cat([continuous_part, categorical_part], dim=1)
