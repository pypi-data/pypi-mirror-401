"""
High-level API for TVAE Premium
"""
import numpy as np
import pandas as pd
from .factory import TVAEFactory
from ...tvae.utils.preprocessor import TVAEPreprocessor


class TVAEPremiumAPI:
    """High-level API for TVAE synthetic tabular data generation (premium edition).

    Includes all basic functionality plus 4 premium features:
    1. VampPrior - Better prior distribution
    2. Cyclical KL Annealing - Better training stability
    3. Multi-head Decoder - Better reconstruction for mixed data
    4. Quality Gating - Filter low-quality samples

    When premium features are disabled, works exactly like basic TVAE.
    """

    def __init__(self, model_type: str = "premium"):
        self.model_type = model_type
        self.trainer = None
        self.is_fitted = False

        # Internal TVAE preprocessor (handles raw data)
        self.preprocessor = None

        # Metadata
        self.continuous_cols = None
        self.categorical_cols = None
        self.is_dataframe_mode = False
        self.original_columns = None

    def fit(
        self,
        data,
        continuous_cols=None,
        categorical_cols=None,
        epochs: int = 300,
        config=None,
        verbose: bool = True,  # Default to True for tqdm progress bars
        **kwargs,
    ) -> dict:
        """Fit TVAE Premium model to raw data.

        Args:
            data: pd.DataFrame or np.ndarray (raw data, not preprocessed)
            continuous_cols: List of column names/indices (optional, auto-detected if None)
            categorical_cols: List of column names/indices (optional, auto-detected if None)
            epochs: Number of training epochs
            config: TVAEConfig object (optional, uses defaults if None)
            verbose: Show progress bars (default: True)
            **kwargs: Additional args (batch_size, premium_features, etc)
        """
        # verbose is now a direct parameter with default True

        # --- Mode 1: DataFrame (Internal TVAE Preprocessing) ---
        if isinstance(data, pd.DataFrame):
            if verbose:
                print("TVAE Premium: DataFrame detected. Using internal TVAE preprocessor.")

            self.is_dataframe_mode = True
            self.original_columns = data.columns.tolist()

            # Initialize TVAE preprocessor
            self.preprocessor = TVAEPreprocessor(
                continuous_cols=continuous_cols,
                categorical_cols=categorical_cols
            )

            # Fit and transform
            self.preprocessor.fit(data)
            processed_data = self.preprocessor.transform(data)

            # Get dimensions
            n_continuous, n_categorical_total, categorical_cardinalities = \
                self.preprocessor.get_feature_dims()

            # Store column info
            self.continuous_cols = self.preprocessor.continuous_cols_
            self.categorical_cols = self.preprocessor.categorical_cols_

            # Get output info for decoder
            output_info = self.preprocessor.get_output_info()

        # --- Mode 2: NumPy / Legacy ---
        else:
            if verbose:
                print("TVAE Premium: NumPy array detected. Using internal TVAE preprocessor.")

            self.is_dataframe_mode = False

            # Convert to DataFrame for preprocessing
            df = pd.DataFrame(data)

            # Initialize TVAE preprocessor
            self.preprocessor = TVAEPreprocessor(
                continuous_cols=continuous_cols,
                categorical_cols=categorical_cols
            )

            # Fit and transform
            self.preprocessor.fit(df)
            processed_data = self.preprocessor.transform(df)

            # Get dimensions
            n_continuous, n_categorical_total, categorical_cardinalities = \
                self.preprocessor.get_feature_dims()

            # Store column info
            self.continuous_cols = continuous_cols if continuous_cols else list(range(n_continuous))
            self.categorical_cols = categorical_cols if categorical_cols else []

            # Get output info
            output_info = self.preprocessor.get_output_info()

        # Create trainer with config
        if config is None:
            from ..config.config import TVAEConfig
            config = TVAEConfig(
                continuous_dims=list(range(n_continuous)) if n_continuous > 0 else [],
                categorical_dims=categorical_cardinalities
            )

            # Apply premium features from kwargs if provided
            premium_features = kwargs.get("premium_features", {})
            if premium_features:
                for k, v in premium_features.items():
                    if hasattr(config, k):
                        setattr(config, k, v)

        # Update batch size if provided
        if 'batch_size' in kwargs:
            config.batch_size = kwargs['batch_size']

        # Create trainer
        self.trainer = TVAEFactory.create_premium_model(
            continuous_dims=list(range(n_continuous)) if n_continuous > 0 else [],
            categorical_dims=categorical_cardinalities,
            config=config
        )

        # Fit Trainer
        losses = self.trainer.fit(
            processed_data,
            epochs=epochs,
            verbose=verbose,
            output_info=output_info
        )

        self.is_fitted = True
        return losses

    def generate(self, n_samples: int):
        """Generate synthetic samples in raw format (same as input).

        Returns:
            pd.DataFrame if input was DataFrame, np.ndarray if input was numpy array
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")

        # Generate preprocessed samples (one-hot encoded)
        preprocessed_samples = self.trainer.generate(n_samples)

        # Inverse transform to raw format
        if self.preprocessor:
            raw_data = self.preprocessor.inverse_transform(preprocessed_samples)

            # Return in same format as input
            if self.is_dataframe_mode:
                return raw_data
            else:
                return raw_data.values
        else:
            # Fallback (should not happen if preprocessor was used)
            return preprocessed_samples

    def get_feature_importance(self):
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")
        return self.trainer.get_feature_importance()

    def save(self, filepath: str):
        """Save the model with all metadata"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")

        metadata = {
            "preprocessor": self.preprocessor,
            "continuous_cols": self.continuous_cols,
            "categorical_cols": self.categorical_cols,
            "is_dataframe_mode": self.is_dataframe_mode,
            "original_columns": self.original_columns
        }
        self.trainer.save_model(filepath, **metadata)

    def load(self, filepath: str):
        """Load a saved model and restore metadata"""
        import torch
        import os

        # Load checkpoint to get dimensions
        try:
            checkpoint = torch.load(filepath, map_location="cpu", weights_only=False)
        except (TypeError, AttributeError):
            checkpoint = torch.load(filepath, map_location="cpu")

        # Determine dimensions from preprocessor
        if checkpoint.get('preprocessor') is not None:
            pre = checkpoint['preprocessor']
            n_continuous, n_categorical_total, categorical_cardinalities = pre.get_feature_dims()
            continuous_dims = list(range(n_continuous)) if n_continuous > 0 else []
        else:
            # Fallback
            continuous_dims = list(range(len(checkpoint.get("continuous_cols", []))))
            categorical_cardinalities = checkpoint.get("categorical_dims", [])

        # Create trainer if needed
        if self.trainer is None:
            from ..config.config import TVAEConfig
            config = TVAEConfig(
                continuous_dims=continuous_dims,
                categorical_dims=categorical_cardinalities
            )
            self.trainer = TVAEFactory.create_premium_model(
                continuous_dims=continuous_dims,
                categorical_dims=categorical_cardinalities,
                config=config
            )

        # Load model weights
        self.trainer.load_model(filepath)

        # Restore metadata
        if 'preprocessor' in checkpoint:
            self.preprocessor = checkpoint['preprocessor']
            if self.trainer and self.preprocessor:
                self.trainer.output_info = self.preprocessor.get_output_info()

        if 'continuous_cols' in checkpoint:
            self.continuous_cols = checkpoint['continuous_cols']
        if 'categorical_cols' in checkpoint:
            self.categorical_cols = checkpoint['categorical_cols']
        if 'is_dataframe_mode' in checkpoint:
            self.is_dataframe_mode = checkpoint['is_dataframe_mode']
        if 'original_columns' in checkpoint:
            self.original_columns = checkpoint['original_columns']

        self.is_fitted = True
