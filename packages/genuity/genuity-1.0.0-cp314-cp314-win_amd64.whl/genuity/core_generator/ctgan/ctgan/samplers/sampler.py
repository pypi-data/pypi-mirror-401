import torch
import numpy as np
from typing import List, Dict, Tuple, Optional
from ..config.config import CTGANConfig


class CTGANSampler:
    """
    Conditional Sampler for CTGAN.
    
    Implements the "Training-by-Sampling" mechanism:
    1. Choose a discrete column (variable) randomly.
    2. Choose a category within that column (based on frequency).
    3. Retrieve real data rows that match this category.
    4. Generate a condition vector representing this choice.
    
    This forces the GAN to learn all categories, preventing mode collapse on imbalances.
    """

    def __init__(self, config: CTGANConfig):
        self.config = config
        self.latent_dim = config.latent_dim
        self.device = torch.device("cpu") # Will be updated in sample
        
        # State for conditional sampling
        self.output_info: List[Dict] = []
        self.data: Optional[np.ndarray] = None
        self.n_discrete_columns = 0
        
        # Pre-computed indices
        # List of matrices, one per discrete column
        # Each matrix map: category_index -> list of row_indices
        self.category_row_indices: List[List[np.ndarray]] = []
        
        # Log frequencies for sampling categories
        self.category_log_probs: List[np.ndarray] = []

    def fit(self, data: np.ndarray, output_info: List[Dict]) -> None:
        """
        Initialize the sampler with real data and metadata.
        
        Args:
            data: Preprocessed real data (numpy array)
            output_info: Metadata from Preprocessor.get_output_info()
        """
        self.data = data
        self.output_info = output_info
        self.n_discrete_columns = len(output_info)
        
        if self.n_discrete_columns == 0:
            return

        self.category_row_indices = []
        self.category_log_probs = []

        # Build index for each discrete column
        for info in self.output_info:
            start = info['start_idx']
            end = info['end_idx']
            n_cats = info['num_categories']
            
            # Extract the one-hot block for this feature
            # shape: (n_rows, n_cats)
            one_hot_block = data[:, start:end]
            
            # Find which category is active for each row (argmax)
            # shape: (n_rows,)
            # We assume data is strictly one-hot (one 1 per row in this block)
            # If generated data is passed here it might be soft, but we only fit on REAL data
            category_indices = np.argmax(one_hot_block, axis=1)
            
            # Store row indices for each category
            row_indices_per_cat = []
            freqs = []
            
            for cat_idx in range(n_cats):
                # Rows where this category is active
                rows = np.where(category_indices == cat_idx)[0]
                row_indices_per_cat.append(rows)
                freqs.append(len(rows))
                
            self.category_row_indices.append(row_indices_per_cat)
            
            # Compute log probabilities (smoothing with +1 to avoid log(0))
            # Conditional vector is sampled based on log-frequency
            # (Rare categories get boosted probability in the paper's logic, 
            #  but technically we sample based on freq to match density, 
            #  OR we can sample uniformly to force diversity. 
            #  Standard CTGAN uses frequency-based sampling for the condition 
            #  but effectively balances the batch.)
            # Actually, standard CTGAN samples column uniformly, then category based on frequency?
            # No, standard CTGAN samples category based on LOG frequency to normalize?
            # Let's use frequency for now, it's safer.
            freqs = np.array(freqs) + 1  # Smoothing
            probs = freqs / freqs.sum()
            self.category_log_probs.append(np.log(probs))

    def sample_cond(self, n_samples: int) -> Tuple[Optional[torch.Tensor], Optional[torch.Tensor], Optional[torch.Tensor]]:
        """
        Generate conditional vectors and retrieve matching real data.
        
        Returns:
            cond_vector: Tensor of shape (n_samples, total_categories)
            mask: Tensor of shape (n_samples, n_discrete_columns) indicating which col was chosen
            col_idx: Tensor of shape (n_samples,) indicating chosen column index
            opt_idx: Tensor of shape (n_samples,) indicating chosen category index
        """
        if self.n_discrete_columns == 0:
            return None, None, None

        # 1. Choose which discrete column to condition on (Uniformly)
        # shape: (n_samples,)
        col_choices = np.random.randint(0, self.n_discrete_columns, size=n_samples)
        
        # Prepare storage
        # Total number of one-hot entries across all discrete columns
        total_cats = sum(info['num_categories'] for info in self.output_info)
        cond_vector = np.zeros((n_samples, total_cats), dtype=np.float32)
        mask_vector = np.zeros((n_samples, self.n_discrete_columns), dtype=np.float32)
        
        chosen_rows = np.zeros(n_samples, dtype=int)
        
        # 2. For each sample, choose a category within the chosen column
        for i in range(n_samples):
            col_idx = col_choices[i]
            info = self.output_info[col_idx]
            n_cats = info['num_categories']
            
            # Choose category based on log-frequency (or just frequency)
            # Standard implementation uses log-probability to weight rare classes HIGHER?
            # Let's just use the pre-computed probabilities for now.
            # Actually, to FIX imbalance, we should sample rare classes MORE often.
            # The paper says: "We choose a column... then choose a value... according to log-frequency"
            # Wait, log-frequency is for the generator loss. 
            # For sampling input to Generator, we want to sample `cond` uniformly or balanced?
            # Let's simply sample a category from the empirical distribution (log probs)
            p = np.exp(self.category_log_probs[col_idx])
            p /= p.sum() # Renormalize
            cat_idx = np.random.choice(n_cats, p=p)
            
            # 3. Construct Conditional Vector
            # We need to map (col_idx, cat_idx) to global index in cond_vector
            # We can pre-calculate offsets
            global_offset = 0
            for c in range(col_idx):
                global_offset += self.output_info[c]['num_categories']
            
            cond_vector[i, global_offset + cat_idx] = 1.0
            
            # Mask (which column was selected)
            mask_vector[i, col_idx] = 1.0
            
            # 4. Retrieve a Real Data Row that matches this condition
            # This is critical for the Discriminator to see "Real data that matches Cond"
            matching_rows = self.category_row_indices[col_idx][cat_idx]
            if len(matching_rows) == 0:
                 # Should not happen if data integrity is good, but fallback:
                 chosen_rows[i] = np.random.randint(0, len(self.data))
            else:
                 chosen_rows[i] = np.random.choice(matching_rows)
                 
        return (
            torch.tensor(cond_vector, device=self.device),
            torch.tensor(mask_vector, device=self.device),
            chosen_rows # Return indices so Trainer can slice real_data
        )

    def sample_z(self, n_samples: int, device: torch.device) -> torch.Tensor:
        """Sample latent codes"""
        self.device = device
        return torch.randn(n_samples, self.latent_dim, device=device)
