try:
    # Try absolute import first (when running as a module)
    from nkosi.cli import discover_devices
except ImportError:
    # Fall back to relative import (when running directly)
    from .cli import discover_devices

if __name__ == "__main__":
    discover_devices()
