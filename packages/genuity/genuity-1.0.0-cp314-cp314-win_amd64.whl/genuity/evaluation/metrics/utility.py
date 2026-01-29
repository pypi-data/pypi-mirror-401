"""
Utility Metrics for Synthetic Data Evaluation

This module contains all utility-related metrics:
- TSTR: Train on Synthetic, Test on Real
- TRTS: Train on Real, Test on Synthetic
- Prediction Agreement: Percent identical predictions
- Likelihood Leak: Log-likelihood gap between real and synthetic
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import warnings
from typing import Dict, List, Tuple, Optional, Union

warnings.filterwarnings("ignore")


class TSTRMetrics:
    """Train on Synthetic, Test on Real metrics."""

    def __init__(
        self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, target_column: str
    ):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.target_column = target_column
        self.feature_columns = [
            col for col in real_data.columns if col != target_column
        ]
        # Detect categorical columns
        self.categorical_columns = [
            col for col in self.feature_columns
            if real_data[col].dtype == 'object' or real_data[col].dtype == 'category'
            or len(real_data[col].unique()) < 10
        ]
        self.numerical_columns = [
            col for col in self.feature_columns if col not in self.categorical_columns
        ]

    def tstr_accuracy(self) -> float:
        """TSTR accuracy for classification tasks."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Check if it's a classification task
        target_values = self.real_data[self.target_column].dropna()
        if target_values.dtype == "object" or len(target_values.unique()) < 10:
            # Classification task
            X_synth = self.synthetic_data[self.feature_columns].dropna()
            y_synth = self.synthetic_data[self.target_column].dropna()
            X_real = self.real_data[self.feature_columns].dropna()
            y_real = self.real_data[self.target_column].dropna()

            # Align indices
            common_idx = X_synth.index.intersection(y_synth.index)
            X_synth = X_synth.loc[common_idx]
            y_synth = y_synth.loc[common_idx]

            common_idx = X_real.index.intersection(y_real.index)
            X_real = X_real.loc[common_idx]
            y_real = y_real.loc[common_idx]

            if len(X_synth) == 0 or len(X_real) == 0:
                return 0.0

            # Encode categorical columns
            X_synth_encoded = self._encode_features(X_synth)
            X_real_encoded = self._encode_features(X_real)

            # Train on synthetic, test on real
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_synth_encoded, y_synth)
            y_pred = model.predict(X_real_encoded)

            return accuracy_score(y_real, y_pred)
        else:
            return 0.0

    def tstr_r2(self) -> float:
        """TSTR R² for regression tasks."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Check if it's a regression task
        target_values = self.real_data[self.target_column].dropna()
        if (
            target_values.dtype in ["int64", "float64"]
            and len(target_values.unique()) >= 10
        ):
            # Regression task
            X_synth = self.synthetic_data[self.feature_columns].dropna()
            y_synth = self.synthetic_data[self.target_column].dropna()
            X_real = self.real_data[self.feature_columns].dropna()
            y_real = self.real_data[self.target_column].dropna()

            # Align indices
            common_idx = X_synth.index.intersection(y_synth.index)
            X_synth = X_synth.loc[common_idx]
            y_synth = y_synth.loc[common_idx]

            common_idx = X_real.index.intersection(y_real.index)
            X_real = X_real.loc[common_idx]
            y_real = y_real.loc[common_idx]

            if len(X_synth) == 0 or len(X_real) == 0:
                return 0.0

            # Encode categorical columns
            X_synth_encoded = self._encode_features(X_synth)
            X_real_encoded = self._encode_features(X_real)

            # Train on synthetic, test on real
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_synth_encoded, y_synth)
            y_pred = model.predict(X_real_encoded)

            return r2_score(y_real, y_pred)
        else:
            return 0.0

    def _encode_features(self, X: pd.DataFrame) -> np.ndarray:
        """Encode categorical features for model training."""
        X_encoded = X.copy()

        # Encode categorical columns
        for col in self.categorical_columns:
            if col in X_encoded.columns:
                le = LabelEncoder()
                # Handle NaN values
                mask = X_encoded[col].notna()
                if mask.sum() > 0:
                    X_encoded.loc[mask, col] = le.fit_transform(X_encoded.loc[mask, col].astype(str))
                    X_encoded.loc[~mask, col] = -1  # Encode NaN as -1
                else:
                    X_encoded[col] = -1

        # Convert to numeric, filling NaN with 0
        X_encoded = X_encoded.select_dtypes(include=[np.number])
        X_encoded = X_encoded.fillna(0)

        return X_encoded.values

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all TSTR metrics."""
        return {"tstr_accuracy": self.tstr_accuracy(), "tstr_r2": self.tstr_r2()}


class TRTSMetrics:
    """Train on Real, Test on Synthetic metrics."""

    def __init__(
        self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, target_column: str
    ):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.target_column = target_column
        self.feature_columns = [
            col for col in real_data.columns if col != target_column
        ]
        # Detect categorical columns
        self.categorical_columns = [
            col for col in self.feature_columns
            if real_data[col].dtype == 'object' or real_data[col].dtype == 'category'
            or len(real_data[col].unique()) < 10
        ]
        self.numerical_columns = [
            col for col in self.feature_columns if col not in self.categorical_columns
        ]

    def trts_accuracy(self) -> float:
        """TRTS accuracy for classification tasks."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Check if it's a classification task
        target_values = self.real_data[self.target_column].dropna()
        if target_values.dtype == "object" or len(target_values.unique()) < 10:
            # Classification task
            X_real = self.real_data[self.feature_columns].dropna()
            y_real = self.real_data[self.target_column].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()
            y_synth = self.synthetic_data[self.target_column].dropna()

            # Align indices
            common_idx = X_real.index.intersection(y_real.index)
            X_real = X_real.loc[common_idx]
            y_real = y_real.loc[common_idx]

            common_idx = X_synth.index.intersection(y_synth.index)
            X_synth = X_synth.loc[common_idx]
            y_synth = y_synth.loc[common_idx]

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Encode categorical columns
            X_real_encoded = self._encode_features(X_real)
            X_synth_encoded = self._encode_features(X_synth)

            # Train on real, test on synthetic
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_real_encoded, y_real)
            y_pred = model.predict(X_synth_encoded)

            return accuracy_score(y_synth, y_pred)
        else:
            return 0.0

    def trts_r2(self) -> float:
        """TRTS R² for regression tasks."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Check if it's a regression task
        target_values = self.real_data[self.target_column].dropna()
        if (
            target_values.dtype in ["int64", "float64"]
            and len(target_values.unique()) >= 10
        ):
            # Regression task
            X_real = self.real_data[self.feature_columns].dropna()
            y_real = self.real_data[self.target_column].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()
            y_synth = self.synthetic_data[self.target_column].dropna()

            # Align indices
            common_idx = X_real.index.intersection(y_real.index)
            X_real = X_real.loc[common_idx]
            y_real = y_real.loc[common_idx]

            common_idx = X_synth.index.intersection(y_synth.index)
            X_synth = X_synth.loc[common_idx]
            y_synth = y_synth.loc[common_idx]

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Encode categorical columns
            X_real_encoded = self._encode_features(X_real)
            X_synth_encoded = self._encode_features(X_synth)

            # Train on real, test on synthetic
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_real_encoded, y_real)
            y_pred = model.predict(X_synth_encoded)

            return r2_score(y_synth, y_pred)
        else:
            return 0.0

    def _encode_features(self, X: pd.DataFrame) -> np.ndarray:
        """Encode categorical features for model training."""
        X_encoded = X.copy()

        # Encode categorical columns
        for col in self.categorical_columns:
            if col in X_encoded.columns:
                le = LabelEncoder()
                # Handle NaN values
                mask = X_encoded[col].notna()
                if mask.sum() > 0:
                    X_encoded.loc[mask, col] = le.fit_transform(X_encoded.loc[mask, col].astype(str))
                    X_encoded.loc[~mask, col] = -1  # Encode NaN as -1
                else:
                    X_encoded[col] = -1

        # Convert to numeric, filling NaN with 0
        X_encoded = X_encoded.select_dtypes(include=[np.number])
        X_encoded = X_encoded.fillna(0)

        return X_encoded.values

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all TRTS metrics."""
        return {"trts_accuracy": self.trts_accuracy(), "trts_r2": self.trts_r2()}


class PredictionAgreementMetrics:
    """Prediction agreement metrics between models trained on real vs synthetic."""

    def __init__(
        self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, target_column: str
    ):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.target_column = target_column
        self.feature_columns = [
            col for col in real_data.columns if col != target_column
        ]
        # Detect categorical columns
        self.categorical_columns = [
            col for col in self.feature_columns
            if real_data[col].dtype == 'object' or real_data[col].dtype == 'category'
            or len(real_data[col].unique()) < 10
        ]
        self.numerical_columns = [
            col for col in self.feature_columns if col not in self.categorical_columns
        ]

    def prediction_agreement_percentage(self) -> float:
        """Percentage of identical predictions between models trained on real vs synthetic."""
        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            return 0.0

        # Prepare data
        X_real = self.real_data[self.feature_columns].dropna()
        y_real = self.real_data[self.target_column].dropna()
        X_synth = self.synthetic_data[self.feature_columns].dropna()
        y_synth = self.synthetic_data[self.target_column].dropna()

        # Align indices
        common_idx = X_real.index.intersection(y_real.index)
        X_real = X_real.loc[common_idx]
        y_real = y_real.loc[common_idx]

        common_idx = X_synth.index.intersection(y_synth.index)
        X_synth = X_synth.loc[common_idx]
        y_synth = y_synth.loc[common_idx]

        if len(X_real) == 0 or len(X_synth) == 0:
            return 0.0

        # Check if it's classification or regression
        target_values = self.real_data[self.target_column].dropna()
        is_classification = (
            target_values.dtype == "object" or len(target_values.unique()) < 10
        )

        # Get predictions on a common test set
        test_size = min(len(X_real), len(X_synth)) // 4
        if test_size < 10:
            return 0.0

        # Encode categorical columns
        X_real_encoded = self._encode_features(X_real)
        X_synth_encoded = self._encode_features(X_synth)
        X_test_encoded = self._encode_features(X_real.iloc[:test_size])

        if is_classification:
            # Classification task
            model_real = RandomForestClassifier(n_estimators=100, random_state=42)
            model_synth = RandomForestClassifier(n_estimators=100, random_state=42)

            model_real.fit(X_real_encoded, y_real)
            model_synth.fit(X_synth_encoded, y_synth)
            pred_real = model_real.predict(X_test_encoded)
            pred_synth = model_synth.predict(X_test_encoded)

            # Calculate agreement percentage
            agreement = np.mean(pred_real == pred_synth)
            return agreement
        else:
            # Regression task
            model_real = RandomForestRegressor(n_estimators=100, random_state=42)
            model_synth = RandomForestRegressor(n_estimators=100, random_state=42)

            model_real.fit(X_real_encoded, y_real)
            model_synth.fit(X_synth_encoded, y_synth)
            pred_real = model_real.predict(X_test_encoded)
            pred_synth = model_synth.predict(X_test_encoded)

            # Calculate agreement based on similar predictions (within tolerance)
            tolerance = 0.1 * (y_real.max() - y_real.min())
            agreement = np.mean(np.abs(pred_real - pred_synth) <= tolerance)
            return agreement

    def _encode_features(self, X: pd.DataFrame) -> np.ndarray:
        """Encode categorical features for model training."""
        X_encoded = X.copy()

        # Encode categorical columns
        for col in self.categorical_columns:
            if col in X_encoded.columns:
                le = LabelEncoder()
                # Handle NaN values
                mask = X_encoded[col].notna()
                if mask.sum() > 0:
                    X_encoded.loc[mask, col] = le.fit_transform(X_encoded.loc[mask, col].astype(str))
                    X_encoded.loc[~mask, col] = -1  # Encode NaN as -1
                else:
                    X_encoded[col] = -1

        # Convert to numeric, filling NaN with 0
        X_encoded = X_encoded.select_dtypes(include=[np.number])
        X_encoded = X_encoded.fillna(0)

        return X_encoded.values

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all prediction agreement metrics."""
        return {
            "prediction_agreement_percentage": self.prediction_agreement_percentage()
        }


class LikelihoodLeakMetrics:
    """Likelihood leak metrics using SDV models."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data

    def likelihood_leak_gap(self) -> float:
        """Log-likelihood gap between real and synthetic using SDV models."""
        try:
            # Check if SDV is installed
            try:
                from sdv.single_table import GaussianCopulaSynthesizer
                from sdv.metadata import SingleTableMetadata
            except ImportError:
                print("⚠️ SDV not available (ImportError). Skipping likelihood leak metrics.")
                return 0.0

            # Determine if we can run this check (requires minimal rows)
            if len(self.real_data) < 10 or len(self.synthetic_data) < 10:
                return 0.0

            # Create metadata
            try:
                metadata = SingleTableMetadata()
                metadata.detect_from_dataframe(data=self.real_data)
            except Exception as e:
                print(f"⚠️ Error detecting metadata for likelihood leak: {e}")
                return 0.0

            # Fit synthesizer on real data
            try:
                synthesizer = GaussianCopulaSynthesizer(metadata)
                synthesizer.fit(self.real_data)
            except Exception as e:
                # Common SDV error: constant columns, etc.
                print(f"⚠️ Error fitting synthesizer for likelihood leak: {e}")
                return 0.0

            # Calculate log-likelihood
            try:
                real_ll = synthesizer.get_likelihood(self.real_data)
                synth_ll = synthesizer.get_likelihood(self.synthetic_data)
            except Exception as e:
                print(f"⚠️ Error calculating likelihoods: {e}")
                return 0.0

            # Calculate gap
            # Handle potential NaN/Inf
            if np.isnan(real_ll.mean()) or np.isnan(synth_ll.mean()):
                 return 0.0

            ll_gap = abs(real_ll.mean() - synth_ll.mean())

            # Normalize to 0-1 scale (lower gap is better -> higher score)
            # Use a sigmoid-like or simple inverse
            normalized_gap = 1.0 / (1.0 + ll_gap)

            return float(normalized_gap)

        except Exception as e:
            print(f"⚠️ Unexpected error in likelihood leak metrics: {e}")
            return 0.0

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all likelihood leak metrics."""
        return {"likelihood_leak_gap": self.likelihood_leak_gap()}

