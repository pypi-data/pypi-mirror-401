"""
Derivative Pricing Module

This module provides pricing functionality for various interest rate derivatives
using the calibrated BDT model or simple short-rate models.
"""

import numpy as np
from typing import Optional, List, Tuple, Dict, Union
from dataclasses import dataclass
from enum import Enum

from .model import BDTModel, SimpleShortRateModel
from .lattice import ShortRateLattice


class SwaptionType(Enum):
    """Type of swaption."""
    PAYER = "payer"      # Right to pay fixed, receive floating
    RECEIVER = "receiver"  # Right to receive fixed, pay floating


class OptionType(Enum):
    """Type of option."""
    CALL = "call"
    PUT = "put"


@dataclass
class SwaptionSpec:
    """Specification for a swaption."""
    notional: float
    expiry: int  # Time of option expiry (periods)
    swap_start: int  # When underlying swap starts (usually = expiry)
    swap_end: int  # When underlying swap ends
    fixed_rate: float  # Fixed rate of the underlying swap
    swaption_type: SwaptionType = SwaptionType.PAYER
    option_strike: float = 0.0  # Strike (usually 0 for swaptions)


@dataclass
class BondSpec:
    """Specification for a bond."""
    face_value: float
    maturity: int
    coupon_rate: float = 0.0  # 0 for ZCB
    recovery_rate: float = 0.0  # For defaultable bonds


class SwaptionPricer:
    """
    Pricer for interest rate swaptions using the BDT model.
    
    A swaption gives the holder the right to enter into a swap at
    a future date. For a payer swaption, the holder receives floating
    and pays fixed.
    """
    
    def __init__(self, model: BDTModel):
        """
        Initialize the swaption pricer.
        
        Args:
            model: Calibrated BDT model
        """
        self.model = model
        
    def _compute_swap_value_at_node(
        self,
        time_step: int,
        state: int,
        swap_start: int,
        swap_end: int,
        fixed_rate: float,
        notional: float,
        is_payer: bool
    ) -> float:
        """
        Compute the value of a swap at a specific node.
        
        The swap pays/receives (floating - fixed) * notional in arrears.
        
        Args:
            time_step: Current time step
            state: Current state
            swap_start: When swap starts
            swap_end: When swap ends
            fixed_rate: Fixed leg rate
            notional: Notional amount
            is_payer: True for payer swap (pay fixed)
            
        Returns:
            NPV of the swap at the specified node
        """
        if time_step < swap_start:
            # Before swap starts - need to discount future value
            raise ValueError("Cannot compute swap value before start")
            
        # Build a mini-lattice from this node to value the swap
        n_remaining = swap_end - time_step
        
        # Initialize values at swap end (all zero - last payment already made)
        values = np.zeros((n_remaining + 1, n_remaining + 1))
        
        # Backward induction
        for i in range(n_remaining - 1, -1, -1):
            actual_time = time_step + i
            for j in range(i + 1):
                # Map local state to global state
                global_state = state + j
                
                # Get short rate at this node
                if actual_time < self.model.n_periods:
                    short_rate = self.model.get_short_rate(actual_time, min(global_state, actual_time))
                else:
                    # Use last available rate
                    short_rate = self.model.get_short_rate(
                        self.model.n_periods - 1,
                        min(global_state, self.model.n_periods - 1)
                    )
                
                discount = 1.0 / (1.0 + short_rate)
                
                # Continuation value
                if i < n_remaining - 1:
                    continuation = discount * (
                        self.model.q * values[i + 1, j + 1] +
                        (1 - self.model.q) * values[i + 1, j]
                    )
                else:
                    continuation = 0
                
                # Cash flow at next period (paid in arrears)
                # The payment is based on the rate from the previous period
                if i > 0 or actual_time >= swap_start:
                    # Payment = (floating - fixed) * notional
                    # Floating is the short rate from previous period
                    if is_payer:
                        # Pay fixed, receive floating
                        payment = (short_rate - fixed_rate) * notional
                    else:
                        # Receive fixed, pay floating
                        payment = (fixed_rate - short_rate) * notional
                        
                    # Discount the next-period payment
                    values[i, j] = continuation + discount * payment
                else:
                    values[i, j] = continuation
                    
        return values[0, 0]
    
    def price_swaption(
        self,
        spec: SwaptionSpec
    ) -> float:
        """
        Price a swaption using backward induction.
        
        Args:
            spec: Swaption specification
            
        Returns:
            Present value of the swaption
        """
        n = self.model.n_periods
        expiry = spec.expiry
        
        # Initialize value lattice
        values = np.zeros((n + 1, n + 1))
        
        # At expiry, compute the value of exercising the swaption
        for j in range(expiry + 1):
            # Value of underlying swap if exercised
            swap_value = self._compute_swap_value_lattice(
                expiry, j, spec.swap_start, spec.swap_end,
                spec.fixed_rate, spec.notional,
                spec.swaption_type == SwaptionType.PAYER
            )
            
            # Option payoff: max(swap_value - strike, 0)
            if spec.swaption_type == SwaptionType.PAYER:
                values[expiry, j] = max(swap_value - spec.option_strike, 0)
            else:
                values[expiry, j] = max(spec.option_strike - swap_value, 0)
        
        # Backward induction to time 0
        for i in range(expiry - 1, -1, -1):
            for j in range(i + 1):
                short_rate = self.model.get_short_rate(i, j)
                discount = 1.0 / (1.0 + short_rate)
                
                values[i, j] = discount * (
                    self.model.q * values[i + 1, j + 1] +
                    (1 - self.model.q) * values[i + 1, j]
                )
                
        return values[0, 0]
    
    def _compute_swap_value_lattice(
        self,
        start_time: int,
        start_state: int,
        swap_start: int,
        swap_end: int,
        fixed_rate: float,
        notional: float,
        is_payer: bool
    ) -> float:
        """
        Compute the NPV of a swap starting at a given node.
        
        The swap has cash flows at times swap_start+1, ..., swap_end.
        Each cash flow is (rate_{t-1} - fixed_rate) * notional for a payer swap.
        """
        n = self.model.n_periods
        n_swap_periods = swap_end - swap_start
        
        # Build lattice for the swap from start_time to swap_end
        swap_lattice_size = swap_end - start_time + 1
        values = np.zeros((swap_lattice_size, swap_lattice_size))
        
        # Terminal values (at swap_end): no value remaining
        # Backward induction
        for i in range(swap_lattice_size - 2, -1, -1):
            actual_time = start_time + i
            for j in range(i + 1):
                global_state = start_state + j
                
                # Get short rate
                if actual_time < n:
                    local_state = min(global_state, actual_time)
                    short_rate = self.model.get_short_rate(actual_time, local_state)
                else:
                    short_rate = self.model.get_short_rate(n - 1, min(global_state, n - 1))
                
                discount = 1.0 / (1.0 + short_rate)
                
                # Continuation value
                continuation = discount * (
                    self.model.q * values[i + 1, j + 1] +
                    (1 - self.model.q) * values[i + 1, j]
                )
                
                # Add payment if we're in the swap period
                # Payment at time t+1 is based on rate at time t
                next_time = actual_time + 1
                if next_time > swap_start and next_time <= swap_end:
                    if is_payer:
                        payment = (short_rate - fixed_rate) * notional
                    else:
                        payment = (fixed_rate - short_rate) * notional
                    values[i, j] = continuation + discount * payment
                else:
                    values[i, j] = continuation
                    
        return values[0, 0]
    
    def price_payer_swaption(
        self,
        notional: float,
        expiry: int,
        swap_end: int,
        fixed_rate: float,
        strike: float = 0.0
    ) -> float:
        """
        Convenience method to price a payer swaption.
        
        Args:
            notional: Notional amount
            expiry: Option expiry time
            swap_end: Swap end time
            fixed_rate: Fixed rate of underlying swap
            strike: Option strike (usually 0)
            
        Returns:
            Swaption price
        """
        spec = SwaptionSpec(
            notional=notional,
            expiry=expiry,
            swap_start=expiry,
            swap_end=swap_end,
            fixed_rate=fixed_rate,
            swaption_type=SwaptionType.PAYER,
            option_strike=strike
        )
        return self.price_swaption(spec)


class BondPricer:
    """
    Pricer for bonds, including defaultable bonds with credit risk.
    """
    
    def __init__(self, model: Union[BDTModel, SimpleShortRateModel]):
        """
        Initialize the bond pricer.
        
        Args:
            model: Interest rate model
        """
        self.model = model
        
    def price_zcb(
        self,
        face_value: float,
        maturity: int
    ) -> float:
        """
        Price a zero-coupon bond.
        
        Args:
            face_value: Face value
            maturity: Maturity in periods
            
        Returns:
            Present value
        """
        return face_value * self.model.price_zcb(maturity)
    
    def price_defaultable_zcb(
        self,
        face_value: float,
        maturity: int,
        hazard_rate_func,
        recovery_rate: float
    ) -> float:
        """
        Price a defaultable zero-coupon bond.
        
        Args:
            face_value: Face value
            maturity: Maturity in periods
            hazard_rate_func: Function(i, j) returning hazard rate at node (i,j)
            recovery_rate: Recovery rate upon default (fraction of face value)
            
        Returns:
            Present value of defaultable bond
        """
        n = maturity
        q = self.model.lattice.q
        
        # Value lattice for surviving bond
        # At each node, bond can survive or default
        # If default, receive recovery * face_value
        # If survive to maturity, receive face_value
        
        values = np.zeros((n + 1, n + 1))
        
        # Terminal values: face value if survived
        for j in range(n + 1):
            values[n, j] = face_value
            
        # Backward induction with default risk
        for i in range(n - 1, -1, -1):
            for j in range(i + 1):
                short_rate = self.model.lattice.get_rate(i, j)
                discount = 1.0 / (1.0 + short_rate)
                
                # Hazard rate at this node
                h = hazard_rate_func(i, j)
                
                # Probability of survival
                p_survive = 1.0 - h
                
                # Continuation value if survives
                continuation = discount * (
                    q * values[i + 1, j + 1] +
                    (1 - q) * values[i + 1, j]
                )
                
                # Recovery value if defaults
                recovery_value = discount * recovery_rate * face_value
                
                # Expected value
                values[i, j] = p_survive * continuation + h * recovery_value
                
        return values[0, 0]


class CDSPricer:
    """
    Pricer for Credit Default Swaps.
    """
    
    def __init__(self, model: Union[BDTModel, SimpleShortRateModel]):
        """
        Initialize the CDS pricer.
        
        Args:
            model: Interest rate model
        """
        self.model = model
        
    def price_cds(
        self,
        notional: float,
        maturity: int,
        cds_spread: float,
        hazard_rate_func,
        recovery_rate: float
    ) -> float:
        """
        Price a Credit Default Swap.
        
        The protection buyer pays cds_spread * notional each period.
        Upon default, receives (1 - recovery_rate) * notional.
        
        Args:
            notional: Notional amount
            maturity: CDS maturity
            cds_spread: Annual spread (premium)
            hazard_rate_func: Function(i, j) returning hazard rate
            recovery_rate: Recovery rate
            
        Returns:
            NPV of CDS (positive = value to protection buyer)
        """
        n = maturity
        q = self.model.lattice.q
        
        # Protection leg value (receives 1-R upon default)
        protection_values = np.zeros((n + 1, n + 1))
        
        # Premium leg value (pays spread each period)
        premium_values = np.zeros((n + 1, n + 1))
        
        # Backward induction
        for i in range(n - 1, -1, -1):
            for j in range(i + 1):
                short_rate = self.model.lattice.get_rate(i, j)
                discount = 1.0 / (1.0 + short_rate)
                h = hazard_rate_func(i, j)
                p_survive = 1.0 - h
                
                # Protection leg
                protection_continuation = discount * (
                    q * protection_values[i + 1, j + 1] +
                    (1 - q) * protection_values[i + 1, j]
                )
                default_payment = h * discount * (1 - recovery_rate) * notional
                protection_values[i, j] = p_survive * protection_continuation + default_payment
                
                # Premium leg (paid only if survives)
                premium_continuation = discount * (
                    q * premium_values[i + 1, j + 1] +
                    (1 - q) * premium_values[i + 1, j]
                )
                premium_payment = p_survive * discount * cds_spread * notional
                premium_values[i, j] = p_survive * premium_continuation + premium_payment
                
        # CDS value = Protection leg - Premium leg
        return protection_values[0, 0] - premium_values[0, 0]
    
    def find_fair_spread(
        self,
        notional: float,
        maturity: int,
        hazard_rate_func,
        recovery_rate: float,
        tol: float = 1e-8
    ) -> float:
        """
        Find the fair CDS spread (spread that makes NPV = 0).
        
        Args:
            notional: Notional amount
            maturity: CDS maturity
            hazard_rate_func: Hazard rate function
            recovery_rate: Recovery rate
            tol: Tolerance for convergence
            
        Returns:
            Fair CDS spread
        """
        from scipy.optimize import brentq
        
        def objective(spread):
            return self.price_cds(
                notional, maturity, spread,
                hazard_rate_func, recovery_rate
            )
            
        # Find spread in reasonable range
        return brentq(objective, 0.0001, 0.5, xtol=tol)


def price_payer_swaption(
    model: BDTModel,
    notional: float,
    expiry: int,
    swap_end: int,
    fixed_rate: float,
    strike: float = 0.0
) -> float:
    """
    Convenience function to price a payer swaption.
    
    Args:
        model: Calibrated BDT model
        notional: Notional amount
        expiry: Option expiry
        swap_end: Swap end time
        fixed_rate: Fixed rate
        strike: Option strike
        
    Returns:
        Swaption price
    """
    pricer = SwaptionPricer(model)
    return pricer.price_payer_swaption(
        notional, expiry, swap_end, fixed_rate, strike
    )


def price_defaultable_bond(
    model: Union[BDTModel, SimpleShortRateModel],
    face_value: float,
    maturity: int,
    hazard_rate_func,
    recovery_rate: float
) -> float:
    """
    Convenience function to price a defaultable ZCB.
    
    Args:
        model: Interest rate model
        face_value: Face value
        maturity: Maturity
        hazard_rate_func: Hazard rate function(i, j)
        recovery_rate: Recovery rate
        
    Returns:
        Bond price
    """
    pricer = BondPricer(model)
    return pricer.price_defaultable_zcb(
        face_value, maturity, hazard_rate_func, recovery_rate
    )
