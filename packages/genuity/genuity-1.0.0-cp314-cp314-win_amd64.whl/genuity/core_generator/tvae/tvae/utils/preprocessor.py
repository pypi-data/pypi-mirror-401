"""
Internal preprocessor for TVAE that handles raw data preprocessing.
Based on TVAE paper requirements: MinMaxScaler for continuous, OneHotEncoder for categorical.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from typing import List, Union, Tuple, Optional


class TVAEPreprocessor:
    """
    TVAE-specific preprocessor that handles raw tabular data.

    According to TVAE paper:
    - Continuous features: MinMaxScaler (normalize to [0, 1])
    - Categorical features: OneHotEncoder
    - Missing values: handled by sklearn transformers
    """

    def __init__(self, continuous_cols: Optional[List[Union[str, int]]] = None,
                 categorical_cols: Optional[List[Union[str, int]]] = None,
                 handle_missing: str = 'mean'):
        """
        Args:
            continuous_cols: List of column names/indices for continuous features
            categorical_cols: List of column names/indices for categorical features
            handle_missing: How to handle missing values ('mean', 'median', 'most_frequent', 'drop')
        """
        self.continuous_cols = continuous_cols
        self.categorical_cols = categorical_cols
        self.handle_missing = handle_missing

        # Transformers
        self.continuous_scaler = None
        self.categorical_encoder = None

        # Metadata
        self.feature_names_ = None
        self.continuous_cols_ = None
        self.categorical_cols_ = None
        self.n_continuous_ = 0
        self.n_categorical_ = 0
        self.categorical_cardinalities_ = []
        self.column_order_ = None

        # For inverse transform
        self.continuous_indices_ = None
        self.categorical_indices_ = None

    def _detect_column_types(self, df: pd.DataFrame):
        """Auto-detect continuous vs categorical columns if not specified."""
        if self.continuous_cols is None and self.categorical_cols is None:
            # Auto-detect: numeric = continuous, object/string = categorical
            self.continuous_cols_ = []
            self.categorical_cols_ = []

            for col in df.columns:
                if df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
                    # Check if it's actually categorical (low cardinality)
                    unique_vals = df[col].nunique()
                    if unique_vals <= 20 and df[col].dtype == 'int64':
                        self.categorical_cols_.append(col)
                    else:
                        self.continuous_cols_.append(col)
                else:
                    self.categorical_cols_.append(col)
        else:
            # Use provided columns
            if isinstance(df, pd.DataFrame):
                self.continuous_cols_ = [col for col in self.continuous_cols if col in df.columns] if self.continuous_cols else []
                self.categorical_cols_ = [col for col in self.categorical_cols if col in df.columns] if self.categorical_cols else []
            else:
                # NumPy array - use indices
                self.continuous_cols_ = self.continuous_cols if self.continuous_cols else []
                self.categorical_cols_ = self.categorical_cols if self.categorical_cols else []

    def fit(self, data: Union[pd.DataFrame, np.ndarray]):
        """Fit the preprocessor on raw data."""
        if isinstance(data, pd.DataFrame):
            df = data.copy()
            self.feature_names_ = df.columns.tolist()
        else:
            # Convert numpy to DataFrame for easier handling
            df = pd.DataFrame(data)
            self.feature_names_ = [f'col_{i}' for i in range(data.shape[1])]

        # Detect column types if not provided
        self._detect_column_types(df)

        # Handle missing values
        if df.isnull().any().any():
            if self.handle_missing == 'drop':
                df = df.dropna()
            elif self.handle_missing == 'mean':
                df = df.fillna(df.select_dtypes(include=[np.number]).mean())
            elif self.handle_missing == 'median':
                df = df.fillna(df.select_dtypes(include=[np.number]).median())
            elif self.handle_missing == 'most_frequent':
                for col in df.columns:
                    df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 0, inplace=True)

        # Fit continuous scaler
        if self.continuous_cols_:
            cont_data = df[self.continuous_cols_].values.astype(np.float32)
            self.continuous_scaler = MinMaxScaler(feature_range=(0, 1))
            self.continuous_scaler.fit(cont_data)
            self.n_continuous_ = len(self.continuous_cols_)
        else:
            self.n_continuous_ = 0

        # Fit categorical encoder
        if self.categorical_cols_:
            cat_data = df[self.categorical_cols_].values.astype(str)
            # Use sparse_output for newer sklearn versions, fallback to sparse for older
            try:
                self.categorical_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop=None)
            except TypeError:
                self.categorical_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore', drop=None)
            self.categorical_encoder.fit(cat_data)

            # Get cardinalities
            self.categorical_cardinalities_ = [
                len(cats) for cats in self.categorical_encoder.categories_
            ]
            self.n_categorical_ = sum(self.categorical_cardinalities_)
        else:
            self.n_categorical_ = 0
            self.categorical_cardinalities_ = []

        # Store column order for inverse transform
        self.column_order_ = self.continuous_cols_ + self.categorical_cols_

        return self

    def transform(self, data: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Transform raw data to preprocessed format."""
        if isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            df = pd.DataFrame(data, columns=self.feature_names_ if self.feature_names_ else None)

        # Handle missing values
        if df.isnull().any().any():
            if self.handle_missing == 'drop':
                df = df.dropna()
            elif self.handle_missing == 'mean':
                df = df.fillna(df.select_dtypes(include=[np.number]).mean())
            elif self.handle_missing == 'median':
                df = df.fillna(df.select_dtypes(include=[np.number]).median())
            elif self.handle_missing == 'most_frequent':
                for col in df.columns:
                    df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 0, inplace=True)

        transformed_parts = []

        # Transform continuous
        if self.n_continuous_ > 0:
            cont_data = df[self.continuous_cols_].values.astype(np.float32)
            cont_transformed = self.continuous_scaler.transform(cont_data)
            transformed_parts.append(cont_transformed)

        # Transform categorical
        if self.n_categorical_ > 0:
            cat_data = df[self.categorical_cols_].values.astype(str)
            cat_transformed = self.categorical_encoder.transform(cat_data)
            transformed_parts.append(cat_transformed)

        if transformed_parts:
            return np.concatenate(transformed_parts, axis=1).astype(np.float32)
        else:
            return np.zeros((len(df), 0), dtype=np.float32)

    def inverse_transform(self, transformed_data: np.ndarray) -> pd.DataFrame:
        """Inverse transform preprocessed data back to raw format."""
        n_samples = transformed_data.shape[0]

        # Split continuous and categorical parts
        cont_part = transformed_data[:, :self.n_continuous_] if self.n_continuous_ > 0 else np.array([]).reshape(n_samples, 0)
        cat_part = transformed_data[:, self.n_continuous_:] if self.n_categorical_ > 0 else np.array([]).reshape(n_samples, 0)

        result_parts = {}

        # Inverse transform continuous
        if self.n_continuous_ > 0:
            cont_inverse = self.continuous_scaler.inverse_transform(cont_part)
            for i, col in enumerate(self.continuous_cols_):
                result_parts[col] = cont_inverse[:, i]

        # Inverse transform categorical
        if self.n_categorical_ > 0:
            # OneHotEncoder.inverse_transform expects the full one-hot matrix
            # So we pass the one-hot encoded part directly
            cat_inverse = self.categorical_encoder.inverse_transform(cat_part)

            # Handle case where inverse_transform returns 2D array (multiple columns)
            if cat_inverse.ndim == 2:
                for i, col in enumerate(self.categorical_cols_):
                    result_parts[col] = cat_inverse[:, i]
            else:
                # Single categorical column
                result_parts[self.categorical_cols_[0]] = cat_inverse

        # Create DataFrame in original column order
        result_df = pd.DataFrame(result_parts)

        # Reorder columns to match original order
        if self.column_order_:
            result_df = result_df[self.column_order_]

        return result_df

    def get_output_info(self) -> List[dict]:
        """Get output info for decoder structure (compatible with existing API)."""
        output_info = []

        # Continuous features
        for i in range(self.n_continuous_):
            output_info.append({
                'type': 'continuous',
                'dim': 1,
                'activation': None
            })

        # Categorical features
        for cardinality in self.categorical_cardinalities_:
            output_info.append({
                'type': 'categorical',
                'dim': cardinality,
                'activation': 'softmax',
                'num_categories': cardinality
            })

        return output_info

    def get_feature_dims(self) -> Tuple[int, int, List[int]]:
        """Get dimensions: (n_continuous, n_categorical_total, categorical_cardinalities)."""
        return self.n_continuous_, self.n_categorical_, self.categorical_cardinalities_
