import torch
import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict
from ..config.config import CTGANPremiumConfig


class CTGANPremiumSampler:
    """Conditional sampler for CTGAN to handle mode collapse"""

    def __init__(self, config: CTGANPremiumConfig):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.n_discrete_columns = 0
        self.total_categories = 0
        self.output_info = []
        self.category_log_probs = {} # Log probabilities of categories per column
        self.real_data_indices = defaultdict(list) # Indices of real data rows matching each category

    def fit(self, real_data: np.ndarray, output_info: List[Dict] = None):
        """
        Fit the sampler to the real data.
        Args:
            real_data: The real data, as a numpy array.
            output_info: Metadata about categorical columns, including their spans and dimensions.
        """
        self.real_data = real_data
        self.output_info = output_info or []
        self.n_discrete_columns = len(self.output_info)
        self.real_data_indices = defaultdict(list)
        self.category_log_probs = {}
        
        # Calculate total number of categories for condition vector dimension
        self.total_categories = sum(info['num_categories'] for info in self.output_info)

        if self.n_discrete_columns == 0:
            # No discrete columns, standard sampling will be used
            return

        # Precompute category frequencies and indices
        for col_info in self.output_info:
            col_name = col_info['name']
            num_categories = col_info['num_categories']
            start_idx = col_info['start_idx']
            end_idx = col_info['end_idx']

            # Extract the one-hot encoded part for this column
            # Note: real_data here is expected to be already One-Hot Encoded from Preprocessor
            one_hot_cols = real_data[:, start_idx:end_idx]

            # Find the category index for each row
            category_indices = np.argmax(one_hot_cols, axis=1)

            # Calculate category frequencies (log probabilities)
            unique_cats, counts = np.unique(category_indices, return_counts=True)
            log_probs = np.log(counts / len(real_data))
            
            # Store log probabilities
            full_log_probs = np.full(num_categories, -np.inf) # Use -inf for unseen categories
            full_log_probs[unique_cats] = log_probs
            self.category_log_probs[col_name] = full_log_probs

            # Index real data by category
            for i, cat_idx in enumerate(category_indices):
                self.real_data_indices[(col_name, cat_idx)].append(i)

    def sample_cond(self, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor, np.ndarray]:
        """
        Sample conditional vectors and corresponding real data indices.
        Returns:
            cond_vec: The sampled conditional vector (batch_size, TOTAL_CATEGORIES).
            mask: A mask indicating which columns were sampled (batch_size, n_discrete_columns).
            real_idx: Indices of the real data rows matching the sampled conditions.
        """
        if self.n_discrete_columns == 0:
            return None, None, np.random.randint(0, len(self.real_data), batch_size)

        # Condition vector is ONE-HOT over ALL categories (not just columns)
        cond_vec = torch.zeros(batch_size, self.total_categories, device=self.device)
        mask = torch.zeros(batch_size, self.n_discrete_columns, device=self.device)
        real_idx = np.empty(batch_size, dtype=int)

        # Pre-calculate offsets for efficiency
        offsets = [0] * self.n_discrete_columns
        current_offset = 0
        for i, info in enumerate(self.output_info):
            offsets[i] = current_offset
            current_offset += info['num_categories']

        # Sample conditions
        for i in range(batch_size):
            # Choose a column to sample from uniformly
            col_idx_to_sample = np.random.randint(0, self.n_discrete_columns)
            col_info = self.output_info[col_idx_to_sample]
            col_name = col_info['name']
            num_categories = col_info['num_categories']

            # Sample a category based on log probabilities
            weights = np.exp(self.category_log_probs[col_name])
            
            # Normalize weights (handle zeros/NaNs)
            weights = np.array(weights)
            weights[np.isnan(weights)] = 0
            if weights.sum() == 0:
                weights = np.ones(len(weights)) / len(weights) # Fallback to uniform if empty
            else:
                weights = weights / weights.sum()

            sampled_cat = np.random.choice(range(num_categories), p=weights)

            # Set the conditional vector (Global One-Hot)
            global_cat_idx = offsets[col_idx_to_sample] + sampled_cat
            cond_vec[i, global_cat_idx] = 1
            
            # Set the mask (Which column was chosen)
            mask[i, col_idx_to_sample] = 1

            # Retrieve a real data index matching this condition
            possible_indices = self.real_data_indices.get((col_name, sampled_cat))
            if possible_indices:
                real_idx[i] = np.random.choice(possible_indices)
            else:
                # Fallback: if no data matches, pick a random index
                real_idx[i] = np.random.randint(0, len(self.real_data))

        return cond_vec, mask, real_idx

    def sample_z(self, batch_size: int, device: torch.device) -> torch.Tensor:
        """Sample latent vectors"""
        return torch.randn(batch_size, self.config.latent_dim, device=device)
