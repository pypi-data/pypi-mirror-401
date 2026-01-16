"""
Command Line Interface for Nkosi Network Tools.
"""
import argparse
import sys
from .visualizer import main as visualizer_main

def discover_devices():
    """Discover and list devices on the local network."""
    from .discovery import discover_devices
    
    print("Discovering devices on the local network...")
    devices = discover_devices()
    
    if not devices:
        print("No devices found on the local network.")
        return
    
    print("\nFound the following devices:")
    print("-" * 70)
    print(f"{'IP Address':<15} {'MAC Address':<20} {'Hostname'}")
    print("-" * 70)
    
    for device in devices:
        ip = device.get('ip', 'Unknown')
        mac = device.get('mac', 'Unknown')
        hostname = device.get('hostname', 'Unknown')
        print(f"{ip:<15} {mac:<20} {hostname}")

def start_visualizer():
    """Start the OSI Model Visualizer."""
    print("Starting OSI Model Visualizer...")
    print("Press Ctrl+C to exit\n")
    visualizer_main()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Nkosi Network Tools')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover devices on the local network')
    
    # Visualizer command
    visualizer_parser = subparsers.add_parser('visualize', help='Start the OSI Model Visualizer')
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    return parser.parse_args()

def main():
    """Main entry point for the command line interface."""
    args = parse_args()
    
    if args.command == 'discover':
        discover_devices()
    elif args.command == 'visualize':
        start_visualizer()
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
