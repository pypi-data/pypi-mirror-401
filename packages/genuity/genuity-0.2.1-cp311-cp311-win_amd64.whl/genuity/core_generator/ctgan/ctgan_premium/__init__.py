"""
CTGAN Premium internal package namespace.

This file exposes the utils API so that the outer ctgan package can re-export it cleanly.
"""

from .utils.api import CTGANPremiumAPI
from .utils.factory import CTGANPremiumFactory

__all__ = ["CTGANPremiumAPI", "CTGANPremiumFactory"]
