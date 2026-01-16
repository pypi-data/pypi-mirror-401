#!/usr/bin/env python3
"""PyXESXXN Command Line Interface.

This module provides a command-line interface for PyXESXXN, allowing users
to interact with the library through terminal commands.
"""

import argparse
import sys
import logging
from typing import Optional

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

logger = logging.getLogger('pyxesxxn-cli')

def main() -> int:
    """Main entry point for the PyXESXXN CLI.
    
    Returns:
        Exit code: 0 for success, non-zero for errors
    """
    parser = argparse.ArgumentParser(
        prog='pyxesxxn-cli',
        description='PyXESXXN Command Line Interface',
        epilog='For more information, visit https://github.com/pyxesxxn/pyxesxxn'
    )
    
    # Main command group
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Version command
    subparsers.add_parser('version', help='Show PyXESXXN version information')
    
    # Info command
    subparsers.add_parser('info', help='Show PyXESXXN library information')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check PyXESXXN installation and dependencies')
    check_parser.add_argument('--detailed', action='store_true', help='Show detailed dependency information')
    
    # Network commands
    network_parser = subparsers.add_parser('network', help='Network-related commands')
    network_subparsers = network_parser.add_subparsers(dest='network_command', help='Network subcommands')
    network_subparsers.add_parser('create', help='Create a new network')
    network_subparsers.add_parser('list', help='List available network templates')
    
    # Simulation commands
    sim_parser = subparsers.add_parser('simulate', help='Simulation-related commands')
    sim_parser.add_argument('--scenario', type=str, help='Path to scenario file')
    sim_parser.add_argument('--output', type=str, help='Output directory for simulation results')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'version':
            return handle_version()
        elif args.command == 'info':
            return handle_info()
        elif args.command == 'check':
            return handle_check(args.detailed)
        elif args.command == 'network':
            return handle_network(args.network_command)
        elif args.command == 'simulate':
            return handle_simulate(args.scenario, args.output)
        else:
            logger.error(f"Unknown command: {args.command}")
            parser.print_help()
            return 1
    
    except Exception as e:
        logger.error(f"Error executing command: {str(e)}")
        return 1

def handle_version() -> int:
    """Handle version command."""
    from pyxesxxn.version import __version__, get_version_info
    
    print(f"PyXESXXN Version: {__version__}")
    print(f"Version Info: {get_version_info()}")
    return 0

def handle_info() -> int:
    """Handle info command."""
    from pyxesxxn import __author__, __copyright__
    
    print("PyXESXXN - Python for eXtended Energy System Analysis")
    print("=" * 50)
    print(f"Author: {__author__}")
    print(f"Copyright: {__copyright__}")
    print("Description: A fully independent multi-carrier energy system modeling and optimization library")
    print("License: Proprietary - Free for use, closed source")
    return 0

def handle_check(detailed: bool = False) -> int:
    """Handle check command."""
    print("Checking PyXESXXN installation...")
    
    # Import core modules to verify installation
    try:
        import pyxesxxn as px
        print("✓ PyXESXXN core module imported successfully")
        
        if detailed:
            print("\nChecking dependencies...")
            check_dependencies()
            
        return 0
    except ImportError as e:
        print(f"✗ PyXESXXN import failed: {e}")
        return 1

def check_dependencies() -> None:
    """Check and display dependency information."""
    dependencies = [
        'numpy', 'scipy', 'pandas', 'xarray', 'matplotlib',
        'plotly', 'seaborn', 'geopandas', 'shapely', 'networkx',
        'scikit-learn', 'pyyaml', 'highspy'
    ]
    
    for dep in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✓ {dep}: {version}")
        except ImportError:
            print(f"  ✗ {dep}: Not installed")

def handle_network(subcommand: Optional[str]) -> int:
    """Handle network commands."""
    if not subcommand:
        print("Network subcommand required. Available subcommands: create, list")
        return 1
    
    if subcommand == 'create':
        print("Network creation not fully implemented yet.")
        print("Use Python API: import pyxesxxn as px; network = px.Network()")
    elif subcommand == 'list':
        print("Available network templates:")
        print("  - default: Basic electricity network")
        print("  - urban: Urban energy system with multiple carriers")
        print("  - rural: Rural energy system with renewable focus")
    
    return 0

def handle_simulate(scenario: Optional[str], output: Optional[str]) -> int:
    """Handle simulate command."""
    print(f"Simulation command executed with scenario={scenario}, output={output}")
    print("Simulation functionality not fully implemented yet.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
