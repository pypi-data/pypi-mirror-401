from typing import List, Optional
from ..config.config import CTGANPremiumConfig
from ..trainers.trainer import CTGANPremiumTrainer


class CTGANPremiumFactory:
    """Factory for creating premium CTGAN models"""

    @staticmethod
    def create_basic_model(
        continuous_dims: List[int],
        categorical_dims: List[int],
        n_continuous: int = 0,
        n_categorical: int = 0,
        **kwargs
    ) -> CTGANPremiumTrainer:
        """Create basic CTGAN model (no premium features)"""
        config = CTGANPremiumConfig(
            continuous_dims=continuous_dims,
            categorical_dims=categorical_dims,
            n_continuous=n_continuous,
            n_categorical=n_categorical,
            **kwargs
        )
        return CTGANPremiumTrainer(config)

    @staticmethod
    def create_premium_model(
        continuous_dims: List[int],
        categorical_dims: List[int],
        premium_features: List[str] = None,
        n_continuous: int = 0,
        n_categorical: int = 0,
        config: Optional[CTGANPremiumConfig] = None,
        **kwargs
    ) -> CTGANPremiumTrainer:
        """Create CTGAN model with selected premium features"""
        if config is None:
            config = CTGANPremiumConfig(
                continuous_dims=continuous_dims,
                categorical_dims=categorical_dims,
                n_continuous=n_continuous,
                n_categorical=n_categorical,
                **kwargs
            )

        if premium_features is None:
            # Enable default premium features (PacGAN only as architectural feature, others are weights)
            premium_features = ["pacgan"]

        for feature in premium_features:
            if hasattr(config, f"use_{feature}"):
                setattr(config, f"use_{feature}", True)
        
        # Ensure premium loss weights are set if not provided in kwargs
        if config.diversity_loss_weight == 0.0:
            config.diversity_loss_weight = 0.1
        if config.correlation_loss_weight == 0.0:
            config.correlation_loss_weight = 0.5

        return CTGANPremiumTrainer(config)

    @staticmethod
    def create_enterprise_model(
        continuous_dims: List[int],
        categorical_dims: List[int],
        n_continuous: int = 0,
        n_categorical: int = 0,
        **kwargs
    ) -> CTGANPremiumTrainer:
        """Create enterprise-grade model with all features"""
        config = CTGANPremiumConfig(
            continuous_dims=continuous_dims,
            categorical_dims=categorical_dims,
            n_continuous=n_continuous,
            n_categorical=n_categorical,
            latent_dim=256,
            hidden_dim=512,
            num_layers=4,
            learning_rate=1e-4,
            batch_size=128,
            # Enterprise defaults: Stronger regularization and packing
            use_pacgan=True,
            diversity_loss_weight=0.2,
            correlation_loss_weight=0.8,
            **kwargs
        )

        return CTGANPremiumTrainer(config)
