"""
Core Generator Module for Genuity

This module contains various synthetic data generation methods including:
- TabuDiff: Advanced tabular diffusion models
- CTGAN: Conditional Tabular GAN
- TVAE: Tabular Variational Autoencoder
- Copula: Copula-based generation
- Masked Predictor: Mask-based generation
- Differential Privacy: Privacy-preserving data processing
"""

# Differential Privacy
from .differential_privacy import (
    DifferentialPrivacyProcessor,
    apply_differential_privacy
)

# CTGAN - Conditional Tabular GAN
from .ctgan import CTGANAPI
from .ctgan.ctgan_premium.utils.api import CTGANPremiumAPI

# TVAE - Tabular Variational Autoencoder
from .tvae import TVAEAPI, TVAEPremiumAPI

# TabuDiff - Tabular Diffusion Models
from .tabudiff import TabuDiffBasicAPI, TabuDiffPremiumAPI

# Copula - Copula-based generation
from .copula import CopulaAPI

# Masked Predictor
from .masked_predictor import MaskedPredictorAPI

__all__ = [
    # Differential Privacy
    "DifferentialPrivacyProcessor",
    "apply_differential_privacy",
    # CTGAN
    "CTGANAPI",
    "CTGANPremiumAPI",
    # TVAE
    "TVAEAPI",
    "TVAEPremiumAPI",
    # TabuDiff
    "TabuDiffBasicAPI",
    "TabuDiffPremiumAPI",
    # Copula
    "CopulaAPI",
    # Masked Predictor
    "MaskedPredictorAPI",
]
