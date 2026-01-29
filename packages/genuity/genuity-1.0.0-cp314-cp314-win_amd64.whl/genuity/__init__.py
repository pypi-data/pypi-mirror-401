"""
Genuity: offline-licensed AI library

__version__ = "0.1.2"

Usage:
    import genuity
    genuity.activate('PASTE_LICENSE')
"""
from genuity.licensing import activate_license as _activate_license, check_activation as _check_activation

# Enforce license check before any public API can be used

def _require_activation():
    if not check_activation():
        raise RuntimeError("No active license found. Please call genuity.activate_license('<LICENSE_STRING>') before using any library features.")

# --- Public API gatekeeping ---

def activate_license(license_string):
    """
    Activate this installation with a license string from your purchase portal.
    """
    return _activate_license(license_string)

def check_activation():
    """
    Returns True if a valid license activation cache is present.
    """
    return _check_activation()

# Core modules - Import only what exists and works, always after activation check

# Data Processing
from .data_processor import TabularPreprocessor as _TabularPreprocessor, TabularPostprocessor as _TabularPostprocessor

class TabularPreprocessor(_TabularPreprocessor):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

class TabularPostprocessor(_TabularPostprocessor):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

# Copula API
from .core_generator.copula import CopulaAPI as _CopulaAPI

class CopulaAPI(_CopulaAPI):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

# CTGAN API (Basic and Premium)
from .core_generator.ctgan import CTGANAPI as _CTGANAPI, CTGANPremiumAPI as _CTGANPremiumAPI

class CTGANAPI(_CTGANAPI):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

class CTGANPremiumAPI(_CTGANPremiumAPI):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

# TVAE API (Basic and Premium)
from .core_generator.tvae import TVAEAPI as _TVAEAPI, TVAEPremiumAPI as _TVAEPremiumAPI

class TVAEAPI(_TVAEAPI):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

class TVAEPremiumAPI(_TVAEPremiumAPI):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

# TabuDiff API (Basic and Premium)
from .core_generator.tabudiff import TabuDiffBasicAPI as _TabuDiffBasicAPI, TabuDiffPremiumAPI as _TabuDiffPremiumAPI

class TabuDiffBasicAPI(_TabuDiffBasicAPI):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

class TabuDiffPremiumAPI(_TabuDiffPremiumAPI):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

# Masked Predictor API
from .core_generator.masked_predictor import MaskedPredictorAPI as _MaskedPredictorAPI

class MaskedPredictorAPI(_MaskedPredictorAPI):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

# Differential Privacy
from .core_generator.differential_privacy import DifferentialPrivacyProcessor as _DifferentialPrivacyProcessor, apply_differential_privacy as _apply_differential_privacy

class DifferentialPrivacyProcessor(_DifferentialPrivacyProcessor):
    def __init__(self, *args, **kwargs):
        _require_activation()
        super().__init__(*args, **kwargs)

def apply_differential_privacy(*args, **kwargs):
    _require_activation()
    return _apply_differential_privacy(*args, **kwargs)

# Evaluation
from .evaluation import evaluate_synthetic_data_comprehensive as _evaluate_synthetic_data_comprehensive

def evaluate_synthetic_data_comprehensive(*args, **kwargs):
    _require_activation()
    return _evaluate_synthetic_data_comprehensive(*args, **kwargs)

# Compliance
from .compliance import check_compliance_and_pii as _check_compliance_and_pii

def check_compliance_and_pii(*args, **kwargs):
    _require_activation()
    return _check_compliance_and_pii(*args, **kwargs)

# Utils
try:
    from .utils import print_genuity_banner
except:
    def print_genuity_banner():
        print("Genuity v1.0.0")

__version__ = "0.2.0"
__author__ = "Genuity Team"

__all__ = [
    # Data Processing
    'TabularPreprocessor',
    'TabularPostprocessor',
    # Generators - Copula
    'CopulaAPI',
    # Generators - CTGAN
    'CTGANAPI',
    'CTGANPremiumAPI',
    # Generators - TVAE
    'TVAEAPI',
    'TVAEPremiumAPI',
    # Generators - TabuDiff
    'TabuDiffBasicAPI',
    'TabuDiffPremiumAPI',
    # Generators - Masked Predictor
    'MaskedPredictorAPI',
    # Differential Privacy
    'DifferentialPrivacyProcessor',
    'apply_differential_privacy',
    # Evaluation
    'evaluate_synthetic_data_comprehensive',
    # Compliance
    'check_compliance_and_pii',
    # Utils
    'print_genuity_banner',
    # License Management
    'activate_license',
    'check_activation',
]

# Print banner on import
print_genuity_banner()
