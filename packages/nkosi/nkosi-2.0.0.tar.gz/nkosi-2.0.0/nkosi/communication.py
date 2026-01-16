"""
Network communication module for Nkosi package.
Provides TCP and UDP server/client implementations with file transfer support.
"""
import socket
import threading
import json
import os
import hashlib
import time
import struct
from typing import Callable, Optional, Dict, Any, Union, Tuple, BinaryIO
from pathlib import Path

# Constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
BUFFER_SIZE = 4096
TIMEOUT = 5  # seconds

class TransferStatus:
    """Status of a file transfer."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class FileTransfer:
    """Represents a file transfer operation."""
    
    def __init__(self, filename: str, filesize: int, transfer_id: str = None):
        self.filename = filename
        self.filesize = filesize
        self.transfer_id = transfer_id or hashlib.md5(f"{filename}{time.time()}".encode()).hexdigest()
        self.bytes_transferred = 0
        self.status = TransferStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.speed = 0
        self.error = None
    
    def start(self):
        """Mark the transfer as started."""
        self.status = TransferStatus.IN_PROGRESS
        self.start_time = time.time()
    
    def update_progress(self, bytes_transferred: int):
        """Update the transfer progress."""
        self.bytes_transferred = bytes_transferred
        if self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                self.speed = bytes_transferred / elapsed  # bytes per second
    
    def complete(self):
        """Mark the transfer as completed."""
        self.status = TransferStatus.COMPLETED
        self.bytes_transferred = self.filesize
        self.end_time = time.time()
        if self.start_time and self.end_time > self.start_time:
            self.speed = self.filesize / (self.end_time - self.start_time)
    
    def fail(self, error: str):
        """Mark the transfer as failed."""
        self.status = TransferStatus.FAILED
        self.error = error
        self.end_time = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the transfer to a dictionary."""
        return {
            "transfer_id": self.transfer_id,
            "filename": self.filename,
            "filesize": self.filesize,
            "bytes_transferred": self.bytes_transferred,
            "status": self.status,
            "progress": (self.bytes_transferred / self.filesize) * 100 if self.filesize > 0 else 0,
            "speed": self.speed,
            "error": self.error
        }

class TCPServer:
    """TCP Server implementation for handling multiple client connections with file transfer support."""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 5000):
        """
        Initialize the TCP server.
        
        Args:
            host: Host IP to bind to (default: '0.0.0.0' for all interfaces)
            port: Port to listen on (default: 5000)
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.running = False
        self.callback = None
        self.file_callback = None
        self.transfers = {}  # Active file transfers
        self.save_dir = "received_files"
        
        # Create save directory if it doesn't exist
        os.makedirs(self.save_dir, exist_ok=True)
    
    def start(self, callback: Optional[Callable[[Dict[str, Any], str], None]] = None) -> None:
        """
        Start the TCP server.
        
        Args:
            callback: Function to call when a message is received.
                     The callback should accept two parameters: the message and the client address.
        """
        self.callback = callback
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        print(f"TCP Server listening on {self.host}:{self.port}")
        
        # Start accepting connections in a new thread
        self.accept_thread = threading.Thread(target=self._accept_connections)
        self.accept_thread.daemon = True
        self.accept_thread.start()
    
    def _accept_connections(self):
        """Accept incoming client connections."""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from {client_address}")
                
                # Store client socket
                self.clients[client_address] = client_socket
                
                # Start a new thread to handle the client
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except OSError as e:
                if self.running:
                    print(f"Error accepting connection: {e}")
                break
    
    def _handle_client(self, client_socket: socket.socket, client_address: tuple):
        """Handle communication with a connected client."""
        try:
            while self.running:
                # Receive data from client
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    # Try to decode JSON data
                    message = json.loads(data.decode('utf-8'))
                    if self.callback:
                        self.callback(message, f"{client_address[0]}:{client_address[1]}")
                except json.JSONDecodeError:
                    # If not JSON, treat as raw data
                    if self.callback:
                        self.callback({"data": data.decode('utf-8', errors='replace')}, 
                                   f"{client_address[0]}:{client_address[1]}")
                        
        except ConnectionResetError:
            print(f"Client {client_address} disconnected unexpectedly")
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            # Clean up
            client_socket.close()
            if client_address in self.clients:
                del self.clients[client_address]
            print(f"Client {client_address} disconnected")
    
    def send_to_client(self, client_address: str, message: Union[dict, str, bytes]):
        """
        Send a message to a specific client.
        
        Args:
            client_address: The address of the client in 'ip:port' format
            message: The message to send (dict will be JSON-encoded)
        """
        try:
            # Find the client socket
            ip, port = client_address.split(':')
            target_address = (ip, int(port))
            
            if target_address not in self.clients:
                print(f"Client {client_address} not found")
                return False
                
            client_socket = self.clients[target_address]
            
            # Prepare the message
            if isinstance(message, dict):
                data = json.dumps(message).encode('utf-8')
            elif isinstance(message, str):
                data = message.encode('utf-8')
            else:  # bytes
                data = message
                
            # Send the data
            client_socket.sendall(data)
            return True
            
        except Exception as e:
            print(f"Error sending to client {client_address}: {e}")
            return False
    
    def broadcast(self, message: Union[dict, str, bytes]):
        """
        Send a message to all connected clients.
        
        Args:
            message: The message to broadcast (dict will be JSON-encoded)
        """
        disconnected_clients = []
        
        # Prepare the message
        if isinstance(message, dict):
            data = json.dumps(message).encode('utf-8')
        elif isinstance(message, str):
            data = message.encode('utf-8')
        else:  # bytes
            data = message
        
        # Send to all clients
        for client_address, client_socket in list(self.clients.items()):
            try:
                client_socket.sendall(data)
            except (ConnectionError, OSError):
                disconnected_clients.append(client_address)
        
        # Remove disconnected clients
        for addr in disconnected_clients:
            if addr in self.clients:
                self.clients[addr].close()
                del self.clients[addr]
    
    def stop(self):
        """Stop the TCP server and close all connections."""
        self.running = False
        
        # Close all client connections
        for client_socket in self.clients.values():
            try:
                client_socket.close()
            except:
                pass
        
        # Close the server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("TCP Server stopped")


class TCPClient:
    """TCP Client implementation for connecting to TCP servers with file transfer support."""
    
    def __init__(self, host: str = 'localhost', port: int = 5000):
        """
        Initialize the TCP client.
        
        Args:
            host: Server hostname or IP address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.callback = None
        self.file_callback = None
        self.receive_thread = None
        self.transfers = {}  # Active file transfers
        self.save_dir = "received_files"
        
        # Create save directory if it doesn't exist
        os.makedirs(self.save_dir, exist_ok=True)
    
    def connect(self, callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> bool:
        """
        Connect to the TCP server.
        
        Args:
            callback: Function to call when a message is received.
                     The callback should accept one parameter: the message.
        """
        self.callback = callback
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            
            # Start receiving messages in a new thread
            self.receive_thread = threading.Thread(target=self._receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            print(f"Connected to {self.host}:{self.port}")
            return True
            
        except Exception as e:
            print(f"Failed to connect to {self.host}:{self.port}: {e}")
            self.connected = False
            return False
    
    def _receive_messages(self):
        """Receive messages from the server."""
        while self.connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    self.connected = False
                    print("Connection closed by server")
                    break
                
                if self.callback:
                    try:
                        # Try to decode JSON data
                        message = json.loads(data.decode('utf-8'))
                        self.callback(message)
                    except json.JSONDecodeError:
                        # If not JSON, treat as raw data
                        self.callback({"data": data.decode('utf-8', errors='replace')})
                        
            except ConnectionResetError:
                self.connected = False
                print("Connection reset by server")
                break
            except Exception as e:
                if self.connected:  # Only log if we didn't intentionally disconnect
                    print(f"Error receiving data: {e}")
                break
    
    def send(self, message: Union[dict, str, bytes]) -> bool:
        """
        Send a message to the server.
        
        Args:
            message: The message to send (dict will be JSON-encoded)
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        if not self.connected or not self.socket:
            print("Not connected to server")
            return False
        
        try:
            # Prepare the message
            if isinstance(message, dict):
                data = json.dumps(message).encode('utf-8')
            elif isinstance(message, str):
                data = message.encode('utf-8')
            else:  # bytes
                data = message
            
            # Send the data
            self.socket.sendall(data)
            return True
            
        except Exception as e:
            print(f"Error sending message: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the server."""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        print("Disconnected from server")


class UDPServer:
    """UDP Server implementation for connectionless communication."""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 5001):
        """
        Initialize the UDP server.
        
        Args:
            host: Host IP to bind to (default: '0.0.0.0' for all interfaces)
            port: Port to listen on (default: 5001)
        """
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.callback = None
    
    def start(self, callback: Optional[Callable[[Dict[str, Any], str], None]] = None) -> None:
        """
        Start the UDP server.
        
        Args:
            callback: Function to call when a message is received.
                     The callback should accept two parameters: the message and the client address.
        """
        self.callback = callback
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        
        print(f"UDP Server listening on {self.host}:{self.port}")
        
        # Start receiving in a new thread
        self.receive_thread = threading.Thread(target=self._receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()
    
    def _receive_messages(self):
        """Receive incoming UDP messages."""
        while self.running:
            try:
                data, addr = self.socket.recvfrom(65535)  # Max UDP packet size
                
                try:
                    # Try to decode JSON data
                    message = json.loads(data.decode('utf-8'))
                    if self.callback:
                        self.callback(message, f"{addr[0]}:{addr[1]}")
                except json.JSONDecodeError:
                    # If not JSON, treat as raw data
                    if self.callback:
                        self.callback({"data": data.decode('utf-8', errors='replace')}, 
                                   f"{addr[0]}:{addr[1]}")
                        
            except OSError as e:
                if self.running:
                    print(f"Error receiving UDP message: {e}")
                break
            except Exception as e:
                print(f"Error processing UDP message: {e}")
    
    def send(self, address: str, message: Union[dict, str, bytes]) -> bool:
        """
        Send a UDP message to a specific address.
        
        Args:
            address: The target address in 'ip:port' format
            message: The message to send (dict will be JSON-encoded)
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        if not self.socket:
            return False
            
        try:
            ip, port = address.split(':')
            
            # Prepare the message
            if isinstance(message, dict):
                data = json.dumps(message).encode('utf-8')
            elif isinstance(message, str):
                data = message.encode('utf-8')
            else:  # bytes
                data = message
            
            # Send the data
            self.socket.sendto(data, (ip, int(port)))
            return True
            
        except Exception as e:
            print(f"Error sending UDP message to {address}: {e}")
            return False
    
    def broadcast(self, port: int, message: Union[dict, str, bytes], subnet: str = "255.255.255.255") -> bool:
        """
        Broadcast a UDP message to all devices on the local network.
        
        Args:
            port: The target port
            message: The message to send (dict will be JSON-encoded)
            subnet: The broadcast address (default: 255.255.255.255)
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        if not self.socket:
            return False
            
        try:
            # Enable broadcasting
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # Prepare the message
            if isinstance(message, dict):
                data = json.dumps(message).encode('utf-8')
            elif isinstance(message, str):
                data = message.encode('utf-8')
            else:  # bytes
                data = message
            
            # Send the broadcast
            self.socket.sendto(data, (subnet, port))
            return True
            
        except Exception as e:
            print(f"Error broadcasting UDP message: {e}")
            return False
        finally:
            # Disable broadcasting
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
    
    def stop(self):
        """Stop the UDP server."""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        print("UDP Server stopped")


class UDPClient:
    """UDP Client implementation for sending datagrams to UDP servers."""
    
    def __init__(self, host: str = 'localhost', port: int = 5001):
        """
        Initialize the UDP client.
        
        Args:
            host: Server hostname or IP address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.callback = None
    
    def start(self, callback: Optional[Callable[[Dict[str, Any], str], None]] = None) -> bool:
        """
        Start the UDP client.
        
        Args:
            callback: Function to call when a message is received.
                     The callback should accept two parameters: the message and the sender address.
        """
        self.callback = callback
        self.running = True
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # If a callback is provided, bind to a random port to receive responses
            if callback:
                self.socket.bind(('', 0))  # Bind to any available port
                
                # Start receiving in a new thread
                self.receive_thread = threading.Thread(target=self._receive_messages)
                self.receive_thread.daemon = True
                self.receive_thread.start()
            
            print(f"UDP Client ready on {self.socket.getsockname()[0]}:{self.socket.getsockname()[1]}")
            return True
            
        except Exception as e:
            print(f"Error starting UDP client: {e}")
            self.running = False
            return False
    
    def _receive_messages(self):
        """Receive incoming UDP messages."""
        while self.running and self.socket:
            try:
                data, addr = self.socket.recvfrom(65535)  # Max UDP packet size
                
                if self.callback:
                    try:
                        # Try to decode JSON data
                        message = json.loads(data.decode('utf-8'))
                        self.callback(message, f"{addr[0]}:{addr[1]}")
                    except json.JSONDecodeError:
                        # If not JSON, treat as raw data
                        self.callback({"data": data.decode('utf-8', errors='replace')}, 
                                   f"{addr[0]}:{addr[1]}")
                        
            except OSError as e:
                if self.running:
                    print(f"Error receiving UDP message: {e}")
                break
            except Exception as e:
                print(f"Error processing UDP message: {e}")
    
    def send(self, message: Union[dict, str, bytes], host: Optional[str] = None, port: Optional[int] = None) -> bool:
        """
        Send a UDP message.
        
        Args:
            message: The message to send (dict will be JSON-encoded)
            host: Optional host to send to (defaults to the host provided in __init__)
            port: Optional port to send to (defaults to the port provided in __init__)
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        if not self.socket:
            return False
            
        target_host = host or self.host
        target_port = port or self.port
        
        try:
            # Prepare the message
            if isinstance(message, dict):
                data = json.dumps(message).encode('utf-8')
            elif isinstance(message, str):
                data = message.encode('utf-8')
            else:  # bytes
                data = message
            
            # Send the data
            self.socket.sendto(data, (target_host, target_port))
            return True
            
        except Exception as e:
            print(f"Error sending UDP message to {target_host}:{target_port}: {e}")
            return False
    
    def broadcast(self, port: int, message: Union[dict, str, bytes], subnet: str = "255.255.255.255") -> bool:
        """
        Broadcast a UDP message to all devices on the local network.
        
        Args:
            port: The target port
            message: The message to send (dict will be JSON-encoded)
            subnet: The broadcast address (default: 255.255.255.255)
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        if not self.socket:
            return False
            
        try:
            # Enable broadcasting
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # Prepare the message
            if isinstance(message, dict):
                data = json.dumps(message).encode('utf-8')
            elif isinstance(message, str):
                data = message.encode('utf-8')
            else:  # bytes
                data = message
            
            # Send the broadcast
            self.socket.sendto(data, (subnet, port))
            return True
            
        except Exception as e:
            print(f"Error broadcasting UDP message: {e}")
            return False
        finally:
            # Disable broadcasting
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
    
    def stop(self):
        """Stop the UDP client."""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        print("UDP Client stopped")
