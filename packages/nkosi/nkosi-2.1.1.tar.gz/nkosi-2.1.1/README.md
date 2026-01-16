# Nkosi

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Nkosi is a Python package for network device discovery and communication. It provides tools to:

- Discover devices on your local network using ARP
- Establish TCP/UDP communication channels
- Create network servers and clients with minimal code
- Send and receive messages between devices

## Features

- **Device Discovery**: Find all devices on your local network using ARP scanning
- **TCP Communication**: Full-featured TCP server and client implementations
- **UDP Communication**: UDP server and client with broadcast support
- **Easy to Use**: Simple API for common networking tasks
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

```bash
pip install nkosi
```

## Quick Start

### Discovering Devices on Your Network

```python
from nkosi import discover_devices

devices = discover_devices()
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}, Hostname: {device['hostname']}")
```

### Creating a TCP Server

```python
from nkosi import TCPServer

def on_message_received(message, client_address):
    print(f"Received from {client_address}: {message}")

server = TCPServer(host='0.0.0.0', port=5000)
server.start(callback=on_message_received)

# Keep the server running
input("Press Enter to stop the server...")
server.stop()
```

### Creating a TCP Client

```python
from nkosi import TCPClient

def on_message_received(message):
    print(f"Received from server: {message}")

client = TCPClient(host='localhost', port=5000)
if client.connect(callback=on_message_received):
    client.send({"type": "greeting", "message": "Hello, server!"})
    
    # Keep the client running
    input("Press Enter to disconnect...")
    client.disconnect()
```

### Creating a UDP Server

```python
from nkosi import UDPServer

def on_message_received(message, client_address):
    print(f"Received from {client_address}: {message}")

server = UDPServer(host='0.0.0.0', port=5001)
server.start(callback=on_message_received)

# Keep the server running
input("Press Enter to stop the server...")
server.stop()
```

### Creating a UDP Client

```python
from nkosi import UDPClient

def on_message_received(message, sender_address):
    print(f"Received from {sender_address}: {message}")

client = UDPClient(host='localhost', port=5001)
if client.start(callback=on_message_received):
    client.send({"type": "greeting", "message": "Hello, server!"})
    
    # Keep the client running
    input("Press Enter to stop the client...")
    client.stop()
```

## Command Line Interface

Nkosi also provides a simple command-line interface for common tasks.

### Discover Devices

```bash
nkosi-discover
```

### Send a Message

```bash
# Send a message to a TCP server
nkosi-send --host localhost --port 5000 --message "Hello, server!" --protocol tcp

# Send a message to a UDP server
nkosi-send --host localhost --port 5001 --message "Hello, server!" --protocol udp
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
