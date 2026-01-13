"""
BDT Model Core Implementation

This module implements the Black-Derman-Toy short-rate model.
"""

import numpy as np
from typing import Optional, List, Tuple, Union
from dataclasses import dataclass, field
from .lattice import ShortRateLattice


@dataclass
class BDTModelParams:
    """Parameters for the BDT model."""
    n_periods: int
    a_params: np.ndarray  # Time-dependent drift parameters
    b: float  # Volatility parameter (can be constant or array)
    q: float = 0.5  # Risk-neutral probability
    
    def __post_init__(self):
        if len(self.a_params) != self.n_periods:
            raise ValueError(
                f"a_params length ({len(self.a_params)}) must match "
                f"n_periods ({self.n_periods})"
            )


class BDTModel:
    """
    Black-Derman-Toy Short-Rate Model
    
    The BDT model is a one-factor, arbitrage-free model of short-rate dynamics.
    The short rate at node (i,j) is given by:
    
        r[i,j] = a[i] * exp(b * j)
    
    where:
        - a[i] are calibrated parameters (one for each time step)
        - b is the volatility parameter (constant in this implementation)
        - j is the number of up-moves from time 0 to time i
    
    The model is calibrated to match market zero-coupon bond prices.
    
    Attributes:
        n_periods: Number of periods in the model
        b: Volatility parameter
        a_params: Calibrated drift parameters
        lattice: The underlying short-rate lattice
        is_calibrated: Whether the model has been calibrated
    """
    
    def __init__(
        self, 
        n_periods: int, 
        b: float = 0.05, 
        q: float = 0.5
    ):
        """
        Initialize the BDT model.
        
        Args:
            n_periods: Number of time periods
            b: Volatility parameter (default 0.05)
            q: Risk-neutral probability of up-move (default 0.5)
        """
        self.n_periods = n_periods
        self.b = b
        self.q = q
        
        # Initialize parameters (will be set during calibration)
        self.a_params = np.zeros(n_periods)
        
        # Create the lattice
        self.lattice = ShortRateLattice(n_periods, q)
        
        # Calibration state
        self.is_calibrated = False
        self.calibration_error = float('inf')
        
    def set_params(self, a_params: np.ndarray, b: Optional[float] = None) -> None:
        """
        Set model parameters directly.
        
        Args:
            a_params: Array of a[i] parameters
            b: Optional new volatility parameter
        """
        if len(a_params) != self.n_periods:
            raise ValueError(
                f"a_params length ({len(a_params)}) must match "
                f"n_periods ({self.n_periods})"
            )
            
        self.a_params = np.array(a_params)
        if b is not None:
            self.b = b
            
        # Update lattice with new parameters
        self.lattice.set_rates_bdt(self.a_params, self.b)
        
    def get_short_rate(self, time_step: int, state: int) -> float:
        """
        Get the short rate at a specific node.
        
        Args:
            time_step: Time index (0 to n_periods-1)
            state: State index (0 to time_step)
            
        Returns:
            Short rate at the specified node
        """
        return self.lattice.get_rate(time_step, state)
    
    def get_discount_factor(self, time_step: int, state: int) -> float:
        """
        Get the one-period discount factor at a specific node.
        
        Args:
            time_step: Time index
            state: State index
            
        Returns:
            One-period discount factor
        """
        return self.lattice.get_discount_factor(time_step, state)
    
    def price_zcb(self, maturity: int) -> float:
        """
        Price a zero-coupon bond with face value 1.
        
        Args:
            maturity: Bond maturity (number of periods)
            
        Returns:
            Present value of the ZCB
        """
        return self.lattice.compute_zcb_price(maturity)
    
    def price_coupon_bond(
        self, 
        maturity: int, 
        coupon_rate: float, 
        face_value: float = 100.0
    ) -> float:
        """
        Price a coupon-bearing bond.
        
        Args:
            maturity: Bond maturity
            coupon_rate: Annual coupon rate (e.g., 0.05 for 5%)
            face_value: Face value of the bond
            
        Returns:
            Present value of the bond
        """
        coupon = face_value * coupon_rate
        
        # Sum of discounted coupons plus discounted face value
        price = 0.0
        for t in range(1, maturity + 1):
            zcb_price = self.price_zcb(t)
            price += coupon * zcb_price
            
        price += face_value * self.price_zcb(maturity)
        
        return price
    
    def get_elementary_prices(self) -> np.ndarray:
        """
        Get the Arrow-Debreu elementary prices.
        
        Returns:
            Matrix of elementary prices
        """
        return self.lattice.compute_elementary_prices()
    
    def compute_forward_rates(self) -> np.ndarray:
        """
        Compute forward rates implied by the model.
        
        Returns:
            Array of forward rates for each period
        """
        forward_rates = np.zeros(self.n_periods)
        
        for t in range(self.n_periods):
            if t == 0:
                forward_rates[t] = self.price_zcb(1)
            else:
                zcb_t = self.price_zcb(t)
                zcb_t1 = self.price_zcb(t + 1)
                forward_rates[t] = zcb_t / zcb_t1 - 1
                
        return forward_rates
    
    def display_lattice(self, precision: int = 4) -> str:
        """Display the short-rate lattice."""
        return self.lattice.display(precision)
    
    def get_params(self) -> BDTModelParams:
        """Get current model parameters as a dataclass."""
        return BDTModelParams(
            n_periods=self.n_periods,
            a_params=self.a_params.copy(),
            b=self.b,
            q=self.q
        )
    
    def __repr__(self) -> str:
        status = "calibrated" if self.is_calibrated else "not calibrated"
        return (
            f"BDTModel(n_periods={self.n_periods}, b={self.b}, "
            f"q={self.q}, status={status})"
        )


class SimpleShortRateModel:
    """
    A simple multiplicative short-rate model.
    
    The short rate at node (i,j) is given by:
        r[i,j] = r0 * u^j * d^(i-j)
    
    This is useful for defaultable bond pricing and CDS valuation.
    """
    
    def __init__(
        self, 
        n_periods: int, 
        r0: float, 
        u: float, 
        d: float, 
        q: float = 0.5
    ):
        """
        Initialize the simple short-rate model.
        
        Args:
            n_periods: Number of periods
            r0: Initial short rate
            u: Up factor
            d: Down factor
            q: Risk-neutral probability of up-move
        """
        self.n_periods = n_periods
        self.r0 = r0
        self.u = u
        self.d = d
        self.q = q
        
        # Create and populate the lattice
        self.lattice = ShortRateLattice(n_periods, q)
        self.lattice.set_rates_simple(r0, u, d)
        
    def get_short_rate(self, time_step: int, state: int) -> float:
        """Get the short rate at a specific node."""
        return self.lattice.get_rate(time_step, state)
    
    def price_zcb(self, maturity: int) -> float:
        """Price a zero-coupon bond."""
        return self.lattice.compute_zcb_price(maturity)
    
    def display_lattice(self, precision: int = 4) -> str:
        """Display the short-rate lattice."""
        return self.lattice.display(precision)
    
    def __repr__(self) -> str:
        return (
            f"SimpleShortRateModel(n_periods={self.n_periods}, "
            f"r0={self.r0}, u={self.u}, d={self.d})"
        )
