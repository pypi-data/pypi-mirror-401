import numpy as np
import pandas as pd
import torch
import pickle
from .factory import TVAEFactory
from .preprocessor import TVAEPreprocessor


class TVAEAPI:
    """High-level API for TVAE synthetic tabular data generation (basic edition).

    According to TVAE paper, TVAE requires special preprocessing:
    - Continuous features: MinMaxScaler (normalize to [0, 1])
    - Categorical features: OneHotEncoder

    The API handles preprocessing internally and returns raw synthetic data.

    Supports two modes:
    1. Raw DataFrame mode (Recommended): Pass a pandas DataFrame to fit().
       The API handles preprocessing internally and returns DataFrame.
    2. NumPy/Legacy mode: Pass a numpy array and column indices.
       Uses internal preprocessing and returns numpy array.
    """

    def __init__(self, model_type: str = "basic"):
        # Only basic model is supported in the base package
        if model_type != "basic":
            raise ValueError(
                "This package provides only the basic TVAE. For advanced features, import tvae_premium and use TVAEAPI(model_type='premium')."
            )
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

    def fit(self, data, continuous_cols=None, categorical_cols=None, epochs=300, **kwargs):
        """Fit TVAE model to raw data.

        According to TVAE paper, preprocessing is handled internally:
        - Continuous: MinMaxScaler to [0, 1]
        - Categorical: OneHotEncoder

        Args:
            data: pd.DataFrame or np.ndarray (raw data, not preprocessed)
            continuous_cols: List of column names/indices (optional, auto-detected if None)
            categorical_cols: List of column names/indices (optional, auto-detected if None)
            epochs: Number of training epochs
            **kwargs: Additional args (verbose, batch_size, etc)
        """
        verbose = kwargs.get("verbose", True)

        # --- Mode 1: DataFrame (Internal TVAE Preprocessing) ---
        if isinstance(data, pd.DataFrame):
            if verbose:
                print("TVAE: DataFrame detected. Using internal TVAE preprocessor (MinMaxScaler + OneHotEncoder).")

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

            # Initialize Trainer
            self.trainer = TVAEFactory.create_basic_model(
                continuous_dims=list(range(n_continuous)) if n_continuous > 0 else [],
                categorical_dims=categorical_cardinalities
            )

            # Update batch size if provided
            if 'batch_size' in kwargs:
                self.trainer.config.batch_size = kwargs['batch_size']

            # Fit Trainer
            losses = self.trainer.fit(
                processed_data,
                epochs=epochs,
                verbose=verbose,
                output_info=output_info
            )
            self.is_fitted = True
            return losses

        # --- Mode 2: NumPy / Legacy ---
        else:
            if verbose:
                print("TVAE: NumPy array detected. Using internal TVAE preprocessor.")

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

            # Initialize Trainer
            self.trainer = TVAEFactory.create_basic_model(
                continuous_dims=list(range(n_continuous)) if n_continuous > 0 else [],
                categorical_dims=categorical_cardinalities
            )

            # Update batch size if provided
            if 'batch_size' in kwargs:
                self.trainer.config.batch_size = kwargs['batch_size']

            losses = self.trainer.fit(
                processed_data, epochs=epochs, verbose=verbose, output_info=output_info
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
            # Convert to DataFrame for inverse transform
            df_preprocessed = pd.DataFrame(preprocessed_samples)
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
            categorical_cardinalities = checkpoint.get("cardinalities", [])

        # Create trainer if needed
        if self.trainer is None:
            self.trainer = TVAEFactory.create_basic_model(
                continuous_dims=continuous_dims,
                categorical_dims=categorical_cardinalities
            )

        # Load model weights
        self.trainer.load_model(filepath)

        # Restore metadata
        if 'preprocessor' in checkpoint:
            self.preprocessor = checkpoint['preprocessor']
            # Restore output info to trainer for generation
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
