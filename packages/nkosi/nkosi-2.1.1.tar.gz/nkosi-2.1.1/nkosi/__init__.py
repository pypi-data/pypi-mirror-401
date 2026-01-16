"""
Nkosi - Network Discovery and Communication Package

A Python package for discovering devices on local networks and establishing
network communication channels using TCP/UDP protocols.
"""

__version__ = "2.1.1"

from .discovery import discover_devices
from .communication import TCPServer, TCPClient, UDPServer, UDPClient
from .visualizer import *

__all__ = [
    'discover_devices', 
    'TCPServer', 
    'TCPClient', 
    'UDPServer', 
    'UDPClient',
    'OSIVisualizer',
    'main'
]
