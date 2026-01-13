"""
BDT Model Calibration Engine

This module provides calibration functionality for the BDT model,
matching model-implied bond prices to market prices.
"""

import numpy as np
from scipy.optimize import minimize, least_squares
from typing import Optional, Callable, Dict, Tuple, List
from dataclasses import dataclass
import warnings

from .model import BDTModel
from .lattice import ShortRateLattice


@dataclass
class CalibrationResult:
    """Results from model calibration."""
    success: bool
    a_params: np.ndarray
    b: float
    final_error: float
    n_iterations: int
    message: str
    model_prices: np.ndarray
    market_prices: np.ndarray
    
    def summary(self) -> str:
        """Generate a summary of calibration results."""
        lines = [
            "=" * 60,
            "BDT Model Calibration Results",
            "=" * 60,
            f"Success: {self.success}",
            f"Final Error: {self.final_error:.2e}",
            f"Iterations: {self.n_iterations}",
            f"Message: {self.message}",
            "",
            "Calibrated Parameters:",
            f"  b (volatility): {self.b:.6f}",
            "  a[i] parameters:",
        ]
        
        for i, a in enumerate(self.a_params):
            lines.append(f"    a[{i}] = {a:.8f}")
            
        lines.extend([
            "",
            "Price Comparison:",
            f"{'Period':<10}{'Market':<15}{'Model':<15}{'Error':<15}"
        ])
        
        for i, (mkt, mdl) in enumerate(zip(self.market_prices, self.model_prices)):
            error = abs(mkt - mdl)
            lines.append(f"{i+1:<10}{mkt:<15.6f}{mdl:<15.6f}{error:<15.2e}")
            
        lines.append("=" * 60)
        
        return "\n".join(lines)


class BDTCalibrator:
    """
    Calibration engine for the Black-Derman-Toy model.
    
    The calibrator finds the a[i] parameters such that model-implied
    zero-coupon bond prices match market prices as closely as possible.
    
    Attributes:
        model: The BDT model to calibrate
        market_rates: Market spot rates for each period
        tol: Convergence tolerance for optimization
        max_iter: Maximum number of optimization iterations
    """
    
    def __init__(
        self,
        n_periods: int,
        b: float = 0.05,
        tol: float = 1e-10,
        max_iter: int = 10000
    ):
        """
        Initialize the calibrator.
        
        Args:
            n_periods: Number of periods in the model
            b: Volatility parameter
            tol: Convergence tolerance
            max_iter: Maximum iterations
        """
        self.n_periods = n_periods
        self.b = b
        self.tol = tol
        self.max_iter = max_iter
        
        # Model will be created during calibration
        self.model: Optional[BDTModel] = None
        self.market_rates: Optional[np.ndarray] = None
        self.market_zcb_prices: Optional[np.ndarray] = None
        
    def _compute_market_zcb_prices(self, spot_rates: np.ndarray) -> np.ndarray:
        """
        Compute market ZCB prices from spot rates.
        
        Args:
            spot_rates: Array of spot rates (per-period compounding)
            
        Returns:
            Array of ZCB prices (face value = 1)
        """
        n = len(spot_rates)
        prices = np.zeros(n)
        
        for t in range(n):
            # Price of ZCB maturing at t+1: 1/(1+r)^(t+1)
            prices[t] = 1.0 / ((1.0 + spot_rates[t]) ** (t + 1))
            
        return prices
    
    def _objective_function(self, a_params: np.ndarray) -> float:
        """
        Objective function: sum of squared pricing errors.
        
        Args:
            a_params: Current guess for a[i] parameters
            
        Returns:
            Sum of squared errors between model and market prices
        """
        # Ensure all a_params are positive
        if np.any(a_params <= 0):
            return 1e10
            
        # Update model with current parameters
        self.model.set_params(a_params, self.b)
        
        # Compute model ZCB prices
        model_prices = np.array([
            self.model.price_zcb(t + 1) for t in range(self.n_periods)
        ])
        
        # Sum of squared errors
        errors = model_prices - self.market_zcb_prices
        return np.sum(errors ** 2)
    
    def _residuals(self, a_params: np.ndarray) -> np.ndarray:
        """
        Residual function for least squares optimization.
        
        Args:
            a_params: Current guess for a[i] parameters
            
        Returns:
            Array of pricing errors
        """
        # Ensure all a_params are positive
        if np.any(a_params <= 0):
            return np.ones(self.n_periods) * 1e5
            
        # Update model with current parameters
        self.model.set_params(a_params, self.b)
        
        # Compute model ZCB prices
        model_prices = np.array([
            self.model.price_zcb(t + 1) for t in range(self.n_periods)
        ])
        
        return model_prices - self.market_zcb_prices
    
    def calibrate(
        self,
        market_rates: np.ndarray,
        initial_guess: Optional[np.ndarray] = None,
        method: str = 'trf',
        verbose: bool = False
    ) -> CalibrationResult:
        """
        Calibrate the BDT model to market rates.
        
        Args:
            market_rates: Array of market spot rates
            initial_guess: Initial guess for a[i] parameters
            method: Optimization method ('trf', 'lm', 'dogbox', or scipy.optimize methods)
            verbose: Whether to print progress
            
        Returns:
            CalibrationResult containing calibration details
        """
        self.market_rates = np.array(market_rates)
        self.n_periods = len(self.market_rates)
        
        # Compute target ZCB prices
        self.market_zcb_prices = self._compute_market_zcb_prices(self.market_rates)
        
        # Create model
        self.model = BDTModel(self.n_periods, self.b)
        
        # Initial guess: use market rates as starting point
        if initial_guess is None:
            initial_guess = self.market_rates.copy() * 0.5
            
        if verbose:
            print(f"Starting calibration with {self.n_periods} periods")
            print(f"Volatility parameter b = {self.b}")
            print(f"Target tolerance: {self.tol}")
            
        # Perform optimization using least_squares (more robust)
        bounds = (1e-10, np.inf)  # a params must be positive
        
        result = least_squares(
            self._residuals,
            initial_guess,
            bounds=(np.ones(self.n_periods) * 1e-10, np.ones(self.n_periods) * np.inf),
            method=method,
            ftol=self.tol,
            xtol=self.tol,
            gtol=self.tol,
            max_nfev=self.max_iter,
            verbose=2 if verbose else 0
        )
        
        # Check if we need to refine further
        current_error = np.sum(result.fun ** 2)
        refinement_count = 0
        max_refinements = 10
        
        while current_error > self.tol and refinement_count < max_refinements:
            if verbose:
                print(f"Refinement {refinement_count + 1}: error = {current_error:.2e}")
                
            result = least_squares(
                self._residuals,
                result.x,
                bounds=(np.ones(self.n_periods) * 1e-10, np.ones(self.n_periods) * np.inf),
                method=method,
                ftol=self.tol / 10,
                xtol=self.tol / 10,
                gtol=self.tol / 10,
                max_nfev=self.max_iter,
                verbose=2 if verbose else 0
            )
            
            new_error = np.sum(result.fun ** 2)
            if abs(new_error - current_error) < 1e-15:
                break
            current_error = new_error
            refinement_count += 1
            
        # Set final parameters
        final_a_params = result.x
        self.model.set_params(final_a_params, self.b)
        self.model.is_calibrated = True
        self.model.calibration_error = current_error
        
        # Compute final model prices
        model_prices = np.array([
            self.model.price_zcb(t + 1) for t in range(self.n_periods)
        ])
        
        calibration_result = CalibrationResult(
            success=result.success and current_error <= 1e-8,
            a_params=final_a_params,
            b=self.b,
            final_error=current_error,
            n_iterations=result.nfev,
            message=result.message if hasattr(result, 'message') else "Optimization completed",
            model_prices=model_prices,
            market_prices=self.market_zcb_prices
        )
        
        if verbose:
            print(calibration_result.summary())
            
        return calibration_result
    
    def calibrate_with_vol(
        self,
        market_rates: np.ndarray,
        b_initial: float = 0.05,
        calibrate_b: bool = False,
        verbose: bool = False
    ) -> Tuple[CalibrationResult, float]:
        """
        Calibrate the model, optionally including volatility parameter.
        
        Args:
            market_rates: Market spot rates
            b_initial: Initial volatility parameter
            calibrate_b: Whether to also calibrate b
            verbose: Print progress
            
        Returns:
            Tuple of (CalibrationResult, final b value)
        """
        if not calibrate_b:
            self.b = b_initial
            return self.calibrate(market_rates, verbose=verbose), self.b
            
        # Grid search over b values, then refine
        best_error = float('inf')
        best_result = None
        best_b = b_initial
        
        b_values = np.linspace(0.01, 0.2, 20)
        
        for b_test in b_values:
            self.b = b_test
            result = self.calibrate(market_rates, verbose=False)
            
            if result.final_error < best_error:
                best_error = result.final_error
                best_result = result
                best_b = b_test
                
        if verbose:
            print(f"Best b = {best_b:.4f} with error = {best_error:.2e}")
            
        # Refine with best b
        self.b = best_b
        final_result = self.calibrate(market_rates, verbose=verbose)
        
        return final_result, best_b
    
    def get_calibrated_model(self) -> BDTModel:
        """
        Get the calibrated model.
        
        Returns:
            The calibrated BDT model
            
        Raises:
            ValueError: If model has not been calibrated
        """
        if self.model is None or not self.model.is_calibrated:
            raise ValueError("Model has not been calibrated. Call calibrate() first.")
        return self.model


def calibrate_bdt_model(
    market_rates: np.ndarray,
    b: float = 0.05,
    tol: float = 1e-10,
    verbose: bool = False
) -> BDTModel:
    """
    Convenience function to calibrate a BDT model.
    
    Args:
        market_rates: Array of market spot rates
        b: Volatility parameter
        tol: Convergence tolerance
        verbose: Print progress
        
    Returns:
        Calibrated BDT model
    """
    calibrator = BDTCalibrator(len(market_rates), b, tol)
    calibrator.calibrate(market_rates, verbose=verbose)
    return calibrator.get_calibrated_model()
