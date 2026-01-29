from typing import List, Optional
from ..config.config import CTGANConfig
from ..trainers.trainer import CTGANTrainer


class CTGANFactory:
    """Factory for creating CTGAN models"""

    @staticmethod
    def create_model(
        continuous_dims: List[int],
        categorical_dims: List[int],
        n_continuous: int = 0,
        n_categorical: int = 0,
        config: Optional[CTGANConfig] = None,
        **kwargs
    ) -> CTGANTrainer:
        """Create CTGAN model with specified configuration"""
        if config is not None:
            return CTGANTrainer(config)
        else:
            config = CTGANConfig(
                continuous_dims=continuous_dims,
                categorical_dims=categorical_dims,
                n_continuous=n_continuous,
                n_categorical=n_categorical,
                **kwargs
            )
            return CTGANTrainer(config)
