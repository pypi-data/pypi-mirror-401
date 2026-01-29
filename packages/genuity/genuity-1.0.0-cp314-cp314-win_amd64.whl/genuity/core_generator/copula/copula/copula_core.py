"""
Copula-based Synthetic Data Generator - Core Module

This module implements Gaussian copula for tabular synthetic data generation.
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm, gaussian_kde
from sklearn.preprocessing import QuantileTransformer
from typing import List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class CopulaCore:
    """
    Core Gaussian Copula implementation for synthetic data generation.
    
    Supports both continuous and categorical variables through:
    1. Marginal distribution fitting
    2. Transformation to uniform/normal space
   3. Copula (correlation structure) fitting
    4. Sampling and inverse transformation
    """
    
    def __init__(self, copula_type: str = "gaussian", verbose: bool = True):
        """
        Initialize Copula model.
        
        Args:
            copula_type: Type of copula ("gaussian", "t", "vine")
            verbose: Whether to print progress messages
        """
        self.copula_type = copula_type
        self.verbose = verbose
        
        # Storage for fitted components
        self.marginal_distributions = {}
        self.correlation_matrix = None
        self.continuous_cols = None
        self.categorical_cols = None
        self.transformers = {}
        self.is_fitted = False
        
    def _print(self, msg):
        """Print message if verbose."""
        if self.verbose:
            print(f"[CopulaCore] {msg}")
    
    def fit(self, data: np.ndarray, continuous_cols: List[int], categorical_cols: List[int], 
            pretransformed: bool = False, output_info: List[dict] = None):
        """
        Fit the Gaussian copula model to data.
        
        Args:
            data: Input data array (n_samples, n_features)
            continuous_cols: List of column indices for continuous variables
            categorical_cols: List of column indices for categorical variables
            pretransformed: If True, data is already in normalized space (e.g., from TabularPreprocessor).
            output_info: List of dicts with 'num_categories' for each categorical group (from preprocessor.get_output_info())
        """
        self._print("Fitting basic model...")
        self._print(f"Data shape: {data.shape}")
        self._print(f"Continuous columns: {len(continuous_cols)}")
        self._print(f"Categorical columns: {len(categorical_cols)}")
        self._print(f"Pretransformed: {pretransformed}")
        
        self.continuous_cols = continuous_cols
        self.categorical_cols = categorical_cols
        self.n_features = data.shape[1]
        self.pretransformed = pretransformed
        self.output_info = output_info if output_info else []
        
        if pretransformed:
            # Data is already in normalized space (e.g., from QuantileTransformer(normal))
            self._print("Skipping marginal fitting (pretransformed=True)...")
            
            # For continuous: no transformer needed, data is already normal
            for col_idx in continuous_cols:
                self.transformers[col_idx] = None
            
            # For categorical: store the actual proportions from one-hot encoded data
            # This preserves the marginal distribution for generation
            self.category_proportions = []
            n_continuous = len(continuous_cols)
            current_idx = n_continuous
            
            for info in self.output_info:
                n_cats = info['num_categories']
                group_cols = list(range(current_idx, current_idx + n_cats))
                
                # Calculate proportion for each category (column mean = proportion)
                proportions = np.mean(data[:, group_cols], axis=0)
                # Normalize to ensure sum = 1
                proportions = proportions / proportions.sum()
                self.category_proportions.append(proportions)
                
                current_idx += n_cats
            
            self._print(f"Stored proportions for {len(self.category_proportions)} categorical groups")
            
            # Pretransformed data is already normal for CONTINUOUS columns
            normal_data = data.astype(float).copy()
            
            # For CATEGORICAL columns (One-Hot), they are 0/1. 
            # We need to transform them to Latent Gaussian variables to avoid singular matrices.
            # Strategy: Add Jitter -> QuantileTransform(normal)
            self._print(f"Transforming {len(categorical_cols)} categorical columns to latent Gaussian...")
            
            for col_idx in categorical_cols:
                col_data = normal_data[:, col_idx]
                
                # Add uniform jitter [0, 1] to separate the binary/discrete values
                # distinct values allow QuantileTransformer to work properly
                jitter = np.random.uniform(0, 1, size=len(col_data))
                jittered_data = col_data + jitter
                
                # Transform to standard normal
                # We use a broad number of quantiles to approximate the distribution
                qt = QuantileTransformer(
                    output_distribution='normal', 
                    n_quantiles=min(1000, len(col_data)),
                    random_state=42
                )
                normal_col = qt.fit_transform(jittered_data.reshape(-1, 1)).flatten()
                
                # Update normal_data
                normal_data[:, col_idx] = normal_col
                
                # We don't need to store this transformer for generation because
                # Copula generation for categorical uses the stored 'category_proportions' 
                # to sample directly from the categorical distribution, 
                # bypassing the inverse transformation of this latent Gaussian.
                # (See generate() method: if output_info is present, it uses it)

            # Clip extreme values for stability
            normal_data = np.clip(normal_data, -5, 5)
        else:
            # Step 1: Fit marginal distributions
            self._print("Fitting marginal distributions...")
            self._fit_marginals(data)
            
            # Step 2: Transform to uniform space
            self._print("Transforming to uniform space...")
            uniform_data = self._transform_to_uniform(data)
            
            # Step 3: Transform to normal space
            normal_data = stats.norm.ppf(np.clip(uniform_data, 1e-6, 1 - 1e-6))
        
        # Step 4: Fit copula (estimate correlation)
        self._print("Fitting copula...")
        self._fit_copula(normal_data)
        
        self.is_fitted = True
        self._print("Model fitting complete!")
        
        return {"status": "success"}
    
    def _fit_marginals(self, data: np.ndarray):
        """Fit marginal distributions for each column."""
        for col_idx in range(self.n_features):
            col_data = data[:, col_idx]
            
            if col_idx in self.continuous_cols:
                # For continuous: use quantile transformer
                transformer = QuantileTransformer(
                    output_distribution='uniform',
                    n_quantiles=min(1000, len(col_data)),
                    random_state=42
                )
                transformer.fit(col_data.reshape(-1, 1))
                self.transformers[col_idx] = transformer
                
            elif col_idx in self.categorical_cols:
                # For categorical: store empirical distribution
                unique, counts = np.unique(col_data, return_counts=True)
                probabilities = counts / len(col_data)
                self.transformers[col_idx] = {
                    'unique_values': unique,
                    'probabilities': probabilities
                }
    
    def _transform_to_uniform(self, data: np.ndarray) -> np.ndarray:
        """Transform data to uniform [0, 1] space."""
        uniform_data = np.zeros(data.shape, dtype=float)
        
        for col_idx in range(self.n_features):
            col_data = data[:, col_idx]
            
            if col_idx in self.continuous_cols:
                # Transform continuous using quantile transformer
                transformer = self.transformers[col_idx]
                uniform_data[:, col_idx] = transformer.transform(
                    col_data.reshape(-1, 1)
                ).flatten()
                
            elif col_idx in self.categorical_cols:
                # Transform categorical using empirical CDF
                transformer = self.transformers[col_idx]
                unique_vals = transformer['unique_values']
                probs = transformer['probabilities']
                
                # Vectorized transformation with dithering
                # Map values to indices
                # Using np.searchsorted requires sorted unique_vals, but np.unique returns sorted
                val_indices = np.searchsorted(unique_vals, col_data)
                
                # Check for values not in training set (should ideally not happen with correct consistent encoding)
                # But for safety, clip indices
                val_indices = np.clip(val_indices, 0, len(unique_vals) - 1)
                
                # Calculate cumulative probabilities
                cumsum = np.cumsum(probs)
                
                # Get lower and upper bounds for each value
                # lower: cumsum[idx-1] (or 0 if idx=0)
                # upper: cumsum[idx]
                
                upper_bounds = cumsum[val_indices]
                lower_bounds = np.zeros_like(upper_bounds)
                
                # For indices > 0, get the previous cumsum
                mask = val_indices > 0
                lower_bounds[mask] = cumsum[val_indices[mask] - 1]
                
                # Apply random dithering: uniform(lower, upper)
                # width = upper - lower = prob[idx]
                width = upper_bounds - lower_bounds
                
                # Generate random noise [0, 1]
                noise = np.random.random(len(col_data))
                
                # cdf = lower + width * noise
                cdf_values = lower_bounds + width * noise
                
                uniform_data[:, col_idx] = np.clip(cdf_values, 1e-6, 1 - 1e-6)
        
        return uniform_data
    
    def _fit_copula(self, normal_data: np.ndarray):
        """Fit Gaussian copula by estimating correlation matrix."""
        try:
            # Handle potential NaN/inf values
            normal_data = np.nan_to_num(normal_data, nan=0.0, posinf=3.0, neginf=-3.0)
            
            if self.copula_type == "gaussian":
                # Estimate correlation matrix
                try:
                    from sklearn.covariance import GraphicalLasso
                    gl = GraphicalLasso(alpha=0.01, max_iter=100)
                    gl.fit(normal_data)
                    self.correlation_matrix = gl.covariance_
                except Exception as e:
                    self._print(f"⚠️ Graphical Lasso failed: {e}. Using correlation matrix.")
                    self.correlation_matrix = np.corrcoef(normal_data.T)
            else:
                raise NotImplementedError(f"Copula type '{self.copula_type}' not implemented")
            
            # Validate correlation matrix
            if np.any(np.isnan(self.correlation_matrix)) or np.any(np.isinf(self.correlation_matrix)):
                self._print("⚠️ Correlation matrix contains inf/NaN. Using identity matrix.")
                self.correlation_matrix = np.eye(self.n_features)
                
        except Exception as e:
            self._print(f"⚠️ Error fitting copula: {e}. Using identity correlation.")
            self.correlation_matrix = np.eye(self.n_features)
    
    def generate(self, n_samples: int) -> np.ndarray:
        """
        Generate synthetic samples.
        
        Args:
            n_samples: Number of samples to generate
            
        Returns:
            Generated synthetic data
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before generating samples")
        
        # Step 1: Sample from multivariate normal
        try:
            mean = np.zeros(self.n_features)
            normal_samples = np.random.multivariate_normal(
                mean, self.correlation_matrix, size=n_samples
            )
        except Exception as e:
            self._print(f"⚠️ Error sampling from copula: {e}. Using independent samples.")
            normal_samples = np.random.randn(n_samples, self.n_features)
        
        # If pretransformed, the input was already in normal space.
        if getattr(self, 'pretransformed', False):
            synthetic_data = np.zeros_like(normal_samples)
            
            # For continuous columns: output normal samples directly
            # The postprocessor's QuantileTransformer.inverse_transform expects normal input
            for col_idx in self.continuous_cols:
                synthetic_data[:, col_idx] = normal_samples[:, col_idx]
            
            # For categorical (one-hot): convert to proper one-hot using output_info
            # Each categorical group should have softmax applied, then argmax to get one-hot
            output_info = getattr(self, 'output_info', [])
            n_continuous = len(self.continuous_cols)
            
            if output_info:
                # Use stored category proportions to sample categories
                category_proportions = getattr(self, 'category_proportions', [])
                current_idx = n_continuous
                
                for i, info in enumerate(output_info):
                    n_cats = info['num_categories']
                    group_cols = list(range(current_idx, current_idx + n_cats))
                    
                    # Get proportions for this group (stored during fit)
                    if i < len(category_proportions):
                        probs = category_proportions[i]
                    else:
                        # Fallback: uniform distribution
                        probs = np.ones(n_cats) / n_cats
                    
                    # Sample category indices based on stored proportions
                    sampled_idx = np.random.choice(n_cats, size=len(normal_samples), p=probs)
                    
                    # Convert to one-hot
                    one_hot = np.zeros((len(normal_samples), n_cats))
                    one_hot[np.arange(len(normal_samples)), sampled_idx] = 1.0
                    
                    synthetic_data[:, group_cols] = one_hot
                    current_idx += n_cats
            else:
                # Fallback: treat each categorical column independently
                for col_idx in self.categorical_cols:
                    probs = stats.norm.cdf(normal_samples[:, col_idx])
                    synthetic_data[:, col_idx] = (probs > 0.5).astype(float)
            
            return synthetic_data.astype(float)
        
        # Standard flow: Transform to uniform space then to original space
        uniform_samples = stats.norm.cdf(normal_samples)
        synthetic_data = self._inverse_transform(uniform_samples)
        
        return synthetic_data
    
    def _inverse_transform(self, uniform_data: np.ndarray) -> np.ndarray:
        """Transform from uniform space back to original data space."""
        synthetic_data = np.empty(uniform_data.shape, dtype=object)
        
        for col_idx in range(self.n_features):
            uniform_col = uniform_data[:, col_idx]
            
            if col_idx in self.continuous_cols:
                # Inverse transform for continuous
                transformer = self.transformers[col_idx]
                synthetic_data[:, col_idx] = transformer.inverse_transform(
                    uniform_col.reshape(-1, 1)
                ).flatten()
                
            elif col_idx in self.categorical_cols:
                # Inverse transform for categorical - sample based on CDF
                transformer = self.transformers[col_idx]
                unique_vals = transformer['unique_values']
                probs = transformer['probabilities']
                
                # Convert uniform values to categorical via inverse CDF
                # Convert uniform values to categorical via inverse CDF
                cumsum = np.cumsum(probs)
                
                # Vectorized inverse transform using searchsorted
                # Find indices where uniform_col would be inserted to maintain order in cumsum
                # e.g. if cumsum=[0.2, 0.5, 1.0] and u=0.3, searchsorted returns 1 (index of 0.5)
                idx = np.searchsorted(cumsum, uniform_col)
                
                # Clip to valid range
                idx = np.clip(idx, 0, len(unique_vals) - 1)
                
                # Map indices to values
                synthetic_col = unique_vals[idx]
                
                synthetic_data[:, col_idx] = synthetic_col
        
        return synthetic_data
    
    def save_model(self, filepath: str):
        """Save the fitted model."""
        import pickle
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        model_state = {
            'copula_type': self.copula_type,
            'continuous_cols': self.continuous_cols,
            'categorical_cols': self.categorical_cols,
            'n_features': self.n_features,
            'correlation_matrix': self.correlation_matrix,
            'transformers': self.transformers,
            'is_fitted': self.is_fitted
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_state, f)
    
    def load_model(self, filepath: str):
        """Load a saved model."""
        import pickle
        
        with open(filepath, 'rb') as f:
            model_state = pickle.load(f)
        
        self.copula_type = model_state['copula_type']
        self.continuous_cols = model_state['continuous_cols']
        self.categorical_cols = model_state['categorical_cols']
        self.n_features = model_state['n_features']
        self.correlation_matrix = model_state['correlation_matrix']
        self.transformers = model_state['transformers']
        self.is_fitted = model_state['is_fitted']
