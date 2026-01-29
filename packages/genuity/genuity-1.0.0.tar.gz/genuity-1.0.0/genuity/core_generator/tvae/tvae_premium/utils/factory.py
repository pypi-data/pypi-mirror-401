"""
Factory for TVAE Premium - creates premium trainer with optional features
"""
import numpy as np


class TVAEFactory:
    """Factory to create TVAE trainer instances"""

    @staticmethod
    def create_basic_model(continuous_dims, categorical_dims):
        """Create basic TVAE trainer (uses basic implementation)"""
        from ...tvae.tvae.trainers.trainer import TVAETrainer
        from ...tvae.tvae.config.config import TVAEConfig

        config = TVAEConfig(
            continuous_dims=continuous_dims,
            categorical_dims=categorical_dims
        )
        return TVAETrainer(config)

    @staticmethod
    def create_premium_model(continuous_dims, categorical_dims, config=None, premium_features=None):
        """Create premium TVAE trainer with enhanced features.

        Args:
            continuous_dims: List of continuous dimension indices
            categorical_dims: List of categorical cardinalities
            config: TVAEConfig object (optional)
            premium_features: Dict of premium feature flags (optional)
        """
        from ..trainers.trainer import TVAEPremiumTrainer
        from ..config.config import TVAEConfig

        # Create config if not provided
        if config is None:
            config = TVAEConfig(
                continuous_dims=continuous_dims,
                categorical_dims=categorical_dims
            )

        # Apply premium features to config if provided
        if premium_features:
            for k, v in premium_features.items():
                if hasattr(config, k):
                    setattr(config, k, v)

        # Ensure config has correct dimensions
        config.continuous_dims = continuous_dims
        config.categorical_dims = categorical_dims

        trainer = TVAEPremiumTrainer(config)
        return trainer

    @staticmethod
    def create_enterprise_model(continuous_dims, categorical_dims):
        """Create enterprise TVAE trainer (same as premium with all features enabled)"""
        from ..trainers.trainer import TVAEPremiumTrainer
        from ..config.config import TVAEConfig

        config = TVAEConfig(
            continuous_dims=continuous_dims,
            categorical_dims=categorical_dims,
            # Enable all premium features for enterprise
            use_vampprior=True,
            use_cyclical_kl=True,
            use_multi_head_decoder=True,
            use_quality_gating=True
        )
        return TVAEPremiumTrainer(config)
