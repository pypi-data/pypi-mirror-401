import numpy as np
from typing import List, Dict
from .factory import CTGANPremiumFactory


class CTGANPremiumAPI:
    """High-level API for premium CTGAN synthetic tabular data generation"""

    def __init__(self, model_type: str = "premium"):
        self.model_type = model_type
        self.model_type = model_type
        self.trainer = None
        self.is_fitted = False
        self.data_min = None
        self.data_max = None

    def fit(
        self,
        data: np.ndarray,
        continuous_cols: list,
        categorical_cols: list,
        epochs: int = 300,
        **kwargs,
    ) -> dict:
        """Fit the premium CTGAN model to data"""

        # Convert column indices to counts
        n_cont = len(continuous_cols)
        n_cat = len(categorical_cols)
        
        # Store cardinalities for reconstruction (computed during preprocessing if available, 
        # but here we compute them from data to be consistent with Basic API logic)
        cardinalities = []
        if n_cat > 0:
            for col_idx in categorical_cols:
                # We assume data is label encoded so we can find max value
                col_data = data[:, col_idx].astype(int)
                cardinalities.append(len(np.unique(col_data)))
        
        # We need to pass cardinalities (list of ints) to the Factory, not just ranges.
        # But wait, Factory.create_premium_model expects categorical_dims as list of ints (cardinalities).
        # The original code passed `list(range(n_cat))` which is WRONG. It passed indices [0, 1, 2].
        # The config expects list of cardinalities [10, 5, 2] etc.
        # I must fix this call too.
        
        # Re-computing cardinalities accurately
        real_cardinalities = []
        for col_idx in categorical_cols:
            unique_vals = np.unique(data[:, col_idx])
            real_cardinalities.append(len(unique_vals))

        # Extract continuous part for clamping
        data_cont = data[:, continuous_cols].astype(np.float32)
        if n_cont > 0:
            self.data_min = np.min(data_cont, axis=0)
            self.data_max = np.max(data_cont, axis=0)
        else:
            self.data_min = None
            self.data_max = None
            
        # Transform data to one-hot (same as Basic CTGAN)
        transformed_parts = []
        
        # Add continuous columns
        if n_cont > 0:
            transformed_parts.append(data_cont) # Already extracted and cast above
            
        # Add one-hot encoded categorical columns
        for i, col_idx in enumerate(categorical_cols):
            # We must use the cardinatlities we computed
            col_data = data[:, col_idx].astype(int)
            n_classes = real_cardinalities[i]
            
            # Create one-hot
            one_hot = np.zeros((len(data), n_classes), dtype=np.float32)
            one_hot[np.arange(len(data)), col_data] = 1.0
            transformed_parts.append(one_hot)
            
        if transformed_parts:
            transformed_data = np.concatenate(transformed_parts, axis=1)
        else:
            transformed_data = np.zeros((len(data), 0))


        # Extract verbose parameter
        verbose = kwargs.pop("verbose", True)

        # Create model based on type
        if self.model_type == "basic":
            self.trainer = CTGANPremiumFactory.create_basic_model(
                continuous_dims=list(range(n_cont)), categorical_dims=real_cardinalities
            )
        elif self.model_type == "premium":
            premium_features = kwargs.get("premium_features", None)
            self.trainer = CTGANPremiumFactory.create_premium_model(
                list(range(n_cont)), real_cardinalities, premium_features
            )
        elif self.model_type == "enterprise":
            self.trainer = CTGANPremiumFactory.create_enterprise_model(
                list(range(n_cont)), real_cardinalities
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        # Fit the model
        losses = self.trainer.fit(transformed_data, epochs=epochs, verbose=verbose)
        self.is_fitted = True

        return losses

    def generate(self, n_samples: int) -> np.ndarray:
        """Generate synthetic samples"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")

        raw_samples = self.trainer.generate(n_samples)
        
        # Reconstruct (Inverse Transform)
        # Split continuous and categorical
        # Continuous dims are 0..n_cont
        # Categorical dims are packed after
        
        # Get dimensions from config
        cont_dims = self.trainer.config.continuous_dims
        cat_dims = self.trainer.config.categorical_dims # List of cardinalities
        
        n_cont_dim = len(cont_dims)
        
        samples_cont = raw_samples[:, :n_cont_dim]
        samples_cat_part = raw_samples[:, n_cont_dim:]
        
        # Clamp continuous
        if self.data_min is not None and self.data_max is not None:
            samples_cont = np.clip(samples_cont, self.data_min, self.data_max)
            
        # Decode Categorical (Argmax)
        samples_cat_list = []
        start_idx = 0
        for dim in cat_dims:
            end_idx = start_idx + dim
            # Extract chunk
            chunk = samples_cat_part[:, start_idx:end_idx]
            # Argmax
            labels = np.argmax(chunk, axis=1).reshape(-1, 1)
            samples_cat_list.append(labels)
            start_idx = end_idx
            
        if samples_cat_list:
            samples_cat = np.hstack(samples_cat_list)
            return np.hstack([samples_cont, samples_cat])
        else:
            return samples_cont

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
            # Create a basic trainer if none exists
            # We need to infer the dimensions from the saved model
            import torch

            checkpoint = torch.load(filepath, map_location="cpu")
            config = checkpoint.get("config")
            if config is None:
                raise ValueError("Cannot load model: config not found in saved file")

            # Create trainer based on model type
            if self.model_type == "basic":
                self.trainer = CTGANPremiumFactory.create_basic_model(
                    continuous_dims=config.continuous_dims,
                    categorical_dims=config.categorical_dims,
                )
            elif self.model_type == "premium":
                self.trainer = CTGANPremiumFactory.create_premium_model(
                    continuous_dims=config.continuous_dims,
                    categorical_dims=config.categorical_dims,
                )
            elif self.model_type == "enterprise":
                self.trainer = CTGANPremiumFactory.create_enterprise_model(
                    continuous_dims=config.continuous_dims,
                    categorical_dims=config.categorical_dims,
                )
            else:
                raise ValueError(f"Unknown model type: {self.model_type}")

        self.trainer.load_model(filepath)
        self.is_fitted = True
