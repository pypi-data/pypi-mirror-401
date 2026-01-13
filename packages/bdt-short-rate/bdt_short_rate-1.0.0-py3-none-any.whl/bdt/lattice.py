"""
Short Rate Lattice Construction

This module provides the core lattice structure for binomial short-rate models.
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class LatticeNode:
    """Represents a single node in the short-rate lattice."""
    time_step: int
    state: int
    short_rate: float
    discount_factor: float = 1.0
    value: float = 0.0


class ShortRateLattice:
    """
    A binomial lattice for short-rate modeling.
    
    The lattice represents possible evolutions of the short rate over time.
    At each time step i, there are (i+1) possible states j = 0, 1, ..., i.
    
    Attributes:
        n_periods: Number of time periods in the lattice
        rates: 2D array of short rates, rates[i,j] = rate at time i, state j
        q: Risk-neutral probability of up-move (default 0.5)
    """
    
    def __init__(self, n_periods: int, q: float = 0.5):
        """
        Initialize the lattice.
        
        Args:
            n_periods: Number of time periods
            q: Risk-neutral probability of up-move
        """
        self.n_periods = n_periods
        self.q = q
        
        # Initialize rates matrix (upper triangular structure)
        # rates[i,j] where i = time step, j = number of up moves
        self.rates = np.zeros((n_periods, n_periods))
        
        # Elementary prices for Arrow-Debreu securities
        self.elementary_prices = np.zeros((n_periods + 1, n_periods + 1))
        self.elementary_prices[0, 0] = 1.0
        
    def set_rates_bdt(self, a_params: np.ndarray, b: float) -> None:
        """
        Set short rates using BDT model specification.
        
        r[i,j] = a[i] * exp(b * j)
        
        Args:
            a_params: Array of a[i] parameters for each time step
            b: Volatility parameter (constant)
        """
        for i in range(self.n_periods):
            for j in range(i + 1):
                self.rates[i, j] = a_params[i] * np.exp(b * j)
                
    def set_rates_simple(self, r0: float, u: float, d: float) -> None:
        """
        Set short rates using simple multiplicative model.
        
        r[i,j] = r0 * u^j * d^(i-j)
        
        Args:
            r0: Initial short rate
            u: Up factor
            d: Down factor
        """
        for i in range(self.n_periods):
            for j in range(i + 1):
                self.rates[i, j] = r0 * (u ** j) * (d ** (i - j))
                
    def compute_elementary_prices(self) -> np.ndarray:
        """
        Compute Arrow-Debreu elementary prices.
        
        The elementary price E[i,j] is the time-0 price of a security
        that pays 1 in state (i,j) and 0 elsewhere.
        
        Returns:
            Array of elementary prices
        """
        self.elementary_prices = np.zeros((self.n_periods + 1, self.n_periods + 1))
        self.elementary_prices[0, 0] = 1.0
        
        for i in range(self.n_periods):
            for j in range(i + 1):
                if self.elementary_prices[i, j] > 0:
                    discount = 1.0 / (1.0 + self.rates[i, j])
                    
                    # Probability of up move
                    up_prob = self.q
                    down_prob = 1.0 - self.q
                    
                    # Propagate to next time step
                    self.elementary_prices[i + 1, j + 1] += (
                        self.elementary_prices[i, j] * discount * up_prob
                    )
                    self.elementary_prices[i + 1, j] += (
                        self.elementary_prices[i, j] * discount * down_prob
                    )
                    
        return self.elementary_prices
    
    def compute_zcb_price(self, maturity: int) -> float:
        """
        Compute zero-coupon bond price for given maturity.
        
        Args:
            maturity: Bond maturity (number of periods)
            
        Returns:
            Price of ZCB with face value 1
        """
        self.compute_elementary_prices()
        return np.sum(self.elementary_prices[maturity, :maturity + 1])
    
    def backward_induction(
        self, 
        terminal_values: np.ndarray,
        early_exercise: bool = False,
        exercise_values: Optional[np.ndarray] = None
    ) -> float:
        """
        Perform backward induction to price a derivative.
        
        Args:
            terminal_values: Payoff at terminal nodes [n_periods+1 values]
            early_exercise: Whether early exercise is allowed
            exercise_values: Values if exercised at each node (for American options)
            
        Returns:
            Present value of the derivative
        """
        n = self.n_periods
        values = np.zeros((n + 1, n + 1))
        
        # Set terminal values
        for j in range(n + 1):
            values[n, j] = terminal_values[j] if j < len(terminal_values) else 0.0
            
        # Backward induction
        for i in range(n - 1, -1, -1):
            for j in range(i + 1):
                discount = 1.0 / (1.0 + self.rates[i, j])
                continuation = discount * (
                    self.q * values[i + 1, j + 1] + 
                    (1 - self.q) * values[i + 1, j]
                )
                
                if early_exercise and exercise_values is not None:
                    values[i, j] = max(continuation, exercise_values[i, j])
                else:
                    values[i, j] = continuation
                    
        return values[0, 0]
    
    def get_rate(self, time_step: int, state: int) -> float:
        """Get the short rate at a specific node."""
        return self.rates[time_step, state]
    
    def get_discount_factor(self, time_step: int, state: int) -> float:
        """Get the one-period discount factor at a specific node."""
        return 1.0 / (1.0 + self.rates[time_step, state])
    
    def __repr__(self) -> str:
        return f"ShortRateLattice(n_periods={self.n_periods}, q={self.q})"
    
    def display(self, precision: int = 4) -> str:
        """
        Create a string representation of the lattice.
        
        Args:
            precision: Decimal places for rate display
            
        Returns:
            Formatted string showing the lattice structure
        """
        lines = [f"Short Rate Lattice ({self.n_periods} periods)"]
        lines.append("=" * 50)
        
        for i in range(self.n_periods):
            rates_str = " | ".join(
                f"{self.rates[i, j]:.{precision}f}" 
                for j in range(i + 1)
            )
            lines.append(f"t={i}: {rates_str}")
            
        return "\n".join(lines)
