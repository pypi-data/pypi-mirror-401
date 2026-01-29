from dataclasses import dataclass, field
from typing import List


@dataclass
class CTGANConfig:
    """Configuration for the basic CTGAN model with improved accuracy settings"""

    # Core architecture settings
    latent_dim: int = 256
    hidden_dim: int = 512
    discriminator_hidden_dim: int = 512
    num_layers: int = 4

    # Training settings
    learning_rate: float = 2e-4
    batch_size: int = 500
    discriminator_dropout: float = 0.0

    # Feature dimensions - these are the ACTUAL counts, not index lists
    n_continuous: int = 0  # Number of continuous columns in input
    n_categorical: int = 0  # Number of one-hot categorical columns in input
    
    # Legacy fields for compatibility (indices within the data)
    continuous_dims: List[int] = field(default_factory=list)
    categorical_dims: List[int] = field(default_factory=list)

    # Training stability
    use_spectral_norm: bool = True
    use_gradient_penalty: bool = True
    gradient_penalty_weight: float = 10.0

    # Loss balancing
    generator_loss_weight: float = 1.0
    discriminator_loss_weight: float = 1.0
    
    # Advanced Loss Weights
    diversity_loss_weight: float = 0.1
    conditional_loss_weight: float = 1.0
    
    # Gumbel Softmax
    gumbel_tau: float = 0.2
    
    @property
    def output_dim(self) -> int:
        """Total output dimension = continuous + categorical one-hot columns"""
        return self.n_continuous + self.n_categorical

    def __post_init__(self):
        if self.continuous_dims is None:
            self.continuous_dims = []
        if self.categorical_dims is None:
            self.categorical_dims = []
