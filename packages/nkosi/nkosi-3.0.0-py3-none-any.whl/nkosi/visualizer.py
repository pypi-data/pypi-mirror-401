"""
OSI Model Visualization Tool with real network integration.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import threading
import json
import os
import shutil
import queue
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
from pathlib import Path
from .discovery import discover_devices
from .communication import TCPServer, TCPClient, UDPServer, UDPClient, FileTransfer, TransferStatus

class OSIVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("OSI Model Flow Simulator with Real Network")
        self.root.geometry("1000x700")
        
        # Network components
        self.devices = []
        self.selected_device = None
        self.tcp_server = None
        self.udp_server = None
        self.client = None
        self.protocol = "TCP"  # Default protocol
        self.active_transfers: Dict[str, FileTransfer] = {}
        
        # Create received files directory
        self.received_files_dir = Path("received_files")
        self.received_files_dir.mkdir(exist_ok=True)
        
        # Queue for thread-safe UI updates
        self.message_queue = queue.Queue()
        self.process_queue()
        
        self.build_ui()
        self.start_servers()
        self.discover_network_devices()
    
    def build_ui(self):
        # Main layout
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls
        self.left_panel = ttk.Frame(self.main_pane, width=250, padding=10)
        self.main_pane.add(self.left_panel, weight=0)
        
        # Center panel - OSI Layers
        self.center_panel = ttk.Frame(self.main_pane, padding=10)
        self.main_pane.add(self.center_panel, weight=1)
        
        # Bottom panel - Logs
        self.bottom_panel = ttk.Frame(self.root, height=150)
        self.bottom_panel.pack(fill=tk.BOTH, expand=False)
        
        self.build_controls()
        self.build_osi_layers()
        self.build_logs()
    
    def build_controls(self):
        # Network Controls
        ttk.Label(self.left_panel, text="Network Devices", font=("Arial", 12, "bold")).pack(pady=(0, 10), anchor=tk.W)
        
        # Search frame
        search_frame = ttk.Frame(self.left_panel)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Search entry
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        search_entry.bind('<KeyRelease>', self._filter_devices)
        
        # Refresh button
        refresh_btn = ttk.Button(
            search_frame,
            text="↻",
            width=3,
            command=self.discover_network_devices,
            style='Accent.TButton'
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # Devices list container
        list_container = ttk.Frame(self.left_panel)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for devices list
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Devices listbox
        self.devices_listbox = tk.Listbox(
            list_container,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            font=('Consolas', 9),
            relief=tk.FLAT
        )
        self.devices_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.devices_listbox.yview)
        self.devices_listbox.bind('<<ListboxSelect>>', self.on_device_select)
        
        # Status bar
        self.status_bar = ttk.Label(
            self.left_panel,
            text="Ready",
            style='Status.TLabel',
            anchor='w'
        )
        self.status_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Protocol Section
        ttk.Label(self.left_panel, text="Protocol", style='Section.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        # Protocol selection
        protocol_frame = ttk.Frame(self.left_panel)
        protocol_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.protocol_var = tk.StringVar(value="TCP")
        ttk.Radiobutton(protocol_frame, 
                       text="TCP", 
                       variable=self.protocol_var, 
                       value="TCP",
                       command=self.on_protocol_change).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(protocol_frame, 
                       text="UDP", 
                       variable=self.protocol_var, 
                       value="UDP",
                       command=self.on_protocol_change).pack(side=tk.LEFT)
        
        # Message Section
        ttk.Label(self.left_panel, text="Message", style='Section.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        # Message input
        self.message_entry = ttk.Entry(self.left_panel)
        self.message_entry.pack(fill=tk.X, pady=(0, 10))
        self.message_entry.insert(0, "Hello, OSI Model!")
        
        # Action Buttons
        btn_frame = ttk.Frame(self.left_panel)
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.send_btn = ttk.Button(
            btn_frame,
            text="Send Message",
            command=self.send_message,
            style='Accent.TButton'
        )
        self.send_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.file_btn = ttk.Button(
            btn_frame,
            text="📎",
            width=3,
            command=self.send_file_dialog
        )
        self.file_btn.pack(side=tk.RIGHT)
        
        # Initially disable action buttons until device is selected
        self.send_btn.config(state=tk.DISABLED)
        self.file_btn.config(state=tk.DISABLED)
    
    def _configure_styles(self):
        """Configure ttk styles for the application."""
        style = ttk.Style()
        
        # Configure the main window style
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        
        # Configure listbox
        style.configure('Listbox',
                      background='white',
                      foreground='black',
                      selectbackground='#0078d7',
                      selectforeground='white',
                      font=('Consolas', 9),
                      borderwidth=1,
                      relief='solid')
        
        # Configure buttons
        style.configure('TButton', padding=5)
        style.configure('Accent.TButton',
                       background='#0078d7',
                       foreground='white',
                       font=('Segoe UI', 9, 'bold'))
        
        # Configure status bar
        style.configure('Status.TLabel',
                      background='#e0e0e0',
                      foreground='#333333',
                      padding=5,
                      font=('Arial', 8),
                      anchor='w')
        
        # Configure section headers
        style.configure('Section.TLabel',
                      font=('Arial', 10, 'bold'),
                      foreground='#2c3e50')
        
        # Configure entry fields
        style.configure('TEntry',
                      fieldbackground='white',
                      padding=3)
    
    def build_osi_layers(self):
        self.layer_frames = {}
        self.layer_vars = {}
        
        # OSI Layers in order from top to bottom
        layers = [
            ("Application", "HTTP/FTP/SMTP"),
            ("Presentation", "SSL/TLS/JPEG/MP3"),
            ("Session", "API/Socket"),
            ("Transport", "TCP/UDP"),
            ("Network", "IP/ICMP"),
            ("Data Link", "Ethernet/PPP"),
            ("Physical", "WiFi/Cable")
        ]
        
        for layer_name, protocols in layers:
            # Create frame for each layer
            frame = ttk.LabelFrame(self.center_panel, text=f"{layer_name} Layer")
            frame.pack(fill=tk.X, padx=5, pady=2, ipady=5)
            
            # Protocol label
            ttk.Label(frame, text=protocols, font=('Arial', 9, 'italic')).pack(side=tk.LEFT, padx=5)
            
            # Data label (will be updated during simulation)
            data_var = tk.StringVar()
            data_label = ttk.Label(frame, textvariable=data_var, wraplength=600, justify=tk.LEFT)
            data_label.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
            
            self.layer_frames[layer_name] = frame
            self.layer_vars[layer_name] = data_var
    
    def build_logs(self):
        # Log frame
        log_frame = ttk.LabelFrame(self.bottom_panel, text="Simulation Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log text area with scrollbar
        log_scroll = ttk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, yscrollcommand=log_scroll.set)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
        
        # Configure tags for different log levels
        self.log_text.tag_config('INFO', foreground='black')
        self.log_text.tag_config('SUCCESS', foreground='green')
        self.log_text.tag_config('WARNING', foreground='orange')
        self.log_text.tag_config('ERROR', foreground='red')
    
    def log(self, message: str, level: str = 'INFO'):
        """Add a message to the log with the specified level."""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", level)
        self.log_text.see(tk.END)
    
    def highlight_layer(self, layer_name: str, highlight: bool = True):
        """Highlight or unhighlight a layer."""
        frame = self.layer_frames[layer_name]
        if highlight:
            frame.config(style='Highlight.TLabelframe')
        else:
            frame.config(style='TLabelframe')
        self.root.update()
    
    def update_layer_data(self, layer_name: str, data: str):
        """Update the data displayed in a layer."""
        self.layer_vars[layer_name].set(data)
        self.log(f"{layer_name}: {data}")
    
    def _enable_ui_controls(self):
        """Re-enable UI controls after scan completes."""
        for widget in self.left_panel.winfo_children():
            if isinstance(widget, (ttk.Button, ttk.Radiobutton)):
                if widget != self.refresh_btn:  # Keep refresh button enabled
                    widget.config(state=tk.NORMAL)

    def discover_network_devices(self):
        """Discover devices on the local network with progress feedback."""
        self.devices_listbox.delete(0, tk.END)
        self.devices_listbox.insert(tk.END, "Scanning network...")
        self.status_bar.config(text="Scanning network...")
        
        # Disable UI controls during scan
        for widget in self.left_panel.winfo_children():
            if isinstance(widget, (ttk.Button, ttk.Radiobutton)) and widget != self.refresh_btn:
                widget.config(state=tk.DISABLED)
        
        def scan():
            try:
                start_time = time.time()
                
                # Update UI with scanning status
                self.root.after(0, lambda: self._update_scan_status("Discovering local devices..."))
                
                # Discover devices with a 10-second timeout
                devices = discover_devices(timeout=10)
                
                # Update the devices list in the UI thread
                self.root.after(0, lambda: self._update_devices_list(devices, time.time() - start_time))
                
            except Exception as e:
                self.root.after(0, lambda: self._handle_scan_error(e))
            finally:
                self.root.after(0, self._enable_ui_controls)
        
        # Run in a separate thread to avoid freezing the UI
        threading.Thread(target=scan, daemon=True).start()
    
    def _update_scan_status(self, message: str):
        """Update the scan status in the UI."""
        self.status_bar.config(text=message)
        self.log(message)
    
    def _update_devices_list(self, devices: list, scan_time: float):
        """Update the devices list in the UI."""
        self.devices = devices
        self.filtered_devices = devices.copy()  # Initialize filtered devices
        
        self.devices_listbox.delete(0, tk.END)
        
        if not devices:
            self.devices_listbox.insert(tk.END, "No devices found")
            self.status_bar.config(text="No devices found on the network")
            return
        
        # Add column headers
        header = f"{'IP':<15} {'Status':<8} {'Hostname':<20} {'MAC Address':<17}"
        self.devices_listbox.insert(tk.END, "-" * 70)
        self.devices_listbox.insert(tk.END, header)
        self.devices_listbox.insert(tk.END, "-" * 70)
        
        # Add devices
        for device in devices:
            ip = device.get('ip', 'Unknown')
            hostname = device.get('hostname', 'Unknown')
            mac = device.get('mac', 'Unknown')
            status = '✅' if device.get('reachable', False) else '❌'
            
            # Truncate long hostnames
            if len(hostname) > 15:
                hostname = hostname[:12] + '...'
                
            # Format the device entry
            device_entry = f"{ip:<15} {status:<8} {hostname:<20} {mac}"
            self.devices_listbox.insert(tk.END, device_entry)
        
        # Update status
        self.status_bar.config(
            text=f"Found {len(devices)} device(s) in {scan_time:.1f} seconds"
        )
        self.log(f"Device scan completed. Found {len(devices)} device(s)", 'SUCCESS')
    
    def _handle_scan_error(self, error: Exception):
        """Handle errors during device scanning."""
        error_msg = f"Error scanning network: {str(error)}"
        self.devices_listbox.delete(0, tk.END)
        self.devices_listbox.insert(tk.END, "Error scanning network")
        self.status_bar.config(text=error_msg, foreground='red')
        self.log(error_msg, 'ERROR')
    
    def _filter_devices(self, event=None):
        """Filter the devices list based on search text."""
        if not hasattr(self, 'devices') or not self.devices:
            return
            
        search_text = self.search_var.get().lower()
        
        if not search_text:
            self.filtered_devices = self.devices
        else:
            self.filtered_devices = [
                d for d in self.devices
                if (search_text in d.get('ip', '').lower() or
                    search_text in d.get('hostname', '').lower() or
                    search_text in d.get('mac', '').lower())
            ]
        
        # Update the listbox
        self.devices_listbox.delete(0, tk.END)
        
        if not self.filtered_devices:
            self.devices_listbox.insert(tk.END, "No matching devices found")
            return
            
        # Add column headers
        header = f"{'IP':<15} {'Status':<8} {'Hostname':<20} {'MAC Address':<17}"
        self.devices_listbox.insert(tk.END, "-" * 70)
        self.devices_listbox.insert(tk.END, header)
        self.devices_listbox.insert(tk.END, "-" * 70)
        
        # Add filtered devices
        for device in self.filtered_devices:
            ip = device.get('ip', 'Unknown')
            hostname = device.get('hostname', 'Unknown')
            mac = device.get('mac', 'Unknown')
            status = '✅' if device.get('reachable', False) else '❌'
            
            if len(hostname) > 15:
                hostname = hostname[:12] + '...'
                
            device_entry = f"{ip:<15} {status:<8} {hostname:<20} {mac}"
            self.devices_listbox.insert(tk.END, device_entry)
    
    def on_device_select(self, event):
        """Handle device selection from the list."""
        selection = self.devices_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        if index < 3:  # Skip header rows
            return
            
        device_index = index - 3  # Adjust for header rows
        if 0 <= device_index < len(self.filtered_devices):
            self.selected_device = self.filtered_devices[device_index]
            self.send_btn.config(state=tk.NORMAL)
            self.file_btn.config(state=tk.NORMAL)
            self.log(f"Selected device: {self.selected_device.get('ip')} ({self.selected_device.get('hostname', 'Unknown')})")
    
    def start_servers(self):
        """Start TCP and UDP servers."""
        try:
            # Start TCP Server
            self.tcp_server = TCPServer(port=5000)
            self.tcp_server.file_callback = self.handle_file_transfer_update
            self.tcp_server.start(callback=self.handle_incoming_tcp)
            self.log("TCP Server started on port 5000", 'SUCCESS')
            
            # Start UDP Server
            self.udp_server = UDPServer(port=5001)
            self.udp_server.start(callback=self.handle_incoming_udp)
            self.log("UDP Server started on port 5001", 'SUCCESS')
            
        except Exception as e:
            self.log(f"Error starting servers: {str(e)}", 'ERROR')
    
    def discover_network_devices(self):
        """Discover devices on the local network with progress feedback."""
        self.devices_listbox.delete(0, tk.END)
        self.devices_listbox.insert(tk.END, "Scanning network...")
        self.refresh_btn.config(state=tk.DISABLED)
        self.status_bar.config(text="Scanning network...")
        
        def scan():
            try:
                start_time = time.time()
                
                # Update UI with scanning status
                self.root.after(0, lambda: self._update_scan_status("Discovering local devices..."))
                
                # Discover devices with a 10-second timeout
                devices = discover_devices(timeout=10)
                
                # Update the devices list in the UI thread
                self.root.after(0, lambda: self._update_devices_list(devices, time.time() - start_time))
                
            except Exception as e:
                self.root.after(0, lambda: self._handle_scan_error(e))
            finally:
                self.root.after(0, lambda: self.refresh_btn.config(state=tk.NORMAL))
        
        # Run in a separate thread to avoid freezing the UI
        threading.Thread(target=scan, daemon=True).start()
    
    def _update_scan_status(self, message: str):
        """Update the scan status in the UI."""
        self.status_bar.config(text=message)
        self.log(message)
    
    def _update_devices_list(self, devices: list, scan_time: float):
        """Update the devices list in the UI."""
        self.devices = devices
        self.filtered_devices = devices.copy()  # Initialize filtered devices
        
        self.devices_listbox.delete(0, tk.END)
        
        if not devices:
            self.devices_listbox.insert(tk.END, "No devices found")
            self.status_bar.config(text="No devices found on the network")
            return
        
        # Add column headers
        header = f"{'IP':<15} {'Status':<8} {'Hostname':<20} {'MAC Address':<17}"
        self.devices_listbox.insert(tk.END, "-" * 70)
        self.devices_listbox.insert(tk.END, header)
        self.devices_listbox.insert(tk.END, "-" * 70)
        
        # Add devices
        for device in devices:
            ip = device.get('ip', 'Unknown')
            hostname = device.get('hostname', 'Unknown')
            mac = device.get('mac', 'Unknown')
            status = '✅' if device.get('reachable', False) else '❌'
            
            # Truncate long hostnames
            if len(hostname) > 15:
                hostname = hostname[:12] + '...'
                
            # Format the device entry
            device_entry = f"{ip:<15} {status:<8} {hostname:<20} {mac}"
            self.devices_listbox.insert(tk.END, device_entry)
        
        # Update status
        self.status_bar.config(
            text=f"Found {len(devices)} device(s) in {scan_time:.1f} seconds"
        )
        self.log(f"Device scan completed. Found {len(devices)} device(s)", 'SUCCESS')
    
    def _handle_scan_error(self, error: Exception):
        """Handle errors during device scanning."""
        error_msg = f"Error scanning network: {str(error)}"
        self.devices_listbox.delete(0, tk.END)
        self.devices_listbox.insert(tk.END, "Error scanning network")
        self.status_bar.config(text=error_msg, foreground='red')
        self.log(error_msg, 'ERROR')
    
    def _filter_devices(self, event=None):
        """Filter the devices list based on search text."""
        if not hasattr(self, 'devices') or not self.devices:
            return
            
        search_text = self.search_var.get().lower()
        
        if not search_text:
            self.filtered_devices = self.devices
        else:
            self.filtered_devices = [
                d for d in self.devices
                if (search_text in d.get('ip', '').lower() or
                    search_text in d.get('hostname', '').lower() or
                    search_text in d.get('mac', '').lower())
            ]
        
        # Update the listbox
        self.devices_listbox.delete(0, tk.END)
        
        if not self.filtered_devices:
            self.devices_listbox.insert(tk.END, "No matching devices found")
            return
            
        # Add column headers
        header = f"{'IP':<15} {'Status':<8} {'Hostname':<20} {'MAC Address':<17}"
        self.devices_listbox.insert(tk.END, "-" * 70)
        self.devices_listbox.insert(tk.END, header)
        self.devices_listbox.insert(tk.END, "-" * 70)
        
        # Add filtered devices
        for device in self.filtered_devices:
            ip = device.get('ip', 'Unknown')
            hostname = device.get('hostname', 'Unknown')
            mac = device.get('mac', 'Unknown')
            status = '✅' if device.get('reachable', False) else '❌'
            
            if len(hostname) > 15:
                hostname = hostname[:12] + '...'
                
            device_entry = f"{ip:<15} {status:<8} {hostname:<20} {mac}"
            self.devices_listbox.insert(tk.END, device_entry)
    
    def process_queue(self):
        """Process messages from the queue in the main thread."""
        try:
            while True:
                func, args = self.message_queue.get_nowait()
                func(*args)
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)
    
    def on_device_select(self, event):
        """Handle device selection from the list."""
        selection = self.devices_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.devices):
                self.selected_device = self.devices[index]
                self.log(f"Selected device: {self.selected_device['ip']}")
                self.send_button.config(state=tk.NORMAL)
                self.test_button.config(state=tk.NORMAL)
                self.file_button.config(state=tk.NORMAL)
                self.status_label.config(text=f"Status: Ready to connect", foreground="green")
    
    def on_protocol_change(self):
        """Handle protocol change (TCP/UDP)."""
        self.protocol = self.protocol_var.get()
        self.log(f"Selected protocol: {self.protocol}")
    
    def send_message(self):
        """Send a message to the selected device."""
        if not self.selected_device:
            messagebox.showerror("Error", "No device selected")
            return
        
        message = self.message_entry.get().strip()
        if not message:
            messagebox.showerror("Error", "Message cannot be empty")
            return
        
        # Start a new thread to handle the message sending and OSI simulation
        threading.Thread(
            target=self.simulate_osi_flow,
            args=(message, self.selected_device['ip']),
            daemon=True
        ).start()
    
    def simulate_osi_flow(self, message: str, target_ip: str):
        """Simulate the OSI model flow for sending a message."""
        try:
            # Reset UI
            self.root.after(0, lambda: self.log(f"Starting {self.protocol} transmission to {target_ip}", 'INFO'))
            for layer in self.layer_frames:
                self.root.after(0, lambda l=layer: self.highlight_layer(l, False))
                self.root.after(0, lambda l=layer, d="": self.update_layer_data(l, d))
            
            # Application Layer
            self.root.after(0, lambda: self.highlight_layer("Application"))
            self.root.after(0, lambda: self.update_layer_data(
                "Application", 
                f"Sending: {message[:30]}{'...' if len(message) > 30 else ''}"
            ))
            time.sleep(1)
            
            # Presentation Layer
            self.root.after(0, lambda: self.highlight_layer("Presentation"))
            encoded_message = message.encode('utf-8')
            self.root.after(0, lambda: self.update_layer_data(
                "Presentation", 
                f"Encoded: {encoded_message[:30]}..."
            ))
            time.sleep(1)
            
            # Session Layer
            self.root.after(0, lambda: self.highlight_layer("Session"))
            session_data = {"protocol": self.protocol, "data": message}
            self.root.after(0, lambda: self.update_layer_data(
                "Session", 
                f"Session established with {target_ip}"
            ))
            time.sleep(0.5)
            
            # Transport Layer
            self.root.after(0, lambda: self.highlight_layer("Transport"))
            port = 5000 if self.protocol == "TCP" else 5001
            transport_header = f"{self.protocol} SRC_PORT:54321 DST_PORT:{port}"
            self.root.after(0, lambda: self.update_layer_data(
                "Transport", 
                f"{transport_header}"
            ))
            time.sleep(0.5)
            
            # Network Layer
            self.root.after(0, lambda: self.highlight_layer("Network"))
            import socket
            local_ip = socket.gethostbyname(socket.gethostname())
            network_header = f"SRC_IP:{local_ip} DST_IP:{target_ip}"
            self.root.after(0, lambda: self.update_layer_data(
                "Network", 
                f"Routing: {network_header}"
            ))
            time.sleep(0.5)
            
            # Data Link Layer
            self.root.after(0, lambda: self.highlight_layer("Data Link"))
            self.root.after(0, lambda: self.update_layer_data(
                "Data Link", 
                "Resolving MAC address..."
            ))
            time.sleep(0.5)
            
            # Physical Layer
            self.root.after(0, lambda: self.highlight_layer("Physical"))
            self.root.after(0, lambda: self.update_layer_data(
                "Physical", 
                f"Transmitting {len(message)} bytes..."
            ))
            
            # Actually send the message using the selected protocol
            if self.protocol == "TCP":
                self.send_tcp_message(target_ip, port, message)
            else:
                self.send_udp_message(target_ip, port, message)
            
            # Reset highlights after a short delay
            time.sleep(1)
            self.root.after(0, lambda: self.highlight_layer("Physical", False))
            self.root.after(0, lambda: self.log("Transmission complete!", 'SUCCESS'))
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error during transmission: {str(e)}", 'ERROR'))
    
    def test_connection(self):
        """Test connection to the selected device."""
        if not self.selected_device:
            messagebox.showerror("Error", "No device selected")
            return
            
        def _test():
            ip = self.selected_device['ip']
            port = 5000 if self.protocol == "TCP" else 5001
            
            try:
                if self.protocol == "TCP":
                    client = TCPClient(host=ip, port=port)
                    if client.connect():
                        success, response = client.test_connection()
                        if success:
                            self.message_queue.put((
                                lambda msg: self.log(f"Connection test successful: {msg}", 'SUCCESS'),
                                [response or "Connection established"]
                            ))
                            self.message_queue.put((
                                lambda: self.status_label.config(
                                    text=f"Status: Connected to {ip}", 
                                    foreground="green"
                                ),
                                []
                            ))
                            return
                else:
                    # For UDP, just try to send a test message
                    client = UDPClient(host=ip, port=port)
                    if client.start():
                        client.send("TEST_CONNECTION")
                        self.message_queue.put((
                            lambda: self.log("UDP test message sent", 'INFO'),
                            []
                        ))
                        self.message_queue.put((
                            lambda: self.status_label.config(
                                text=f"Status: UDP message sent to {ip}", 
                                foreground="green"
                            ),
                            []
                        ))
                        return
                
                self.message_queue.put((
                    lambda: self.log(f"Failed to connect to {ip}", 'ERROR'),
                    []
                ))
                self.message_queue.put((
                    lambda: self.status_label.config(
                        text=f"Status: Connection failed", 
                        foreground="red"
                    ),
                    []
                ))
                
            except Exception as e:
                self.message_queue.put((
                    lambda e=e: self.log(f"Connection test failed: {str(e)}", 'ERROR'),
                    []
                ))
                self.message_queue.put((
                    lambda: self.status_label.config(
                        text=f"Status: Connection error", 
                        foreground="red"
                    ),
                    []
                ))
            finally:
                if 'client' in locals():
                    if self.protocol == "TCP":
                        client.disconnect()
                    else:
                        client.stop()
        
        # Run in a separate thread
        threading.Thread(target=_test, daemon=True).start()
    
    def send_file_dialog(self):
        """Open file dialog to select a file to send."""
        if not self.selected_device:
            messagebox.showerror("Error", "No device selected")
            return
            
        file_path = filedialog.askopenfilename(
            title="Select file to send",
            filetypes=[
                ("All files", "*.*"),
                ("Images", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("Videos", "*.mp4 *.avi *.mov *.mkv"),
                ("Documents", "*.pdf *.doc *.docx *.xls *.xlsx *.ppt *.pptx *.txt")
            ]
        )
        
        if not file_path:
            return  # User cancelled
            
        file_size = os.path.getsize(file_path)
        if file_size > 5 * 1024 * 1024:  # 5MB limit
            messagebox.showerror("Error", "File size exceeds 5MB limit")
            return
            
        self.send_file(file_path)
    
    def send_file(self, file_path: str):
        """Send a file to the selected device."""
        if not self.selected_device:
            return
            
        ip = self.selected_device['ip']
        port = 5000  # Using TCP for file transfer
        
        def _send():
            try:
                client = TCPClient(host=ip, port=port)
                if not client.connect():
                    self.message_queue.put((
                        lambda: self.log(f"Failed to connect to {ip}:{port}", 'ERROR'),
                        []
                    ))
                    return
                
                # Send file transfer request
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                
                transfer = client.send_file(file_path)
                if not transfer:
                    self.message_queue.put((
                        lambda: self.log(f"Failed to start file transfer", 'ERROR'),
                        []
                    ))
                    return
                
                self.message_queue.put((
                    lambda: self.log(f"Starting file transfer: {file_name} ({file_size/1024:.1f} KB)", 'INFO'),
                    []
                ))
                
                # Track transfer progress
                transfer_id = transfer.transfer_id
                self.active_transfers[transfer_id] = transfer
                
                # Show progress bar
                self.message_queue.put((
                    lambda: self.progress.pack(fill=tk.X, pady=(5, 0)),
                    []
                ))
                
                # Wait for transfer to complete
                while transfer.status == TransferStatus.IN_PROGRESS:
                    progress = (transfer.bytes_transferred / file_size) * 100
                    self.message_queue.put((
                        lambda p=progress: self.progress_var.set(p),
                        []
                    ))
                    time.sleep(0.1)
                
                if transfer.status == TransferStatus.COMPLETED:
                    self.message_queue.put((
                        lambda: self.log(f"File transfer completed: {file_name}", 'SUCCESS'),
                        []
                    ))
                else:
                    self.message_queue.put((
                        lambda: self.log(f"File transfer failed: {file_name}", 'ERROR'),
                        []
                    ))
                
            except Exception as e:
                self.message_queue.put((
                    lambda e=e: self.log(f"File transfer error: {str(e)}", 'ERROR'),
                    []
                ))
            finally:
                if 'transfer_id' in locals():
                    self.active_transfers.pop(transfer_id, None)
                if 'client' in locals():
                    client.disconnect()
                
                # Hide progress bar
                self.message_queue.put((
                    lambda: self.progress.pack_forget(),
                    []
                ))
        
        # Run in a separate thread
        threading.Thread(target=_send, daemon=True).start()
    
    def handle_file_transfer_update(self, transfer: FileTransfer):
        """Handle file transfer progress updates."""
        if transfer.status == TransferStatus.COMPLETED:
            self.log(f"Received file: {transfer.filename} ({transfer.filesize/1024:.1f} KB)", 'SUCCESS')
            
            # Save the received file
            save_path = self.received_files_dir / transfer.filename
            with open(save_path, 'wb') as f:
                f.write(transfer.data)
            
            self.log(f"File saved to: {save_path}", 'INFO')
    
    def send_tcp_message(self, ip: str, port: int, message: str):
        """Send a message using TCP."""
        try:
            client = TCPClient(host=ip, port=port)
            if client.connect():
                response = client.send(message)
                if response:
                    self.message_queue.put((
                        lambda: self.log(f"TCP response from {ip}:{port}: {response}", 'INFO'),
                        []
                    ))
                self.message_queue.put((
                    lambda: self.log(f"TCP message sent to {ip}:{port}", 'SUCCESS'),
                    []
                ))
                return True
            else:
                self.message_queue.put((
                    lambda: self.log(f"Failed to connect to {ip}:{port}", 'ERROR'),
                    []
                ))
                return False
        except Exception as e:
            self.message_queue.put((
                lambda e=e: self.log(f"TCP error: {str(e)}", 'ERROR'),
                []
            ))
            return False
        finally:
            if 'client' in locals():
                client.disconnect()
    
    def send_udp_message(self, ip: str, port: int, message: str):
        """Send a message using UDP."""
        try:
            client = UDPClient(host=ip, port=port)
            if client.start():
                client.send(message)
                self.root.after(0, lambda: self.log(f"UDP message sent to {ip}:{port}", 'SUCCESS'))
            else:
                self.root.after(0, lambda: self.log(f"Failed to start UDP client", 'ERROR'))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"UDP error: {str(e)}", 'ERROR'))
        finally:
            if 'client' in locals():
                client.stop()
    
    def handle_incoming_tcp(self, message, client_address):
        """Handle incoming TCP messages."""
        if isinstance(message, dict) and message.get('type') == 'test_connection':
            # Handle test connection request
            self.message_queue.put((
                lambda: self.log(f"Connection test from {client_address}", 'INFO'),
                []
            ))
            return {"status": "success", "message": "Connection test successful"}
        
        self.message_queue.put((
            lambda: self.log(f"TCP from {client_address}: {message}", 'INFO'),
            []
        ))
    
    def handle_incoming_udp(self, message, client_address):
        """Handle incoming UDP messages."""
        if message == "TEST_CONNECTION":
            self.message_queue.put((
                lambda: self.log(f"UDP test from {client_address}", 'INFO'),
                []
            ))
        else:
            self.message_queue.put((
                lambda: self.log(f"UDP from {client_address}: {message}", 'INFO'),
                []
            ))

def main():
    root = tk.Tk()
    
    # Configure styles
    style = ttk.Style()
    style.configure('Highlight.TLabelframe', background='#e6f3ff')
    
    # Create a queue for thread-safe UI updates
    import queue
    
    app = OSIVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
