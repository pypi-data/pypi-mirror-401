#!/usr/bin/env python3
"""
BDT Short Rate Model - Command Line Interface

A professional CLI for calibrating the Black-Derman-Toy model
and pricing interest rate derivatives.
"""

import sys
import argparse
import json
from pathlib import Path

import numpy as np

from .model import BDTModel, SimpleShortRateModel
from .calibration import BDTCalibrator, calibrate_bdt_model
from .pricing import SwaptionPricer, BondPricer, CDSPricer, price_payer_swaption
from .utils import (
    load_market_data, 
    compute_discount_factors,
    create_hazard_rate_function,
    build_term_structure_report,
    export_results_to_json,
    export_lattice_to_csv
)


def calibrate_command(args):
    """Handle the calibrate command."""
    print("=" * 60)
    print("BDT Model Calibration")
    print("=" * 60)
    
    # Load market data
    if args.data:
        print(f"Loading market data from: {args.data}")
        periods, rates = load_market_data(args.data)
    else:
        # Use default rates from the problem
        print("Using default market rates")
        rates = np.array([0.030, 0.031, 0.032, 0.033, 0.034, 
                         0.035, 0.0355, 0.036, 0.0365, 0.037])
    
    n_periods = args.periods if args.periods else len(rates)
    rates = rates[:n_periods]
    
    print(f"Number of periods: {n_periods}")
    print(f"Volatility parameter b: {args.b}")
    print(f"Market rates: {rates}")
    print()
    
    # Create calibrator and calibrate
    calibrator = BDTCalibrator(n_periods, b=args.b, tol=args.tolerance)
    result = calibrator.calibrate(rates, verbose=args.verbose)
    
    # Print results
    print(result.summary())
    
    # Get calibrated model
    model = calibrator.get_calibrated_model()
    
    # Show term structure comparison
    if args.verbose:
        print()
        print(build_term_structure_report(model, rates))
    
    # Export if requested
    if args.output:
        results = {
            'n_periods': n_periods,
            'b': args.b,
            'a_params': result.a_params.tolist(),
            'final_error': result.final_error,
            'market_rates': rates.tolist(),
            'model_prices': result.model_prices.tolist()
        }
        export_results_to_json(results, args.output)
        print(f"Results exported to: {args.output}")
        
    if args.lattice_output:
        export_lattice_to_csv(model, args.lattice_output)
        print(f"Lattice exported to: {args.lattice_output}")
    
    return model, result


def price_swaption_command(args):
    """Handle the price-swaption command."""
    print("=" * 60)
    print("Swaption Pricing")
    print("=" * 60)
    
    # First calibrate the model
    if args.data:
        periods, rates = load_market_data(args.data)
    else:
        rates = np.array([0.030, 0.031, 0.032, 0.033, 0.034, 
                         0.035, 0.0355, 0.036, 0.0365, 0.037])
    
    n_periods = args.periods if args.periods else len(rates)
    rates = rates[:n_periods]
    
    print(f"Calibrating model with b = {args.b}...")
    model = calibrate_bdt_model(rates, b=args.b, verbose=False)
    print(f"Calibration complete. Error: {model.calibration_error:.2e}")
    print()
    
    # Price the swaption
    print("Swaption Parameters:")
    print(f"  Notional: ${args.notional:,.2f}")
    print(f"  Expiry: t = {args.expiry}")
    print(f"  Swap End: t = {args.swap_end}")
    print(f"  Fixed Rate: {args.fixed_rate * 100:.2f}%")
    print(f"  Strike: {args.strike}")
    print()
    
    pricer = SwaptionPricer(model)
    price = pricer.price_payer_swaption(
        notional=args.notional,
        expiry=args.expiry,
        swap_end=args.swap_end,
        fixed_rate=args.fixed_rate,
        strike=args.strike
    )
    
    print(f"Payer Swaption Price: ${price:,.2f}")
    print(f"Rounded to nearest integer: ${round(price):,}")
    
    return price


def price_defaultable_bond_command(args):
    """Handle the price-defaultable-bond command."""
    print("=" * 60)
    print("Defaultable Bond Pricing")
    print("=" * 60)
    
    # Create simple short-rate model
    print("Model Parameters:")
    print(f"  r0 = {args.r0 * 100:.2f}%")
    print(f"  u = {args.u}")
    print(f"  d = {args.d}")
    print(f"  q = {args.q}")
    print()
    
    model = SimpleShortRateModel(
        n_periods=args.periods,
        r0=args.r0,
        u=args.u,
        d=args.d,
        q=args.q
    )
    
    print("Bond Parameters:")
    print(f"  Face Value: ${args.face_value:,.2f}")
    print(f"  Recovery Rate: {args.recovery * 100:.1f}%")
    print()
    
    print("Hazard Rate Parameters:")
    print(f"  a = {args.hazard_a}")
    print(f"  b = {args.hazard_b}")
    print()
    
    # Create hazard rate function
    hazard_func = create_hazard_rate_function(args.hazard_a, args.hazard_b)
    
    # Price the bond
    pricer = BondPricer(model)
    price = pricer.price_defaultable_zcb(
        face_value=args.face_value,
        maturity=args.periods,
        hazard_rate_func=hazard_func,
        recovery_rate=args.recovery
    )
    
    print(f"Defaultable ZCB Price: ${price:.2f}")
    
    # Also compute risk-free price for comparison
    rf_price = pricer.price_zcb(args.face_value, args.periods)
    print(f"Risk-Free ZCB Price: ${rf_price:.2f}")
    print(f"Credit Spread Value: ${rf_price - price:.2f}")
    
    return price


def show_lattice_command(args):
    """Handle the show-lattice command."""
    print("=" * 60)
    print("Short Rate Lattice")
    print("=" * 60)
    
    if args.model_type == 'bdt':
        if args.data:
            periods, rates = load_market_data(args.data)
        else:
            rates = np.array([0.030, 0.031, 0.032, 0.033, 0.034, 
                             0.035, 0.0355, 0.036, 0.0365, 0.037])
        
        n_periods = args.periods if args.periods else len(rates)
        rates = rates[:n_periods]
        
        print(f"Calibrating BDT model with b = {args.b}...")
        model = calibrate_bdt_model(rates, b=args.b, verbose=False)
        print()
    else:
        model = SimpleShortRateModel(
            n_periods=args.periods,
            r0=args.r0,
            u=args.u,
            d=args.d
        )
    
    print(model.display_lattice(precision=args.precision))


def main():
    parser = argparse.ArgumentParser(
        description='BDT Short Rate Model - CLI Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Calibrate model with default rates
  python cli.py calibrate --b 0.05 --verbose
  
  # Calibrate from CSV file
  python cli.py calibrate --data market_rates.csv --b 0.05
  
  # Price a payer swaption
  python cli.py price-swaption --expiry 3 --swap-end 10 --fixed-rate 0.039 --notional 1000000
  
  # Price a defaultable bond
  python cli.py price-defaultable-bond --r0 0.05 --u 1.1 --d 0.9 --face-value 100 --recovery 0.2
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Calibrate command
    cal_parser = subparsers.add_parser('calibrate', help='Calibrate the BDT model')
    cal_parser.add_argument('--data', '-d', type=str, help='Path to market rates CSV')
    cal_parser.add_argument('--periods', '-n', type=int, help='Number of periods')
    cal_parser.add_argument('--b', type=float, default=0.05, help='Volatility parameter')
    cal_parser.add_argument('--tolerance', '-t', type=float, default=1e-10, 
                           help='Calibration tolerance')
    cal_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    cal_parser.add_argument('--output', '-o', type=str, help='Output JSON file')
    cal_parser.add_argument('--lattice-output', type=str, help='Export lattice to CSV')
    
    # Price swaption command
    swap_parser = subparsers.add_parser('price-swaption', help='Price a swaption')
    swap_parser.add_argument('--data', '-d', type=str, help='Path to market rates CSV')
    swap_parser.add_argument('--periods', '-n', type=int, default=10, help='Number of periods')
    swap_parser.add_argument('--b', type=float, default=0.05, help='Volatility parameter')
    swap_parser.add_argument('--expiry', '-e', type=int, required=True, help='Option expiry')
    swap_parser.add_argument('--swap-end', type=int, required=True, help='Swap end time')
    swap_parser.add_argument('--fixed-rate', '-r', type=float, required=True, help='Fixed rate')
    swap_parser.add_argument('--notional', type=float, default=1000000, help='Notional amount')
    swap_parser.add_argument('--strike', type=float, default=0.0, help='Option strike')
    
    # Price defaultable bond command
    bond_parser = subparsers.add_parser('price-defaultable-bond', 
                                        help='Price a defaultable bond')
    bond_parser.add_argument('--periods', '-n', type=int, default=10, help='Number of periods')
    bond_parser.add_argument('--r0', type=float, default=0.05, help='Initial short rate')
    bond_parser.add_argument('--u', type=float, default=1.1, help='Up factor')
    bond_parser.add_argument('--d', type=float, default=0.9, help='Down factor')
    bond_parser.add_argument('--q', type=float, default=0.5, help='Risk-neutral probability')
    bond_parser.add_argument('--face-value', '-f', type=float, default=100, help='Face value')
    bond_parser.add_argument('--recovery', '-R', type=float, default=0.2, help='Recovery rate')
    bond_parser.add_argument('--hazard-a', type=float, default=0.01, help='Hazard rate param a')
    bond_parser.add_argument('--hazard-b', type=float, default=1.01, help='Hazard rate param b')
    
    # Show lattice command
    lattice_parser = subparsers.add_parser('show-lattice', help='Display short rate lattice')
    lattice_parser.add_argument('--model-type', choices=['bdt', 'simple'], default='bdt')
    lattice_parser.add_argument('--data', '-d', type=str, help='Path to market rates CSV')
    lattice_parser.add_argument('--periods', '-n', type=int, default=10, help='Number of periods')
    lattice_parser.add_argument('--b', type=float, default=0.05, help='Volatility parameter')
    lattice_parser.add_argument('--r0', type=float, default=0.05, help='Initial rate (simple)')
    lattice_parser.add_argument('--u', type=float, default=1.1, help='Up factor (simple)')
    lattice_parser.add_argument('--d', type=float, default=0.9, help='Down factor (simple)')
    lattice_parser.add_argument('--precision', '-p', type=int, default=4, help='Decimal places')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'calibrate':
        calibrate_command(args)
    elif args.command == 'price-swaption':
        price_swaption_command(args)
    elif args.command == 'price-defaultable-bond':
        price_defaultable_bond_command(args)
    elif args.command == 'show-lattice':
        show_lattice_command(args)


if __name__ == '__main__':
    main()
