import numpy as np
import pandas as pd
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
)
from sklearn.preprocessing import LabelEncoder


class SingleColumnPredictor:
    def __init__(self, column_name, column_type, config):
        """
        Initialize single column predictor

        Args:
            column_name: Name of the column to predict
            column_type: Type of the column ('categorical' or 'continuous')
            config: MaskedPredictorConfig instance
        """
        self.column_name = column_name
        self.column_type = column_type
        self.config = config
        self.model = None
        self.label_encoder = None



    def fit(self, X, y):
        """
        Fit the predictor model

        Args:
            X: Feature matrix
            y: Target values
        """
        try:
            # Features are already numeric (preprocessed)
            X_encoded = X

            if self.column_type == "categorical":
                self.model = HistGradientBoostingClassifier(
                    random_state=self.config.random_state
                )
                # Encode target for classification
                self.label_encoder = LabelEncoder()
                # If target is numeric (floats from preprocessor), cast to int for cleaner labels
                if pd.api.types.is_numeric_dtype(y):
                    y_clean = y.astype(int)
                else:
                    y_clean = y.astype(str)
                    
                y_encoded = self.label_encoder.fit_transform(y_clean)
            else:
                self.model = HistGradientBoostingRegressor(
                    random_state=self.config.random_state
                )
                y_encoded = y

            self.model.fit(X_encoded, y_encoded)

        except ValueError as e:
            # Handle wrong model chosen
            if "Unknown label type: continuous" in str(e):
                print(
                    f"[WARN] Misclassified column '{y.name}' as categorical. Switching to regressor."
                )
                self.column_type = "continuous"
                self.model = HistGradientBoostingRegressor(
                    random_state=self.config.random_state
                )
                self.model.fit(X_encoded, y)
            else:
                raise e  # if it's another ValueError, re-raise it

    def predict(self, X):
        """
        Predict values for the given features

        Args:
            X: Feature matrix

        Returns:
            Predicted values
        """
        # Features are already numeric
        X_encoded = X

        # Get predictions
        predictions = self.model.predict(X_encoded)

        # Decode predictions if categorical
        if self.column_type == "categorical" and self.label_encoder is not None:
            predictions = self.label_encoder.inverse_transform(predictions)

        return predictions
