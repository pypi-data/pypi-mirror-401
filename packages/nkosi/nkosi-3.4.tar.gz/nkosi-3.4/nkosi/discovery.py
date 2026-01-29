"""
Network device discovery module for Nkosi package.
Provides cross-platform functionality to discover devices on the local network.
"""
import platform
import subprocess
import ipaddress
import socket
import re
import sys
import time
from typing import List, Dict, Optional, Tuple

def is_linux() -> bool:
    """Check if the current platform is Linux."""
    return sys.platform.startswith('linux')

def is_windows() -> bool:
    """Check if the current platform is Windows."""
    return sys.platform.startswith('win')

def is_macos() -> bool:
    """Check if the current platform is macOS."""
    return sys.platform == 'darwin'

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
    Discover devices on the local network using the best available method.
    
    Returns:
        List of dictionaries containing device information (ip, mac, hostname).
    """
    try:
        local_ip = get_local_ip()
        if not local_ip or local_ip == "127.0.0.1":
            raise ValueError("Could not determine local IP address")
            
        # Try platform-specific methods first
        if is_windows():
            # Try Windows-specific method first
            devices = _scan_windows()
            if not devices:
                # Fall back to generic method if Windows-specific method fails
                print("Windows ARP scan returned no devices, trying generic method...")
                devices = _scan_generic()
            return devices
        elif is_linux():
            return _scan_linux()
        elif is_macos():
            return _scan_macos()
        else:
            # Fallback to generic method
            return _scan_generic()
    except Exception as e:
        print(f"Error during device discovery: {e}")
        return []

def _scan_windows() -> List[Dict[str, str]]:
    """Scan network devices on Windows using arp -a."""
    devices = []
    try:
        # First, get the local network prefix
        local_ip = get_local_ip()
        if not local_ip or local_ip == "127.0.0.1":
            print("Warning: Could not determine local IP address")
            return devices

        network_prefix = ".".join(local_ip.split(".")[:3]) + "."

        # Run arp -a command
        result = subprocess.run(
            ["arp", "-a"], 
            capture_output=True, 
            text=True, 
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Parse the output
        for line in result.stdout.splitlines():
            # Match IP and MAC address pattern
            match = re.search(r'((?:\d{1,3}\.){3}\d{1,3})\s+([0-9a-fA-F-]+)', line)
            if match:
                ip = match.group(1)
                # Only process IPs in the same subnet
                if ip.startswith(network_prefix):
                    mac = match.group(2).replace("-", ":").upper()
                    # Skip broadcast address and multicast addresses
                    if ip not in [f"{network_prefix}255", "224.0.0.22", "224.0.0.251", "224.0.0.252"]:
                        try:
                            hostname = _get_hostname(ip)
                            devices.append({"ip": ip, "mac": mac, "hostname": hostname})
                        except Exception as e:
                            print(f"Warning: Could not get hostname for {ip}: {e}")
                            devices.append({"ip": ip, "mac": mac, "hostname": "Unknown"})
                            
    except subprocess.CalledProcessError as e:
        print(f"ARP command failed: {e.stderr}")
    except Exception as e:
        print(f"Windows ARP scan failed: {e}")
    
    return devices

def _scan_linux() -> List[Dict[str, str]]:
    """Scan network devices on Linux systems."""
    devices = []
    
    # Try arp-scan first (requires root)
    try:
        result = subprocess.run(
            ["sudo", "arp-scan", "--localnet", "--ignoredups", "--quiet"],
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # Parse arp-scan output
        for line in result.stdout.splitlines()[2:-3]:  # Skip header and footer
            parts = line.split()
            if len(parts) >= 2:
                ip = parts[0]
                mac = parts[1].upper()
                hostname = parts[2] if len(parts) > 2 else _get_hostname(ip)
                devices.append({"ip": ip, "mac": mac, "hostname": hostname})
        return devices
    except (subprocess.SubprocessError, FileNotFoundError):
        pass  # Fall through to next method
    
    # Fallback to reading /proc/net/arp
    try:
        with open('/proc/net/arp', 'r') as f:
            next(f)  # Skip header
            for line in f:
                parts = line.split()
                if len(parts) >= 4 and parts[0] != 'IP':
                    ip = parts[0]
                    mac = parts[3].upper()
                    if mac != '00:00:00:00:00:00':  # Skip incomplete entries
                        hostname = _get_hostname(ip)
                        devices.append({"ip": ip, "mac": mac, "hostname": hostname})
        return devices
    except Exception as e:
        print(f"Linux ARP scan failed: {e}")
    
    return devices

def _scan_macos() -> List[Dict[str, str]]:
    """Scan network devices on macOS systems."""
    devices = []
    try:
        # Get the default gateway IP
        result = subprocess.run(
            ["netstat", "-rn"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # Parse the output to find the default gateway
        for line in result.stdout.splitlines():
            if 'default' in line and 'UGSc' in line:
                parts = line.split()
                if len(parts) >= 2:
                    gateway = parts[1]
                    # Get the network interface
                    result = subprocess.run(
                        ["netstat", "-rn"], 
                        capture_output=True, 
                        text=True, 
                        check=True
                    )
                    # Run arp -a for the interface
                    result = subprocess.run(
                        ["arp", "-a"], 
                        capture_output=True, 
                        text=True, 
                        check=True
                    )
                    
                    # Parse arp -a output
                    for line in result.stdout.splitlines():
                        match = re.search(r'\(([0-9.]+)\) at ([0-9a-fA-F:]+)', line)
                        if match:
                            ip = match.group(1)
                            mac = match.group(2).upper()
                            hostname = _get_hostname(ip)
                            devices.append({"ip": ip, "mac": mac, "hostname": hostname})
                    break
    except Exception as e:
        print(f"macOS ARP scan failed: {e}")
    
    return devices

def _scan_generic() -> List[Dict[str, str]]:
    """Generic network scanning using ICMP ping and ARP."""
    devices = []
    try:
        local_ip = get_local_ip()
        if not local_ip or local_ip == "127.0.0.1":
            return []
            
        # Get network prefix (assuming /24 subnet)
        network_prefix = ".".join(local_ip.split(".")[:-1])
        
        # Try to ping all IPs in the subnet
        for i in range(1, 255):
            ip = f"{network_prefix}.{i}"
            try:
                # Use a quick ping with timeout
                subprocess.run(
                    ["ping", "-c", "1", "-W", "1", ip],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=1
                )
                
                # If we get here, the host is up
                mac = _get_mac_address(ip)
                if mac and mac != '00:00:00:00:00:00':
                    hostname = _get_hostname(ip)
                    devices.append({"ip": ip, "mac": mac, "hostname": hostname})
            except Exception:
                continue
    except Exception as e:
        print(f"Generic scan failed: {e}")
    
    return devices

def _get_hostname(ip: str) -> str:
    """Get hostname from IP address."""
    try:
        return socket.getfqdn(ip) if ip != "127.0.0.1" else "localhost"
    except (socket.herror, socket.gaierror):
        return "Unknown"

def _get_mac_address(ip: str) -> str:
    """Get MAC address from IP using ARP."""
    try:
        if is_windows():
            result = subprocess.run(
                ["arp", "-a", ip],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            match = re.search(r'([0-9A-Fa-f]{2}[-:]){5}([0-9A-Fa-f]{2})', result.stdout)
            return match.group(0).upper() if match else ""
        else:
            result = subprocess.run(
                ["arp", "-n", ip],
                capture_output=True,
                text=True,
                check=True
            )
            parts = result.stdout.split()
            return parts[3].upper() if len(parts) > 3 else ""
    except Exception:
        return ""

def discover_devices(timeout: int = 10) -> List[Dict[str, str]]:
    """
    Discover devices on the local network with a timeout.
    
    Args:
        timeout: Maximum time in seconds to spend scanning (default: 10).
        
    Returns:
        List of dictionaries containing device information (ip, mac, hostname).
    """
    start_time = time.time()
    devices = []
    found_ips = set()
    
    def add_device(device):
        """Helper to add a device if it's not already in the list."""
        if device['ip'] not in found_ips:
            devices.append(device)
            found_ips.add(device['ip'])
    
    print(f"Starting device discovery with timeout of {timeout} seconds...")
    
    try:
        # Method 1: Try platform-specific method first
        print("Trying platform-specific discovery...")
        platform_devices = get_network_devices()
        for device in platform_devices:
            add_device(device)
        
        # Method 2: If no devices found or we have time, try the generic method
        if (not devices or time.time() - start_time < timeout / 2) and is_windows():
            print("Trying Windows-specific ARP scan...")
            try:
                win_devices = _scan_windows()
                for device in win_devices:
                    add_device(device)
            except Exception as e:
                print(f"Windows ARP scan failed: {e}")
        
        # Method 3: Try a quick ping sweep if we still have time
        if time.time() - start_time < timeout * 0.8:
            print("Trying ping sweep...")
            try:
                from .scanner import ping_sweep  # Assuming you'll create this
                pinged_ips = ping_sweep(timeout=min(5, max(1, timeout // 2)))
                for ip in pinged_ips:
                    if ip not in found_ips:
                        try:
                            mac = _get_mac_address(ip) or "Unknown"
                            hostname = _get_hostname(ip) or "Unknown"
                            add_device({"ip": ip, "mac": mac, "hostname": hostname})
                        except Exception as e:
                            print(f"Could not get details for {ip}: {e}")
            except ImportError:
                print("Ping sweep not available")
            except Exception as e:
                print(f"Ping sweep failed: {e}")
        
    except Exception as e:
        print(f"Error during device discovery: {e}")
    
    # Ensure we don't exceed the timeout
    elapsed = time.time() - start_time
    if elapsed >= timeout:
        print(f"Warning: Device discovery timed out after {timeout:.1f} seconds")
    
    print(f"Found {len(devices)} device(s) in {elapsed:.1f} seconds")
    return devices
    if not result_queue.empty():
        return result_queue.get()
    
    # If we get here, the scan timed out
    print(f"Warning: Device discovery timed out after {timeout} seconds")
    return []
