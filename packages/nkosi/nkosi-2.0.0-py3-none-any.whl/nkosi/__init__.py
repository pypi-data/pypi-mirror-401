"""
Nkosi - Network Discovery and Communication Package

A Python package for discovering devices on local networks and establishing
network communication channels using TCP/UDP protocols.
"""

__version__ = "0.1.0"

from .discovery import discover_devices
from .communication import TCPServer, TCPClient, UDPServer, UDPClient

__all__ = ['discover_devices', 'TCPServer', 'TCPClient', 'UDPServer', 'UDPClient']
