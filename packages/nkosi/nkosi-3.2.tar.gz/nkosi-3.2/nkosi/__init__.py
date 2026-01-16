"""
Nkosi - Network Discovery and Communication Package

A Python package for discovering devices on local networks and establishing
network communication channels using TCP/UDP protocols.
"""

__version__ = "3.2"

from .discovery import discover_devices, get_network_devices, get_local_ip
from .communication import TCPServer, TCPClient, UDPServer, UDPClient
from .visualizer import *
from .scanner import ping, ping_sweep

__all__ = [
    'discover_devices',
    'get_network_devices',
    'get_local_ip',
    'ping',
    'ping_sweep',
    'TCPServer',
    'TCPClient',
    'UDPServer',
    'UDPClient',
    'OSIVisualizer',
    'main'
]
