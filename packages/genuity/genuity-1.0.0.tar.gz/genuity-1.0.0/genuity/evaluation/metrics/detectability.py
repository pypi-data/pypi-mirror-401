"""
Detectability Metrics for Synthetic Data Evaluation

This module contains all detectability-related metrics:
- Classifier AUC: AUROC, F1-score, Precision, Recall for classifying real vs synthetic
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
from typing import Dict, List, Tuple, Optional, Union

warnings.filterwarnings("ignore")


class ClassifierAUCMetrics:
    """Classifier-based detectability metrics."""

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame):
        self.real_data = real_data
        self.synthetic_data = synthetic_data
        self.feature_columns = real_data.columns.tolist()
        # Detect categorical columns
        self.categorical_columns = [
            col for col in self.feature_columns
            if real_data[col].dtype == 'object' or real_data[col].dtype == 'category'
            or len(real_data[col].unique()) < 10
        ]
        self.numerical_columns = [
            col for col in self.feature_columns if col not in self.categorical_columns
        ]

    def _encode_features(self, X: pd.DataFrame) -> np.ndarray:
        """Encode categorical features for model training."""
        X_encoded = X.copy()

        # Encode categorical columns
        for col in X_encoded.columns:
            # Check if column is categorical (object type or low cardinality)
            is_categorical = (
                col in self.categorical_columns or
                X_encoded[col].dtype == 'object' or
                X_encoded[col].dtype == 'category' or
                (X_encoded[col].dtype in [np.int64, np.float64] and len(X_encoded[col].unique()) < 10)
            )

            if is_categorical and X_encoded[col].dtype == 'object':
                le = LabelEncoder()
                # Handle NaN values
                mask = X_encoded[col].notna()
                if mask.sum() > 0:
                    try:
                        X_encoded.loc[mask, col] = le.fit_transform(X_encoded.loc[mask, col].astype(str))
                        X_encoded.loc[~mask, col] = -1  # Encode NaN as -1
                    except:
                        # If encoding fails, convert to numeric codes
                        X_encoded[col] = pd.Categorical(X_encoded[col]).codes
                        X_encoded.loc[X_encoded[col] == -1, col] = -1

        # Convert to numeric, filling NaN with 0
        X_encoded = X_encoded.select_dtypes(include=[np.number])
        X_encoded = X_encoded.fillna(0)

        return X_encoded.values

    def classifier_auc(self) -> float:
        """AUROC for classifying real vs synthetic data."""
        try:
            # Prepare data
            X_real = self.real_data[self.feature_columns].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Create labels (1 for real, 0 for synthetic)
            y_real = np.ones(len(X_real))
            y_synth = np.zeros(len(X_synth))

            # Combine data
            X_combined = pd.concat([X_real, X_synth], ignore_index=True)
            y_combined = np.concatenate([y_real, y_synth])

            # Split into train/test
            # Note: stratify might fail if classes are imbalanced, so we handle it
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_combined,
                    y_combined,
                    test_size=0.3,
                    random_state=42,
                    stratify=y_combined,
                )
            except:
                # Fallback without stratification
                X_train, X_test, y_train, y_test = train_test_split(
                    X_combined,
                    y_combined,
                    test_size=0.3,
                    random_state=42,
                )

            # Encode categorical columns
            X_train_encoded = self._encode_features(X_train)
            X_test_encoded = self._encode_features(X_test)

            # Train classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train_encoded, y_train)

            # Get predictions
            y_pred_proba = classifier.predict_proba(X_test_encoded)[:, 1]
            y_pred = classifier.predict(X_test_encoded)

            # Calculate AUROC
            auc = roc_auc_score(y_test, y_pred_proba)

            return auc

        except Exception as e:
            print(f"⚠️ Error calculating classifier AUC: {e}")
            return 0.0

    def classifier_f1(self) -> float:
        """F1-score for classifying real vs synthetic data."""
        try:
            # Prepare data
            X_real = self.real_data[self.feature_columns].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Create labels (1 for real, 0 for synthetic)
            y_real = np.ones(len(X_real))
            y_synth = np.zeros(len(X_synth))

            # Combine data
            X_combined = pd.concat([X_real, X_synth], ignore_index=True)
            y_combined = np.concatenate([y_real, y_synth])

            # Split into train/test
            # Note: stratify might fail if classes are imbalanced, so we handle it
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_combined,
                    y_combined,
                    test_size=0.3,
                    random_state=42,
                    stratify=y_combined,
                )
            except:
                # Fallback without stratification
                X_train, X_test, y_train, y_test = train_test_split(
                    X_combined,
                    y_combined,
                    test_size=0.3,
                    random_state=42,
                )

            # Encode categorical columns
            X_train_encoded = self._encode_features(X_train)
            X_test_encoded = self._encode_features(X_test)

            # Train classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train_encoded, y_train)

            # Get predictions
            y_pred = classifier.predict(X_test_encoded)

            # Calculate F1-score
            f1 = f1_score(y_test, y_pred)

            return f1

        except Exception as e:
            print(f"⚠️ Error calculating classifier F1: {e}")
            return 0.0

    def classifier_precision(self) -> float:
        """Precision for classifying real vs synthetic data."""
        try:
            # Prepare data
            X_real = self.real_data[self.feature_columns].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Create labels (1 for real, 0 for synthetic)
            y_real = np.ones(len(X_real))
            y_synth = np.zeros(len(X_synth))

            # Combine data
            X_combined = pd.concat([X_real, X_synth], ignore_index=True)
            y_combined = np.concatenate([y_real, y_synth])

            # Split into train/test
            # Note: stratify might fail if classes are imbalanced, so we handle it
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_combined,
                    y_combined,
                    test_size=0.3,
                    random_state=42,
                    stratify=y_combined,
                )
            except:
                # Fallback without stratification
                X_train, X_test, y_train, y_test = train_test_split(
                    X_combined,
                    y_combined,
                    test_size=0.3,
                    random_state=42,
                )

            # Encode categorical columns
            X_train_encoded = self._encode_features(X_train)
            X_test_encoded = self._encode_features(X_test)

            # Train classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train_encoded, y_train)

            # Get predictions
            y_pred = classifier.predict(X_test_encoded)

            # Calculate precision
            precision = precision_score(y_test, y_pred)

            return precision

        except Exception as e:
            print(f"⚠️ Error calculating classifier precision: {e}")
            return 0.0

    def classifier_recall(self) -> float:
        """Recall for classifying real vs synthetic data."""
        try:
            # Prepare data
            X_real = self.real_data[self.feature_columns].dropna()
            X_synth = self.synthetic_data[self.feature_columns].dropna()

            if len(X_real) == 0 or len(X_synth) == 0:
                return 0.0

            # Create labels (1 for real, 0 for synthetic)
            y_real = np.ones(len(X_real))
            y_synth = np.zeros(len(X_synth))

            # Combine data
            X_combined = pd.concat([X_real, X_synth], ignore_index=True)
            y_combined = np.concatenate([y_real, y_synth])

            # Split into train/test
            # Note: stratify might fail if classes are imbalanced, so we handle it
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_combined,
                    y_combined,
                    test_size=0.3,
                    random_state=42,
                    stratify=y_combined,
                )
            except:
                # Fallback without stratification
                X_train, X_test, y_train, y_test = train_test_split(
                    X_combined,
                    y_combined,
                    test_size=0.3,
                    random_state=42,
                )

            # Encode categorical columns
            X_train_encoded = self._encode_features(X_train)
            X_test_encoded = self._encode_features(X_test)

            # Train classifier
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X_train_encoded, y_train)

            # Get predictions
            y_pred = classifier.predict(X_test_encoded)

            # Calculate recall
            recall = recall_score(y_test, y_pred)

            return recall

        except Exception as e:
            print(f"⚠️ Error calculating classifier recall: {e}")
            return 0.0

    def evaluate_all(self) -> Dict[str, float]:
        """Evaluate all classifier detectability metrics."""
        return {
            "classifier_auc": self.classifier_auc(),
            "classifier_f1": self.classifier_f1(),
            "classifier_precision": self.classifier_precision(),
            "classifier_recall": self.classifier_recall(),
        }
