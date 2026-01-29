import numpy as np
from typing import List, Dict
from .factory import CTGANFactory


class CTGANAPI:
    """High-level API for CTGAN synthetic tabular data generation"""

    def __init__(self):
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
        Fit the CTGAN model to data.
        
        Args:
            data: Input data array (n_samples, n_features)
            continuous_cols: List of column INDICES that are continuous
            categorical_cols: List of column INDICES that are one-hot categorical
            epochs: Number of training epochs
            **kwargs: Additional config parameters
        """
        # Get actual data shape
        n_samples, n_features = data.shape
        n_cont = len(continuous_cols)
        n_cat = len(categorical_cols)
        
        # Validate
        if n_cont + n_cat != n_features:
            raise ValueError(
                f"continuous_cols ({n_cont}) + categorical_cols ({n_cat}) "
                f"must equal number of features ({n_features})"
            )

        # Extract verbose parameter
        verbose = kwargs.pop("verbose", True)

        # Extract output_info if provided (for Conditional Sampling)
        output_info = kwargs.pop("output_info", None)

        # Create model with ACTUAL dimensions
        self.trainer = CTGANFactory.create_model(
            continuous_dims=continuous_cols,
            categorical_dims=categorical_cols,
            n_continuous=n_cont,
            n_categorical=n_cat,
            **kwargs,
        )

        # Fit the model
        losses = self.trainer.fit(data, epochs=epochs, verbose=verbose, output_info=output_info)
        self.is_fitted = True

        return losses

    def generate(self, n_samples: int) -> np.ndarray:
        """Generate synthetic samples"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")

        return self.trainer.generate(n_samples)

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

            self.trainer = CTGANFactory.create_model(
                continuous_dims=config.continuous_dims,
                categorical_dims=config.categorical_dims,
                n_continuous=config.n_continuous,
                n_categorical=config.n_categorical,
            )

        self.trainer.load_model(filepath)
        self.is_fitted = True
