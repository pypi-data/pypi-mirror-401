# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-10

### Added
- Initial release of BDT Short Rate Model
- `BDTModel` class for short-rate dynamics
- `BDTCalibrator` for fitting to market zero-coupon bond prices
- `SwaptionPricer` for European swaption pricing
- `BondPricer` for defaultable bond pricing
- `CDSPricer` for credit default swap pricing
- `ShortRateLattice` for binomial tree management
- Command-line interface with `calibrate`, `price-swaption`, `price-defaultable-bond`, and `show-lattice` commands
- Comprehensive documentation and examples
