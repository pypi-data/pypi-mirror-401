"""
CTGAN-based synthetic data generation.

This is the public namespace for the CTGAN core generator. It re-exports
the high-level API from the internal implementation package.
"""

from .ctgan.utils.api import CTGANAPI
from .ctgan_premium.utils.api import CTGANPremiumAPI

__all__ = ["CTGANAPI", "CTGANPremiumAPI"]
