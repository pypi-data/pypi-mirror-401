# BDT Short Rate Model

A professional Python implementation of the Black-Derman-Toy (BDT) binomial short-rate model for interest rate derivatives pricing and calibration.

## Installation

```bash
pip install bdt-short-rate
```

## Quick Start

```python
import numpy as np
from bdt import BDTModel, BDTCalibrator, SwaptionPricer

# Market spot rates (annualized)
spot_rates = np.array([0.03, 0.031, 0.032, 0.033, 0.034,
                       0.035, 0.0355, 0.036, 0.0365, 0.037])

# Create and calibrate the model
model = BDTModel(n_periods=10, b=0.05, dt=1.0)
calibrator = BDTCalibrator(model, spot_rates)
calibrator.calibrate()

# Price a swaption
pricer = SwaptionPricer(model)
price = pricer.price_payer_swaption(
    expiry=5,
    tenor=4,
    strike=0.05,
    notional=1_000_000
)
print(f"Swaption price: ${price:,.2f}")
```

## Features

- **Calibration**: Fit model to market zero-coupon bond prices using scipy.optimize
- **Pricing**: Value swaptions, defaultable bonds, and other interest rate derivatives
- **Lattice Visualization**: Display the short-rate binomial tree
- **CLI Interface**: Command-line tools for production use

## CLI Usage

```bash
# Calibrate model to market data
bdt calibrate --data market_rates.csv --volatility 0.05 --output calibrated.json

# Price a swaption
bdt price-swaption --model calibrated.json --expiry 5 --tenor 4 --strike 0.05

# Show the rate lattice
bdt show-lattice --model calibrated.json
```

## Documentation

See the [full documentation](https://bdt-short-rate.readthedocs.io) for detailed API reference and examples.

## License

MIT License
