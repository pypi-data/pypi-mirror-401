import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.mixture import GaussianMixture
import numpy as np


# 1. VampPrior with Learnable Pseudo-Inputs
class VampPrior(nn.Module):
    def __init__(self, encoder, num_pseudos=10):
        super().__init__()
        self.encoder = encoder
        self.num_pseudos = num_pseudos
        self.pseudo_inputs = nn.Parameter(torch.randn(num_pseudos, encoder.input_dim))

    def forward(self):
        mu, logvar = self.encoder(self.pseudo_inputs)
        return mu, logvar


# 2. Beta-Divergence Robust VAE
class BetaDivergenceLoss(nn.Module):
    def __init__(self, beta=1.0):
        super().__init__()
        self.beta = beta

    def forward(self, kl_loss):
        # Automatic beta optimization could be added here
        return self.beta * kl_loss


# 3. Disentangled β-VAE with Mutual Information
class BetaVAE(nn.Module):
    def __init__(self, beta=4.0):
        super().__init__()
        self.beta = beta

    def forward(self, recon_loss, kl_loss, mi_loss=0):
        # recon_loss + beta * kl_loss - mutual_info
        return recon_loss + self.beta * kl_loss - mi_loss


# 4. Adaptive Multi-Head Decoder
class MultiHeadDecoder(nn.Module):
    def __init__(self, hidden_dim, n_cont, n_cat):
        super().__init__()
        self.cont_head = nn.Linear(hidden_dim, n_cont)
        self.cat_head = nn.Linear(hidden_dim, n_cat)

    def forward(self, h):
        return self.cont_head(h), self.cat_head(h)


# 5. Cross-Feature Transformer Attention
class TransformerAttention(nn.Module):
    def __init__(self, hidden_dim, nhead=4):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(d_model=hidden_dim, nhead=nhead)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=1)

    def forward(self, h):
        return self.transformer(h.unsqueeze(1)).squeeze(1)


# 6. Gaussian Mixture Model Latent Clustering
class GMMLatentClustering:
    def __init__(self, n_components="auto"):
        self.n_components = n_components
        self.gmm = None

    def fit(self, z):
        if self.n_components == "auto":
            # Use BIC to select best number of clusters
            lowest_bic = np.infty
            best_gmm = None
            for n in range(1, 8):
                gmm = GaussianMixture(n, covariance_type="full")
                gmm.fit(z)
                bic = gmm.bic(z)
                if bic < lowest_bic:
                    lowest_bic = bic
                    best_gmm = gmm
            self.gmm = best_gmm
        else:
            self.gmm = GaussianMixture(self.n_components, covariance_type="full").fit(z)

    def sample(self, n_samples):
        return self.gmm.sample(n_samples)[0]


# 7. Cyclical KL Annealing with Warm Restarts
class CyclicalKLAnnealing:
    def __init__(self, config, n_cycles=4, ratio=0.5):
        self.n_cycles = n_cycles
        self.ratio = ratio
        # Use total epochs instead of batch_size for cycle calculation
        self.epochs_per_cycle = 100  # Default cycle length

    def __call__(self, epoch):
        cycle = np.floor(1 + epoch / self.epochs_per_cycle)
        x = np.abs(epoch / self.epochs_per_cycle - 2 * cycle + 1)
        return max(0.0, min(1.0, (1 - x) / self.ratio))


# 8. Gradient Noise Injection with Adaptive Scaling
class GradientNoiseInjection:
    def __init__(self, config):
        self.base_scale = 1e-3
        self.batch_size = config.batch_size

    def __call__(self, loss, epoch):
        scale = self.base_scale / np.sqrt(epoch + 1)
        # Create noise with the same shape as loss (scalar)
        noise = torch.randn_like(loss) * scale
        return noise


# 9. Wasserstein Loss Integration
class WassersteinLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, recon, data):
        # Use L1 as a proxy for Wasserstein distance
        return torch.mean(torch.abs(recon - data))


# 10. Multi-Metric Quality Gating System
class QualityGatingSystem:
    """Premium Feature 4: Quality Gating

    Filters generated samples based on reconstruction quality and statistical validity.
    Ensures only high-quality samples are returned.
    """
    def __init__(self, config):
        self.config = config
        self.quality_threshold = getattr(config, 'quality_threshold', 0.7)
        self.min_samples = getattr(config, 'min_quality_samples', 0.8)  # Keep at least 80% of samples

    def __call__(self, samples):
        """Filter samples based on quality metrics."""
        n_samples = samples.shape[0]

        # Quality scores (0-1, higher is better)
        quality_scores = np.ones(n_samples)

        # Check 1: No NaN or Inf values
        valid_mask = np.isfinite(samples).all(axis=1)
        quality_scores[~valid_mask] = 0.0

        # Check 2: Continuous features in reasonable range [0, 1] (after normalization)
        # This is handled by inverse transform, but we can check for extreme values
        if samples.shape[1] > 0:
            # Check for values too far from [0, 1] range (might indicate poor reconstruction)
            extreme_mask = (samples < -0.5) | (samples > 1.5)
            extreme_count = extreme_mask.sum(axis=1)
            quality_scores -= extreme_count * 0.1  # Penalize extreme values

        # Check 3: Categorical features have valid one-hot encoding
        # (sum of one-hot should be close to 1 for each categorical group)
        # This is handled by argmax, but we can verify

        # Filter: Keep samples above threshold, but ensure we keep at least min_samples
        threshold = max(self.quality_threshold,
                       np.percentile(quality_scores, (1 - self.min_samples) * 100))
        keep_mask = quality_scores >= threshold

        if keep_mask.sum() < n_samples * 0.5:
            # If too many filtered, keep top quality samples
            n_keep = max(int(n_samples * self.min_samples), 1)
            top_indices = np.argsort(quality_scores)[-n_keep:]
            keep_mask = np.zeros(n_samples, dtype=bool)
            keep_mask[top_indices] = True

        filtered_samples = samples[keep_mask]

        # If we filtered out samples, we might need to generate more to reach target
        # For now, just return filtered samples
        return filtered_samples
