"""
PFASProphet CLI

Command-line interface for PFASProphet predictions.

Usage:
  - Predict from lists:
      pfasprophet --mass '[248.9461]' --fragments '[[63.9624]]'
  - Predict from CSV:
      pfasprophet --file path/to/data.csv --mass-col mass --fragments-col fragments
  - Show help:
      pfasprophet --help

Behavior:
  - If no arguments are provided, the help message is displayed and the process exits.
  - `--is-ionised` indicates input masses are already ionised (default True).
  - `--in-file` will append a `PP_Score` column to the input CSV (if supported).

Exit codes:
  0 : success
  1 : usage error or runtime failure

This module exposes a `main()` entry point used by the package script `pfasprophet`.
"""

import argparse
import json
import sys
from typing import Optional
from .predictor import PFASProphet
import logging

logger = logging.getLogger(__name__)

def main() -> None:
    """Run the CLI."""
    parser = argparse.ArgumentParser(description="PFASProphet CLI for predictions")
    parser.add_argument("-h", "--help", action="help", help="Display usage information and exit, if you need further help, refer to the documentation at https://pfasprophet.readthedocs.io/")
    parser.add_argument("--mass", type=str, help="JSON string of masses, e.g., '[100.0, 200.0]'")
    parser.add_argument("--fragments", type=str, help="JSON string of fragments, e.g., '[[1.0], [2.0]]'")
    parser.add_argument("--file", type=str, help="Path to CSV file to process")
    parser.add_argument("--mass-col", type=str, default="mass", help="Mass column name in CSV file (default: mass)")
    parser.add_argument("--fragments-col", type=str, default="fragments", help="Fragments column name in CSV file (default: fragments)")
    parser.add_argument("--in-file", action="store_true", help="Append PFAS Prophet score column to input file else new file is created")
    parser.add_argument("--is-ionised", action="store_true", default=True, help="if true, mass is ionised (default); if false, mass is neutral and proton mass is subtracted to obtain ionised mass")

    # If no arguments provided, show help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    prophet = PFASProphet()

    try:
        if args.file:
            result = prophet.predict(
                file_path=args.file,
                mass_col=args.mass_col,
                fragments_col=args.fragments_col,
                in_file=args.in_file,
                is_ionised=args.is_ionised
            )
        elif args.mass and args.fragments:
            mass_list = json.loads(args.mass)
            fragments_list = json.loads(args.fragments)
            result = prophet.predict(
                mass=mass_list,
                fragments=fragments_list,
                is_ionised=args.is_ionised
            )
        else:
            print("Error: Provide --file or both --mass and --fragments")
            sys.exit(1)

        logger.info("Predictions: %s", result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()