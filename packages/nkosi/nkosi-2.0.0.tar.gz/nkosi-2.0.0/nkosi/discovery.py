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
            return _scan_windows()
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
                mac = match.group(2).replace("-", ":").upper()
                if ip not in ["224.0.0.22", "224.0.0.251", "224.0.0.252"]:
                    hostname = _get_hostname(ip)
                    devices.append({"ip": ip, "mac": mac, "hostname": hostname})
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

def discover_devices(timeout: int = 2) -> List[Dict[str, str]]:
    """
    Discover devices on the local network with a timeout.
    
    Args:
        timeout: Maximum time in seconds to spend scanning.
        
    Returns:
        List of dictionaries containing device information (ip, mac, hostname).
    """
    import threading
    from queue import Queue
    
    result_queue = Queue()
    
    def _scan_thread():
        try:
            devices = get_network_devices()
            result_queue.put(devices)
        except Exception as e:
            print(f"Error during device discovery: {e}")
            result_queue.put([])
    
    # Start the scan in a separate thread
    scan_thread = threading.Thread(target=_scan_thread)
    scan_thread.daemon = True
    scan_thread.start()
    
    # Wait for the scan to complete or timeout
    scan_thread.join(timeout=timeout)
    
    # Get results if available
    if not result_queue.empty():
        return result_queue.get()
    
    # If we get here, the scan timed out
    print(f"Warning: Device discovery timed out after {timeout} seconds")
    return []
