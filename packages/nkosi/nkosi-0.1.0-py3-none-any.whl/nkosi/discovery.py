"""
Network device discovery module for Nkosi package.
Provides functionality to discover devices on the local network using ARP.
"""
import platform
import subprocess
import ipaddress
import socket
import re
from typing import List, Dict, Optional

def get_local_ip() -> str:
    """Get the local IP address of the machine."""
    try:
        # Create a socket connection to a public address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def get_network_devices() -> List[Dict[str, str]]:
    """
    Discover devices on the local network using ARP.
    
    Returns:
        List of dictionaries containing device information (ip, mac, hostname).
    """
    devices = []
    local_ip = get_local_ip()
    
    # Get network address (assuming /24 subnet)
    network = ".".join(local_ip.split(".")[:-1]) + ".0/24"
    
    # Platform-specific ARP commands
    if platform.system() == "Windows":
        return _scan_windows(network)
    else:  # Linux and macOS
        return _scan_unix(network)

def _scan_windows(network: str) -> List[Dict[str, str]]:
    """Scan network devices on Windows using arp -a."""
    devices = []
    try:
        # Run arp -a command
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=True)
        
        # Parse the output
        lines = result.stdout.splitlines()
        for line in lines:
            # Match IP and MAC address pattern
            match = re.search(r'((?:\d{1,3}\.){3}\d{1,3})\s+([0-9a-fA-F-]+)', line)
            if match:
                ip = match.group(1)
                mac = match.group(2).replace("-", ":").upper()
                if ip != "224.0.0.22" and ip != "224.0.0.251" and ip != "224.0.0.252":
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except (socket.herror, socket.gaierror):
                        hostname = "Unknown"
                    devices.append({"ip": ip, "mac": mac, "hostname": hostname})
    except Exception as e:
        print(f"Error scanning network: {e}")
    
    return devices

def _scan_unix(network: str) -> List[Dict[str, str]]:
    """Scan network devices on Unix-like systems using arp-scan."""
    devices = []
    try:
        # Try to use arp-scan if available
        result = subprocess.run(
            ["arp-scan", "--localnet", "--ignoredups", "--quiet"],
            capture_output=True, text=True, check=True
        )
        
        # Parse arp-scan output
        lines = result.stdout.splitlines()
        for line in lines[2:-3]:  # Skip header and footer
            parts = line.split()
            if len(parts) >= 2:
                ip = parts[0]
                mac = parts[1].upper()
                hostname = parts[2] if len(parts) > 2 else "Unknown"
                devices.append({"ip": ip, "mac": mac, "hostname": hostname})
    except (subprocess.SubprocessError, FileNotFoundError):
        # Fallback to basic ARP scanning
        try:
            result = subprocess.run(
                ["arp", "-a"], capture_output=True, text=True, check=True
            )
            
            # Parse arp -a output
            for line in result.stdout.splitlines():
                match = re.search(r'\(([0-9.]+)\) at ([0-9a-fA-F:]+)', line)
                if match:
                    ip = match.group(1)
                    mac = match.group(2).upper()
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except (socket.herror, socket.gaierror):
                        hostname = "Unknown"
                    devices.append({"ip": ip, "mac": mac, "hostname": hostname})
        except Exception as e:
            print(f"Error scanning network: {e}")
    
    return devices

def discover_devices(timeout: int = 2) -> List[Dict[str, str]]:
    """
    Discover devices on the local network.
    
    Args:
        timeout: Timeout in seconds for network operations.
        
    Returns:
        List of dictionaries containing device information.
    """
    # First, get the local network devices using ARP
    devices = get_network_devices()
    
    # Then try to get more information about each device
    for device in devices:
        try:
            # Try to get hostname if not already available
            if device.get("hostname") in ["Unknown", ""]:
                try:
                    hostname = socket.gethostbyaddr(device["ip"])[0]
                    device["hostname"] = hostname
                except (socket.herror, socket.gaierror):
                    pass
        except Exception:
            continue
    
    return devices
