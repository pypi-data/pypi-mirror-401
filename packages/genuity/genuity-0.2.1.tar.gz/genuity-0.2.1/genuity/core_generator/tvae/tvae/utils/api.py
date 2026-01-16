import numpy as np
from .factory import TVAEFactory


class TVAEAPI:
    """High-level API for TVAE synthetic tabular data generation (basic edition)"""

    def __init__(self, model_type: str = "basic"):
        # Only basic model is supported in the base package
        if model_type != "basic":
            raise ValueError(
                "This package provides only the basic TVAE. For advanced features, import tvae_premium and use TVAEAPI(model_type='premium')."
            )
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
        
        # Calculate cardinalities and transform data to one-hot
        # We assume data is label-encoded (integers) for categorical columns
        
        # 1. Compute cardinalities
        cardinalities = []
        for col_idx in categorical_cols:
            unique_vals = np.unique(data[:, col_idx])
            cardinalities.append(len(unique_vals))
            
        # 2. Transform data to one-hot
        transformed_parts = []
        
        # Add continuous columns
        if continuous_cols:
            cont_data = data[:, continuous_cols]
            # Capture min/max for clamping
            self.data_min = np.min(cont_data, axis=0)
            self.data_max = np.max(cont_data, axis=0)
            transformed_parts.append(cont_data)
            
        # Add one-hot encoded categorical columns
        for i, col_idx in enumerate(categorical_cols):
            col_data = data[:, col_idx].astype(int)
            n_classes = cardinalities[i]
            
            # Create one-hot
            one_hot = np.zeros((len(data), n_classes), dtype=np.float32)
            one_hot[np.arange(len(data)), col_data] = 1.0
            transformed_parts.append(one_hot)
            
        if transformed_parts:
            transformed_data = np.concatenate(transformed_parts, axis=1)
        else:
            transformed_data = np.zeros((len(data), 0))

        # Create basic model only
        # categorical_dims is a list of cardinalities
        self.trainer = TVAEFactory.create_basic_model(
            continuous_dims=list(range(len(continuous_cols))), 
            categorical_dims=cardinalities
        )
        losses = self.trainer.fit(
            transformed_data, epochs=epochs, verbose=kwargs.get("verbose", True)
        )
        self.is_fitted = True
        
        # Store metadata for generation
        self.continuous_cols = continuous_cols
        self.categorical_cols = categorical_cols
        self.cardinalities = cardinalities
        
        return losses

    def generate(self, n_samples: int) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")
            
        # Generate raw data (continuous + one-hot)
        raw_data = self.trainer.generate(n_samples)
        
        # Reconstruct original format (continuous + label-encoded categorical)
        n_cont = len(self.continuous_cols)
        
        # Extract continuous part
        continuous_part = raw_data[:, :n_cont]
        
        # Clamp continuous values to original range to ensure post-processing compatibility
        if self.data_min is not None and self.data_max is not None:
            continuous_part = np.clip(continuous_part, self.data_min, self.data_max)
        
        # Extract and convert categorical part
        categorical_part = raw_data[:, n_cont:]
        
        categorical_labels = []
        start_idx = 0
        for cardinality in self.cardinalities:
            end_idx = start_idx + cardinality
            # Argmax to get label
            labels = np.argmax(categorical_part[:, start_idx:end_idx], axis=1)
            categorical_labels.append(labels.reshape(-1, 1))
            start_idx = end_idx
            
        if categorical_labels:
            categorical_labels = np.concatenate(categorical_labels, axis=1)
        else:
            categorical_labels = np.zeros((n_samples, 0))
            
        # Combine based on original column order
        total_cols = len(self.continuous_cols) + len(self.categorical_cols)
        output = np.zeros((n_samples, total_cols))
        
        cols_data = []
        for i, col_idx in enumerate(self.continuous_cols):
            cols_data.append((col_idx, continuous_part[:, i]))
            
        for i, col_idx in enumerate(self.categorical_cols):
            cols_data.append((col_idx, categorical_labels[:, i]))
            
        cols_data.sort(key=lambda x: x[0])
        result = np.stack([x[1] for x in cols_data], axis=1)
        
        return result

    def get_feature_importance(self):
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")
        return self.trainer.get_feature_importance()

    def save(self, filepath: str):
        """Save the model with all metadata"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
            
        metadata = {
            "continuous_cols": list(self.continuous_cols),
            "categorical_cols": list(self.categorical_cols),
            "cardinalities": [int(v) for v in self.cardinalities],
            "data_min": self.data_min.tolist() if self.data_min is not None else None,
            "data_max": self.data_max.tolist() if self.data_max is not None else None
        }
        self.trainer.save_model(filepath, **metadata)

    def load(self, filepath: str):
        """Load a saved model and restore metadata"""
        if self.trainer is None:
            # Reconstruct basic trainer if needed
            import torch
            try:
                checkpoint = torch.load(filepath, map_location="cpu", weights_only=True)
            except (TypeError, AttributeError):
                checkpoint = torch.load(filepath, map_location="cpu")
                
            self.trainer = TVAEFactory.create_basic_model(
                continuous_dims=list(range(len(checkpoint.get("continuous_cols", [])))),
                categorical_dims=checkpoint.get("cardinalities", [])
            )
            
        self.trainer.load_model(filepath)
        
        # Restore metadata
        import torch
        try:
            checkpoint = torch.load(filepath, map_location="cpu", weights_only=True)
        except (TypeError, AttributeError):
            checkpoint = torch.load(filepath, map_location="cpu")
            
        if 'continuous_cols' in checkpoint:
            self.continuous_cols = checkpoint['continuous_cols']
        if 'categorical_cols' in checkpoint:
            self.categorical_cols = checkpoint['categorical_cols']
        if 'cardinalities' in checkpoint:
            self.cardinalities = checkpoint['cardinalities']
        if 'data_min' in checkpoint:
            self.data_min = np.array(checkpoint['data_min']) if checkpoint['data_min'] is not None else None
        if 'data_max' in checkpoint:
            self.data_max = np.array(checkpoint['data_max']) if checkpoint['data_max'] is not None else None
            
        self.is_fitted = True
