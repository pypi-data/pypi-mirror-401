import numpy as np
from typing import List, Dict
from .factory import CTGANPremiumFactory


class CTGANPremiumAPI:
    """High-level API for premium CTGAN synthetic tabular data generation"""

    def __init__(self, model_type: str = "premium"):
        self.model_type = model_type
        self.trainer = None
        self.is_fitted = False

    def fit(
        self,
        data: np.ndarray,
        continuous_cols: list,
        categorical_cols: list,
        epochs: int = 1000,
        **kwargs,
    ) -> dict:
        """
        Fit the premium CTGAN model to data.
        
        Args:
            data: Input array (n_samples, n_features)
            continuous_cols: List of column indices that are continuous
            categorical_cols: List of column indices that are one-hot categorical
            epochs: Number of training epochs
        """
        n_samples, n_features = data.shape
        n_cont = len(continuous_cols)
        n_cat = len(categorical_cols)
        
        # Validate
        if n_cont + n_cat != n_features:
            raise ValueError(
                f"continuous_cols ({n_cont}) + categorical_cols ({n_cat}) "
                f"must equal number of features ({n_features})"
            )

        verbose = kwargs.pop("verbose", True)
        output_info = kwargs.pop("output_info", None)

        # Create model with actual dimensions
        if self.model_type == "basic":
            self.trainer = CTGANPremiumFactory.create_basic_model(
                continuous_dims=continuous_cols,
                categorical_dims=categorical_cols,
                n_continuous=n_cont,
                n_categorical=n_cat,
            )
        elif self.model_type == "premium":
            premium_features = kwargs.get("premium_features", None)
            # Remove premium_features from kwargs to avoid double passing if needed, 
            # though factory might handle it. better to be clean.
            if "premium_features" in kwargs:
                del kwargs["premium_features"]
                
            self.trainer = CTGANPremiumFactory.create_premium_model(
                continuous_cols, categorical_cols, premium_features,
                n_continuous=n_cont, n_categorical=n_cat,
                **kwargs
            )
        elif self.model_type == "enterprise":
            self.trainer = CTGANPremiumFactory.create_enterprise_model(
                continuous_cols, categorical_cols,
                n_continuous=n_cont, n_categorical=n_cat,
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        losses = self.trainer.fit(data, epochs=epochs, verbose=verbose, output_info=output_info)
        self.is_fitted = True

        return losses

    def generate(self, n_samples: int) -> np.ndarray:
        """Generate synthetic samples"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")

        return self.trainer.generate(n_samples)

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")

        return self.trainer.get_feature_importance()

    def save(self, filepath: str):
        """Save the model"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")

        self.trainer.save_model(filepath)

    def load(self, filepath: str):
        """Load a saved model"""
        if self.trainer is None:
            import torch

            checkpoint = torch.load(filepath, map_location="cpu")
            config = checkpoint.get("config")
            if config is None:
                raise ValueError("Cannot load model: config not found in saved file")

            if self.model_type == "basic":
                self.trainer = CTGANPremiumFactory.create_basic_model(
                    continuous_dims=config.continuous_dims,
                    categorical_dims=config.categorical_dims,
                    n_continuous=config.n_continuous,
                    n_categorical=config.n_categorical,
                )
            elif self.model_type == "premium":
                self.trainer = CTGANPremiumFactory.create_premium_model(
                    config.continuous_dims, config.categorical_dims, None,
                    n_continuous=config.n_continuous, n_categorical=config.n_categorical,
                )
            elif self.model_type == "enterprise":
                self.trainer = CTGANPremiumFactory.create_enterprise_model(
                    config.continuous_dims, config.categorical_dims,
                    n_continuous=config.n_continuous, n_categorical=config.n_categorical,
                )
            else:
                raise ValueError(f"Unknown model type: {self.model_type}")

        self.trainer.load_model(filepath)
        self.is_fitted = True
