"""
BDT Short Rate Model - Python Implementation

A professional implementation of the Black-Derman-Toy binomial short-rate model
for interest rate derivatives pricing and calibration.
"""

from .model import BDTModel
from .calibration import BDTCalibrator
from .pricing import SwaptionPricer, BondPricer, CDSPricer
from .lattice import ShortRateLattice
from .utils import load_market_data, compute_discount_factors

__version__ = "1.0.0"
__author__ = "Quant Finance Team"

__all__ = [
    "BDTModel",
    "BDTCalibrator", 
    "SwaptionPricer",
    "BondPricer",
    "CDSPricer",
    "ShortRateLattice",
    "load_market_data",
    "compute_discount_factors",
]
