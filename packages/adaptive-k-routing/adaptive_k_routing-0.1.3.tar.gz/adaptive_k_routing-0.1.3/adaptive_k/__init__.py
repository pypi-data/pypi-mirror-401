"""
Adaptive-K: Entropy-guided dynamic expert selection for MoE models.

Reduce inference costs by 30-50% with proven methodology.

IMPORTANT: Registration required. Get your free license at:
https://adaptive-k.vertexdata.it/register

License: Apache 2.0 with required registration
Website: https://adaptive-k.vertexdata.it
Contact: amministrazione@vertexdata.it
"""

__version__ = "0.1.3"
__author__ = "Vertex Data"
__email__ = "amministrazione@vertexdata.it"

from .router import AdaptiveKRouter, LicenseRequiredError
from .calibration import Calibrator
from .licensing import LicenseValidator, LicenseInfo, print_license_info

__all__ = [
    "AdaptiveKRouter", 
    "LicenseRequiredError",
