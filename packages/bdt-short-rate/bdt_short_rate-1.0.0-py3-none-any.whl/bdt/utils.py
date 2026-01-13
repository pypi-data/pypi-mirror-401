"""
Utility Functions

Helper functions for data loading, validation, and common calculations.
"""

import numpy as np
import pandas as pd
from typing import Union, List, Optional, Dict, Tuple
from pathlib import Path


def load_market_data(
    filepath: Union[str, Path],
    rate_column: str = 'SpotRate',
    period_column: str = 'Period'
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load market rate data from a CSV file.
    
    Args:
        filepath: Path to CSV file
        rate_column: Name of column containing rates
        period_column: Name of column containing periods
        
    Returns:
        Tuple of (periods, rates) as numpy arrays
    """
    df = pd.read_csv(filepath)
    
    if rate_column not in df.columns:
        raise ValueError(f"Column '{rate_column}' not found in {filepath}")
        
    periods = df[period_column].values if period_column in df.columns else np.arange(1, len(df) + 1)
    rates = df[rate_column].values
    
    return periods, rates


def compute_discount_factors(spot_rates: np.ndarray) -> np.ndarray:
    """
    Compute discount factors from spot rates.
    
    Args:
        spot_rates: Array of spot rates (periodic compounding)
        
    Returns:
        Array of discount factors
    """
    n = len(spot_rates)
    discount_factors = np.zeros(n)
    
    for t in range(n):
        discount_factors[t] = 1.0 / ((1.0 + spot_rates[t]) ** (t + 1))
        
    return discount_factors


def compute_forward_rates(spot_rates: np.ndarray) -> np.ndarray:
    """
    Compute forward rates from spot rates.
    
    Args:
        spot_rates: Array of spot rates
        
    Returns:
        Array of forward rates
    """
    n = len(spot_rates)
    df = compute_discount_factors(spot_rates)
    
    forward_rates = np.zeros(n)
    forward_rates[0] = spot_rates[0]
    
    for t in range(1, n):
        forward_rates[t] = df[t - 1] / df[t] - 1
        
    return forward_rates


def compute_spot_rates(zcb_prices: np.ndarray) -> np.ndarray:
    """
    Compute spot rates from ZCB prices.
    
    Args:
        zcb_prices: Array of ZCB prices (face value 1)
        
    Returns:
        Array of spot rates
    """
    n = len(zcb_prices)
    spot_rates = np.zeros(n)
    
    for t in range(n):
        spot_rates[t] = (1.0 / zcb_prices[t]) ** (1.0 / (t + 1)) - 1
        
    return spot_rates


def validate_rates(rates: np.ndarray, name: str = "rates") -> None:
    """
    Validate that rates are reasonable.
    
    Args:
        rates: Array of rates to validate
        name: Name for error messages
        
    Raises:
        ValueError: If rates are invalid
    """
    if np.any(np.isnan(rates)):
        raise ValueError(f"{name} contains NaN values")
        
    if np.any(np.isinf(rates)):
        raise ValueError(f"{name} contains infinite values")
        
    if np.any(rates < -1):
        raise ValueError(f"{name} contains rates below -100%")
        
    if np.any(rates > 1):
        import warnings
        warnings.warn(f"{name} contains rates above 100%, check if rates are in decimal form")


def create_hazard_rate_function(a: float, b: float):
    """
    Create a hazard rate function h(i,j) = a * b^(j - i/2).
    
    Args:
        a: Base hazard rate parameter
        b: Growth factor
        
    Returns:
        Callable function(i, j) -> hazard rate
    """
    def hazard_rate(i: int, j: int) -> float:
        return a * (b ** (j - i / 2))
    
    return hazard_rate


def format_rate(rate: float, decimals: int = 4) -> str:
    """Format a rate as a percentage string."""
    return f"{rate * 100:.{decimals}f}%"


def format_price(price: float, decimals: int = 2) -> str:
    """Format a price with currency symbol."""
    return f"${price:,.{decimals}f}"


def build_term_structure_report(
    model,
    market_rates: np.ndarray
) -> str:
    """
    Build a comparison report of model vs market term structure.
    
    Args:
        model: BDT model
        market_rates: Market spot rates
        
    Returns:
        Formatted report string
    """
    n = len(market_rates)
    
    lines = [
        "=" * 70,
        "Term Structure Comparison",
        "=" * 70,
        f"{'Period':<10}{'Market Rate':<15}{'Model Rate':<15}{'ZCB Price':<15}{'Error':<15}"
    ]
    
    market_prices = compute_discount_factors(market_rates)
    
    for t in range(n):
        model_price = model.price_zcb(t + 1)
        model_rate = (1.0 / model_price) ** (1.0 / (t + 1)) - 1
        error = abs(market_prices[t] - model_price)
        
        lines.append(
            f"{t + 1:<10}"
            f"{format_rate(market_rates[t]):<15}"
            f"{format_rate(model_rate):<15}"
            f"{model_price:<15.6f}"
            f"{error:<15.2e}"
        )
        
    lines.append("=" * 70)
    
    return "\n".join(lines)


def export_lattice_to_csv(
    model,
    filepath: Union[str, Path]
) -> None:
    """
    Export the short-rate lattice to a CSV file.
    
    Args:
        model: BDT model
        filepath: Output file path
    """
    n = model.n_periods
    
    # Create a list of records
    records = []
    for i in range(n):
        for j in range(i + 1):
            records.append({
                'time_step': i,
                'state': j,
                'short_rate': model.get_short_rate(i, j)
            })
            
    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)
    

def export_results_to_json(
    results: Dict,
    filepath: Union[str, Path]
) -> None:
    """
    Export results to a JSON file.
    
    Args:
        results: Dictionary of results
        filepath: Output file path
    """
    import json
    
    # Convert numpy arrays to lists
    def convert_numpy(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(v) for v in obj]
        return obj
    
    results_converted = convert_numpy(results)
    
    with open(filepath, 'w') as f:
        json.dump(results_converted, f, indent=2)


class TermStructure:
    """
    Represents a term structure of interest rates.
    
    Supports various interpolation methods for rates between quoted maturities.
    """
    
    def __init__(
        self,
        maturities: np.ndarray,
        rates: np.ndarray,
        rate_type: str = 'spot'
    ):
        """
        Initialize term structure.
        
        Args:
            maturities: Array of maturities
            rates: Array of rates
            rate_type: 'spot', 'forward', or 'discount'
        """
        self.maturities = np.array(maturities)
        self.rates = np.array(rates)
        self.rate_type = rate_type
        
        validate_rates(rates, "term structure rates")
        
    def get_rate(self, maturity: float, interpolation: str = 'linear') -> float:
        """
        Get interpolated rate for a given maturity.
        
        Args:
            maturity: Target maturity
            interpolation: 'linear', 'cubic', or 'flat'
            
        Returns:
            Interpolated rate
        """
        if interpolation == 'linear':
            return np.interp(maturity, self.maturities, self.rates)
        elif interpolation == 'flat':
            idx = np.searchsorted(self.maturities, maturity)
            if idx == 0:
                return self.rates[0]
            return self.rates[idx - 1]
        elif interpolation == 'cubic':
            from scipy.interpolate import CubicSpline
            cs = CubicSpline(self.maturities, self.rates)
            return float(cs(maturity))
        else:
            raise ValueError(f"Unknown interpolation method: {interpolation}")
            
    def get_discount_factor(self, maturity: float) -> float:
        """Get discount factor for given maturity."""
        if self.rate_type == 'spot':
            rate = self.get_rate(maturity)
            return 1.0 / ((1.0 + rate) ** maturity)
        elif self.rate_type == 'discount':
            return self.get_rate(maturity)
        else:
            raise NotImplementedError("Forward rate DF calculation not implemented")
            
    @classmethod
    def from_csv(cls, filepath: Union[str, Path], **kwargs) -> 'TermStructure':
        """Load term structure from CSV file."""
        periods, rates = load_market_data(filepath, **kwargs)
        return cls(periods, rates)
