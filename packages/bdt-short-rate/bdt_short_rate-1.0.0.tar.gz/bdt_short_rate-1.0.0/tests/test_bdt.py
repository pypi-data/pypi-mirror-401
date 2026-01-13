"""
Tests for the BDT Short Rate Model package.
"""

import numpy as np
import pytest
from bdt import BDTModel, BDTCalibrator, SwaptionPricer, ShortRateLattice


class TestShortRateLattice:
    """Tests for the ShortRateLattice class."""
    
    def test_lattice_creation(self):
        """Test lattice initialization."""
        lattice = ShortRateLattice(n_periods=10)
        assert lattice.n_periods == 10
        assert lattice.q == 0.5
    
    def test_lattice_zcb_pricing(self):
        """Test zero-coupon bond pricing."""
        lattice = ShortRateLattice(n_periods=5)
        # Set constant rates
        for i in range(5):
            for j in range(i + 1):
                lattice.rates[i, j] = 0.05
        
        price = lattice.compute_zcb_price(maturity=1)
        expected = 1 / (1 + 0.05)
        assert abs(price - expected) < 1e-10


class TestBDTModel:
    """Tests for the BDTModel class."""
    
    def test_model_creation(self):
        """Test model initialization."""
        model = BDTModel(n_periods=10, b=0.05)
        assert model.n_periods == 10
        assert model.b == 0.05
    
    def test_model_short_rate_formula(self):
        """Test BDT short rate formula r[i,j] = a[i] * exp(b * j)."""
        model = BDTModel(n_periods=5, b=0.1)
        model.a_params = np.array([0.03, 0.031, 0.032, 0.033, 0.034])
        model.update_lattice()
        
        # Check rate at node (2, 1): should be a[2] * exp(b * 1)
        expected = 0.032 * np.exp(0.1 * 1)
        actual = model.lattice.rates[2, 1]
        assert abs(actual - expected) < 1e-10


class TestBDTCalibrator:
    """Tests for the BDTCalibrator class."""
    
    def test_calibration_convergence(self):
        """Test that calibration converges."""
        spot_rates = np.array([0.03, 0.031, 0.032, 0.033, 0.034])
        model = BDTModel(n_periods=5, b=0.05)
        calibrator = BDTCalibrator(model, spot_rates)
        
        calibrator.calibrate()
        
        # Check that calibrated prices match market prices
        for i in range(5):
            market_price = 1 / (1 + spot_rates[i]) ** (i + 1)
            model_price = model.price_zcb(i + 1)
            assert abs(market_price - model_price) < 1e-6


class TestSwaptionPricer:
    """Tests for the SwaptionPricer class."""
    
    def test_swaption_pricing(self):
        """Test swaption pricing returns positive value."""
        spot_rates = np.array([0.03, 0.031, 0.032, 0.033, 0.034,
                               0.035, 0.0355, 0.036, 0.0365, 0.037])
        model = BDTModel(n_periods=10, b=0.05)
        calibrator = BDTCalibrator(model, spot_rates)
        calibrator.calibrate()
        
        pricer = SwaptionPricer(model)
        price = pricer.price_payer_swaption(
            expiry=5, tenor=4, strike=0.05, notional=1_000_000
        )
        
        assert price > 0
        assert price < 1_000_000  # Should be less than notional


class TestCoursera:
    """Test cases from Coursera Fixed Income course."""
    
    def test_question_1_b005(self):
        """Question 1: b=0.05, expected ~$4,102."""
        spot_rates = np.array([0.03, 0.031, 0.032, 0.033, 0.034,
                               0.035, 0.0355, 0.036, 0.0365, 0.037])
        model = BDTModel(n_periods=10, b=0.05)
        calibrator = BDTCalibrator(model, spot_rates)
        calibrator.calibrate()
        
        pricer = SwaptionPricer(model)
        price = pricer.price_payer_swaption(
            expiry=5, tenor=4, strike=0.05, notional=1_000_000
        )
        
        # Allow 10% tolerance from expected answer
        assert 3600 < price < 4600
    
    def test_question_2_b010(self):
        """Question 2: b=0.10, expected ~$8,097."""
        spot_rates = np.array([0.03, 0.031, 0.032, 0.033, 0.034,
                               0.035, 0.0355, 0.036, 0.0365, 0.037])
        model = BDTModel(n_periods=10, b=0.10)
        calibrator = BDTCalibrator(model, spot_rates)
        calibrator.calibrate()
        
        pricer = SwaptionPricer(model)
        price = pricer.price_payer_swaption(
            expiry=5, tenor=4, strike=0.05, notional=1_000_000
        )
        
        # Allow 10% tolerance from expected answer
        assert 7200 < price < 9000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
