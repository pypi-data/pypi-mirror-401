"""
Command-line interface for cph-regression package.

This module provides the main CLI entry point for training regression models.
"""

import sys
from pathlib import Path
from cph_regression.regression.cli import RGSLightningCLI
from cph_regression.regression.mainfittest import cli_main as fit_test_main


def main():
    """
    Main CLI entry point.
    
    Supports:
    - cph-regression --config config.yaml (fit + test)
    - cph-regression fit --config config.yaml (training only)
    - cph-regression test --config config.yaml (testing only)
    """
    # Check if subcommand is provided (fit, test, predict)
    if len(sys.argv) > 1 and sys.argv[1] in ['fit', 'test', 'predict']:
        # Use Lightning CLI for subcommands
        # The Lightning CLI will handle --config and other arguments
        cli = RGSLightningCLI()
    else:
        # Default: run fit + test workflow
        # Check if --config is provided
        if '--config' not in sys.argv:
            print("Error: --config argument is required")
            print("Usage: cph-regression --config <config.yaml>")
            print("   or: cph-regression fit --config <config.yaml>")
            print("   or: cph-regression test --config <config.yaml>")
            sys.exit(1)
        
        # Find config path
        config_idx = sys.argv.index('--config')
        if config_idx + 1 >= len(sys.argv):
            print("Error: --config requires a path argument")
            sys.exit(1)
        
        config_path = Path(sys.argv[config_idx + 1]).resolve()
        if not config_path.exists():
            print(f"Error: Config file not found: {config_path}")
            sys.exit(1)
        
        # Run fit + test workflow
        # The mainfittest will parse sys.argv for --config
        fit_test_main()


if __name__ == "__main__":
    main()
