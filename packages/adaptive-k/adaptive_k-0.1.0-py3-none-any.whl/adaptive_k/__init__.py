"""
Adaptive-K: Entropy-guided dynamic expert selection for MoE models.

Reduce inference costs by 30-50% with proven methodology.
"""

__version__ = "0.1.0"
__author__ = "Vertex Data"
__email__ = "amministrazione@vertexdata.it"

from .router import AdaptiveKRouter
from .calibration import Calibrator

__all__ = ["AdaptiveKRouter", "Calibrator"]
