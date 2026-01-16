"""
Network scanning utilities for Nkosi package.
Provides additional scanning methods for device discovery.
"""
import ipaddress
import subprocess
import platform
import time
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping(ip: str, timeout: float = 1) -> bool:
    """
    Ping a single IP address.
    
    Args:
        ip: IP address to ping
        timeout: Timeout in seconds
        
    Returns:
        True if host is reachable, False otherwise
    """
    try:
        # Different ping commands for different platforms
        if platform.system().lower() == 'windows':
            cmd = ['ping', '-n', '1', '-w', str(int(timeout * 1000)), ip]
        else:
            cmd = ['ping', '-c', '1', '-W', str(timeout), ip]
            
        # Run the ping command
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if platform.system().lower() == 'windows' else 0
        )
        
        # Check if ping was successful
        return result.returncode == 0 and 'unreachable' not in result.stdout.decode().lower()
        
    except Exception:
        return False

def ping_sweep(network: str = None, timeout: float = 2, max_workers: int = 32) -> List[str]:
    """
    Perform a ping sweep on the local network.
    
    Args:
        network: Network in CIDR notation (e.g., '192.168.1.0/24')
        timeout: Timeout in seconds for each ping
        max_workers: Maximum number of concurrent pings
        
    Returns:
        List of IP addresses that responded to ping
    """
    from .discovery import get_local_ip
    
    # If no network specified, use the local network
    if not network:
        local_ip = get_local_ip()
        if not local_ip or local_ip == '127.0.0.1':
            return []
        network = ".".join(local_ip.split(".")[:3]) + ".0/24"
    
    try:
        # Generate list of IPs to scan
        ips = [str(ip) for ip in ipaddress.IPv4Network(network, strict=False)]
    except Exception as e:
        print(f"Invalid network: {e}")
        return []
    
    responsive_ips = []
    
    # Use ThreadPoolExecutor for concurrent pings
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Start the ping operations
        future_to_ip = {executor.submit(ping, ip, timeout): ip for ip in ips}
        
        # Process results as they complete
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    responsive_ips.append(ip)
            except Exception as e:
                print(f"Error pinging {ip}: {e}")
    
    return responsive_ips

if __name__ == "__main__":
    # Test the ping sweep
    print("Starting ping sweep...")
    responsive = ping_sweep(timeout=1)
    print(f"Found {len(responsive)} responsive IPs:")
    for ip in sorted(responsive):
        print(f"- {ip}")
