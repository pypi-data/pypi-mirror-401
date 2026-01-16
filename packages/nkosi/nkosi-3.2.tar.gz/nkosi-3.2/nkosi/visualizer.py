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
        self.root.title("OSI Model Network Visualizer")
        self.root.geometry("1200x800")
        
        # Initialize server attributes
        self.tcp_server = None
        self.udp_server = None
        self.tcp_port = 5000
        self.udp_port = 5001
        self.root.minsize(1000, 700)
        
        # Initialize network components
        self.tcp_server = None
        self.udp_server = None
        self.tcp_client = None
        self.udp_client = None
        self.selected_device = None
        self.devices = []
        self.filtered_devices = []
        self.protocol = "TCP"  # Default protocol
        self.active_transfers = {}
        
        # UI Components
        self.refresh_btn = None
        self.devices_listbox = None
        self.status_bar = None
        self.left_panel = None
        self.right_panel = None
        self.main_container = None
        self.bottom_panel = None
        self.search_var = tk.StringVar()
        
        # Initialize layer tracking
        self.layer_frames = {}
        self.layer_vars = {}
        
        # Logging buffer for early messages
        self._log_buffer = []
        
        # Create received files directory
        self.received_files_dir = Path("received_files")
        self.received_files_dir.mkdir(exist_ok=True)
        
        # Queue for thread-safe UI updates
        self.message_queue = queue.Queue()
        
        # Configure styles first
        self._configure_styles()
        
        # Build the UI
        self.build_ui()
        
        # Process any buffered log messages
        if hasattr(self, 'log_text') and self._log_buffer:
            for level, message in self._log_buffer:
                self.log(message, level)
            self._log_buffer = []
        
        # Start servers and discovery
        try:
            self.start_servers()
            if hasattr(self, 'discover_network_devices'):
                self.discover_network_devices()
        except Exception as e:
            self.log(f"Error during initialization: {str(e)}", 'ERROR')
        
        # Start processing messages
        self.process_queue()
    
    def build_ui(self):
        """
        Build the main UI components with proper initialization order.
        """
        try:
            # 1. Create the main container
            self.main_container = ttk.Frame(self.root)
            self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 2. Create panels
            # Left panel for controls (30% width)
            self.left_panel = ttk.LabelFrame(self.main_container, text="Network Controls", padding=10)
            self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
            self.left_panel.pack_propagate(False)
            self.left_panel.config(width=350)
            
            # Right panel for OSI visualization (70% width)
            self.right_panel = ttk.LabelFrame(self.main_container, text="OSI Model", padding=10)
            self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # 3. Build the bottom panel (logs) first to ensure log_text is available
            self.bottom_panel = ttk.LabelFrame(self.root, text="Logs")
            self.bottom_panel.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0, 10))
            self.build_logs()
            
            # 4. Now build the controls and OSI layers
            self.build_controls()
            self.build_osi_layers()
            
            # 5. Initialize devices list if not already done
            if not hasattr(self, 'devices'):
                self.devices = []
            if not hasattr(self, 'filtered_devices'):
                self.filtered_devices = []
            
            # 6. Add status bar at the very bottom
            self.status_bar = ttk.Frame(self.root, style='Status.TFrame')
            self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 5))
            
            # Add status label
            self.status_label = ttk.Label(
                self.status_bar,
                text="Ready",
                style='Status.TLabel',
                anchor='w'
            )
            self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Add protocol indicator
            self.protocol_label = ttk.Label(
                self.status_bar,
                text=f"Protocol: {self.protocol}",
                style='Status.TLabel',
                anchor='e',
                padding=(0, 0, 10, 0)
            )
            self.protocol_label.pack(side=tk.RIGHT)
            
            # 7. Process any buffered log messages
            if hasattr(self, '_log_buffer') and self._log_buffer:
                for level, message in self._log_buffer:
                    self.log(message, level)
                self._log_buffer = []
            
            # 8. Force update to ensure all widgets are properly sized
            self.root.update_idletasks()
            
            # Log successful UI initialization
            self.log("UI initialization complete", 'SUCCESS')
            
        except Exception as e:
            error_msg = f"Failed to build UI: {str(e)}"
            print(error_msg)
            # Try to log the error if possible
            if hasattr(self, 'log'):
                self.log(error_msg, 'ERROR')
            else:
                print("Logger not available:", error_msg)
            messagebox.showerror("UI Error", error_msg)
            raise
    
    def build_controls(self):
        """Build the control panel with network device discovery and controls."""
        try:
            # Network Devices Section
            ttk.Label(self.left_panel, text="Network Devices", style='Section.TLabel').pack(pady=(0, 5), anchor=tk.W)
            
            # Search frame
            search_frame = ttk.Frame(self.left_panel)
            search_frame.pack(fill=tk.X, pady=(0, 5))
            
            # Search entry
            if not hasattr(self, 'search_var'):
                self.search_var = tk.StringVar()
                
            search_entry = ttk.Entry(
                search_frame,
                textvariable=self.search_var,
                style='TEntry'
            )
            search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            search_entry.bind('<KeyRelease>', self._filter_devices)
            
            # Refresh button
            self.refresh_btn = ttk.Button(
                search_frame,
                text="↻",
                width=3,
                command=self.discover_network_devices,
                style='Accent.TButton'
            )
            self.refresh_btn.pack(side=tk.RIGHT)
            
            # Devices list container with scrollbar
            list_container = ttk.Frame(self.left_panel)
            list_container.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
            
            # Scrollbar for devices list
            scrollbar = ttk.Scrollbar(list_container)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Devices listbox
            self.devices_listbox = tk.Listbox(
                list_container,
                yscrollcommand=scrollbar.set,
                selectmode=tk.SINGLE,
                font=('Consolas', 9),
                relief='solid',
                borderwidth=1,
                highlightthickness=0,
                background='white',
                foreground='black',
                selectbackground='#0078d7',
                selectforeground='white'
            )
            self.devices_listbox.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.devices_listbox.yview)
            
            # Bind selection event
            if hasattr(self, 'on_device_select'):
                self.devices_listbox.bind('<<ListboxSelect>>', self.on_device_select)
            
            # Add default message to devices list
            self.devices_listbox.insert(tk.END, "Click refresh to scan for devices")
            
        except Exception as e:
            messagebox.showerror("UI Error", f"Failed to build controls: {str(e)}")
            raise
        
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
        msg_frame = ttk.LabelFrame(self.left_panel, text="Message", padding=5)
        msg_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Message input with scrollbar
        msg_container = ttk.Frame(msg_frame)
        msg_container.pack(fill=tk.X, pady=(0, 5))
        
        self.message_entry = tk.Text(
            msg_container,
            height=4,
            wrap=tk.WORD,
            font=('Segoe UI', 9),
            padx=5,
            pady=5
        )
        self.message_entry.pack(fill=tk.X)
        self.message_entry.insert('1.0', "Hello, OSI Model!")
        
        # Scrollbar for message input
        msg_scroll = ttk.Scrollbar(msg_container, command=self.message_entry.yview)
        msg_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_entry.config(yscrollcommand=msg_scroll.set)
        
        # Action Buttons
        btn_frame = ttk.Frame(msg_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Left side buttons
        left_btn_frame = ttk.Frame(btn_frame)
        left_btn_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.send_btn = ttk.Button(
            left_btn_frame,
            text="Send Message",
            command=self.send_message,
            style='Accent.TButton',
            width=15
        )
        self.send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.test_btn = ttk.Button(
            left_btn_frame,
            text="Test Connection",
            command=self.test_connection,
            width=15
        )
        self.test_btn.pack(side=tk.LEFT)
        
        # Right side buttons
        self.file_btn = ttk.Button(
            btn_frame,
            text="📎 Attach File",
            command=self.send_file_dialog,
            style='Accent.TButton',
            width=12
        )
        self.file_btn.pack(side=tk.RIGHT)
        
        # Initially disable action buttons until device is selected
        self.send_btn.config(state=tk.DISABLED)
        self.file_btn.config(state=tk.DISABLED)
        self.test_btn.config(state=tk.DISABLED)
    
    def _configure_styles(self):
        style =  ttk.Style()
  
        # Configure log area
        style.configure('Log.TFrame', background='white')
        
        # Configure scrollbars
        style.configure('Vertical.TScrollbar',
                      arrowsize=12,
                      arrowcolor='#6c757d',
                      troughcolor='#e9ecef',
                      background='#adb5bd',
                      bordercolor='#dee2e6',
                      arrowpadding=2)
        
        style.map('Vertical.TScrollbar',
                background=[('active', '#6c757d')])
        
        # Configure entry fields
        style.configure('TEntry',
                      fieldbackground='white',
                      foreground='#212529',
                      borderwidth=1,
                      relief='solid',
                      padding='3 6')
        
        style.map('TEntry',
                fieldbackground=[('readonly', '#f8f9fa')],
                foreground=[('readonly', '#495057')])
        
        # Configure radio buttons
        style.configure('TRadiobutton',
                      background='#f5f5f5',
                      font=('Segoe UI', 9))
        
        # Configure notebook tabs
        style.configure('TNotebook', background='#f5f5f5')
        style.configure('TNotebook.Tab',
                      padding=[10, 4],
                      font=('Segoe UI', 9, 'bold'))
        
        # Configure tooltips
        style.configure('Tooltip.TLabel',
                      background='#343a40',
                      foreground='#ffffff',
                      padding=6,
                      relief='solid',
                      borderwidth=1)
    
    def build_osi_layers(self):
        """Build the OSI model visualization with interactive layers."""
        self.layer_frames = {}
        self.layer_vars = {}
        
        # Create a container frame for the OSI model
        container = ttk.Frame(self.right_panel)
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure the canvas scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # OSI Layers in order from top to bottom (Application to Physical)
        layers = [
            ("Application", "HTTP, FTP, SMTP, DNS, SSH"),
            ("Presentation", "SSL/TLS, JPEG, MP3, ASCII, Encryption"),
            ("Session", "API, Sockets, NetBIOS, RPC"),
            ("Transport", "TCP/UDP"),
            ("Network", "IP/ICMP"),
            ("Data Link", "Ethernet/PPP"),
            ("Physical", "WiFi/Cable")
        ]
        
        # Colors for different OSI layers
        layer_colors = {
            'Application': '#f8d7da',
            'Presentation': '#fff3cd',
            'Session': '#d1e7dd',
            'Transport': '#cfe2ff',
            'Network': '#e2e3e5',
            'Data Link': '#d3d3d3',
            'Physical': '#c6c8ca'
        }
        
        for layer_name, protocols in layers:
            # Create main frame for each layer with padding
            layer_frame = ttk.Frame(scrollable_frame, padding=5)
            layer_frame.pack(fill=tk.X, pady=2, padx=5)
            
            # Create a colored header for the layer
            header_frame = ttk.Frame(layer_frame, style='LayerHeader.TFrame')
            header_frame.pack(fill=tk.X, pady=(0, 2))
            
            # Layer name and number
            ttk.Label(
                header_frame,
                text=f"Layer {7 - layers.index((layer_name, protocols))}: {layer_name}",
                font=('Segoe UI', 10, 'bold'),
                background=layer_colors[layer_name],
                padding=(10, 5)
            ).pack(side=tk.LEFT, fill=tk.X, expand=True, anchor='w')
            
            # Protocols label with tooltip
            protocol_frame = ttk.Frame(layer_frame, style='Protocol.TFrame')
            protocol_frame.pack(fill=tk.X, pady=(0, 5))
            
            ttk.Label(
                protocol_frame,
                text=protocols,
                font=('Consolas', 8),
                style='Protocol.TLabel',
                wraplength=500,
                justify=tk.LEFT,
                padding=(5, 3)
            ).pack(fill=tk.X, padx=2)
            
            # Data display area with scrollbar
            data_frame = ttk.Frame(layer_frame, style='Data.TFrame')
            data_frame.pack(fill=tk.X, pady=(0, 5))
            
            # Text widget for data display with scrollbar
            text_widget = tk.Text(
                data_frame,
                height=3,
                wrap=tk.WORD,
                font=('Consolas', 8),
                bg='#f8f9fa',
                relief=tk.SOLID,
                borderwidth=1,
                padx=5,
                pady=3
            )
            text_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
            text_widget.config(state=tk.DISABLED)  # Make it read-only
            
            # Add a clear button for the layer
            clear_btn = ttk.Button(
                data_frame,
                text="Clear",
                width=6,
                command=lambda name=layer_name: self.clear_layer_data(name)
            )
            clear_btn.pack(side=tk.RIGHT, padx=(5, 0))
            
            # Store references
            self.layer_frames[layer_name] = {
                'frame': layer_frame,
                'header': header_frame,
                'protocols': protocol_frame,
                'data': data_frame,
                'text': text_widget,
                'clear_btn': clear_btn,
                'var': tk.StringVar()
            }
            self.layer_vars[layer_name] = self.layer_frames[layer_name]['var']
            
            # Bind variable changes to update the text widget
            def make_callback(var, widget):
                def callback(*args):
                    widget.config(state=tk.NORMAL)
                    widget.delete(1.0, tk.END)
                    widget.insert(tk.END, var.get())
                    widget.config(state=tk.DISABLED)
                return callback
            
            self.layer_vars[layer_name].trace_add('write', 
                make_callback(self.layer_vars[layer_name], text_widget))
        
        # Add some custom styles for the OSI layers
        style = ttk.Style()
        style.configure('LayerHeader.TFrame', background=layer_colors['Application'])
        style.configure('Protocol.TFrame', background='#e9ecef')
        style.configure('Data.TFrame', background='white')
        
        # Add a default message to the application layer
        self.update_layer_data('Application', 'Ready to send/receive data...')
        
        # Make sure the canvas is properly scrolled to the top
        canvas.yview_moveto(0.0)
    
    def clear_layer_data(self, layer_name):
        """Clear the data in the specified layer."""
        if layer_name in self.layer_frames:
            self.layer_vars[layer_name].set('')
            self.log(f"Cleared {layer_name} layer data", 'INFO')
    
    def build_logs(self):
        """Build the logging area with enhanced styling and functionality."""
        try:
            # Create a container frame for the log area
            log_container = ttk.Frame(self.bottom_panel, style='LogContainer.TFrame')
            log_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Log header with controls
            log_header = ttk.Frame(log_container, style='LogHeader.TFrame')
            log_header.pack(fill=tk.X, pady=(0, 2))
            
            ttk.Label(
                log_header,
                text="Simulation Log",
                style='LogHeader.TLabel',
                padding=(5, 2)
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Add clear log button
            clear_btn = ttk.Button(
                log_header,
                text="Clear Log",
                command=self.clear_log,
                style='Small.TButton',
                width=10
            )
            clear_btn.pack(side=tk.RIGHT, padx=2)
            
            # Add save log button
            save_btn = ttk.Button(
                log_header,
                text="Save Log",
                command=self.save_log,
                style='Small.TButton',
                width=10
            )
            save_btn.pack(side=tk.RIGHT, padx=2)
            
            # Create the main log text area with scrollbars
            log_frame = ttk.Frame(log_container, style='LogArea.TFrame')
            log_frame.pack(fill=tk.BOTH, expand=True)
            
            # Vertical scrollbar
            v_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, style='Vertical.TScrollbar')
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Create the text widget
            self.log_text = tk.Text(
                log_frame,
                height=6,  # Reduced height as requested
                wrap=tk.NONE,
                yscrollcommand=v_scroll.set,
                font=('Consolas', 9),
                bg='#ffffff',
                fg='#212529',
                insertbackground='#212529',
                selectbackground='#0078d7',
                selectforeground='white',
                padx=5,
                pady=5,
                relief=tk.SOLID,
                borderwidth=1
            )
            self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            v_scroll.config(command=self.log_text.yview)
            
            # Add horizontal scrollbar
            h_scroll = ttk.Scrollbar(log_frame, orient=tk.HORIZONTAL, style='Horizontal.TScrollbar')
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            self.log_text.config(xscrollcommand=h_scroll.set)
            h_scroll.config(command=self.log_text.xview)
            
            # Configure tags for different log levels
            self.log_text.tag_config('INFO', foreground='#212529')
            self.log_text.tag_config('SUCCESS', foreground='#198754')
            self.log_text.tag_config('WARNING', foreground='#ffc107')
            self.log_text.tag_config('ERROR', foreground='#dc3545')
            self.log_text.tag_config('DEBUG', foreground='#6c757d')
            
            # Make the log text read-only
            self.log_text.config(state=tk.DISABLED)
            
            # Add initial log message
            self.log("Logging initialized. Ready to send/receive data.", 'INFO')
            
            # Add styles for log area
            style = ttk.Style()
            style.configure('LogContainer.TFrame', background='#f8f9fa')
            style.configure('LogHeader.TFrame', background='#e9ecef', relief=tk.SOLID, borderwidth=1)
            style.configure('LogHeader.TLabel', 
                          background='#e9ecef', 
                          font=('Segoe UI', 9, 'bold'),
                          foreground='#212529')
            style.configure('LogArea.TFrame', 
                          background='#ffffff',
                          relief=tk.SOLID, 
                          borderwidth=1)
            style.configure('Small.TButton', 
                          padding='2 4',
                          font=('Segoe UI', 8))
            
        except Exception as e:
            print(f"Error initializing log area: {e}")
            messagebox.showerror("Error", f"Failed to initialize log area: {e}")
    
    def clear_log(self):
        """Clear the log content."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log("Log cleared", 'INFO')
    
    def save_log(self):
        """Save the log content to a file."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Log As"
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log(f"Log saved to {filename}", 'SUCCESS')
        except Exception as e:
            self.log(f"Error saving log: {e}", 'ERROR')
    
    def log(self, message: str, level: str = 'INFO'):
        """
        Add a message to the log with the specified level.
        This method is thread-safe and will schedule the update to run in the main thread.
        
        Args:
            message: The message to log
            level: The log level (INFO, SUCCESS, WARNING, ERROR, DEBUG)
        """
        # Ensure level is valid
        level = level.upper()
        if level not in ['INFO', 'SUCCESS', 'WARNING', 'ERROR', 'DEBUG']:
            level = 'INFO'
            
        # If log_text isn't ready yet, buffer the message
        if not hasattr(self, 'log_text') or self.log_text is None or not self.log_text.winfo_exists():
            if not hasattr(self, '_log_buffer'):
                self._log_buffer = []
            self._log_buffer.append((level, message))
            return
            
        # Process the log message in the main thread
        def _log():
            try:
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_entry = f"[{timestamp}] {message}"
                
                # Add to log text widget with appropriate tag
                if hasattr(self, 'log_text') and self.log_text and self.log_text.winfo_exists():
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, log_entry + "\n", level)
                    self.log_text.see(tk.END)
                    
                    # Limit the number of lines to prevent memory issues
                    try:
                        num_lines = int(self.log_text.index('end-1c').split('.')[0])
                        if num_lines > 1000:  # Keep last 1000 lines
                            self.log_text.delete(1.0, f'{num_lines-1000}.0')
                    except Exception as e:
                        print(f"Error managing log size: {e}")
                    
                    self.log_text.config(state=tk.DISABLED)
                
                # Also print to console for debugging
                print(f"[{level}] {log_entry}")
                
            except Exception as e:
                print(f"Error in log update: {e}")
                # Try to recover by re-enabling the widget
                try:
                    if hasattr(self, 'log_text') and self.log_text and self.log_text.winfo_exists():
                        self.log_text.config(state=tk.NORMAL)
                except Exception as e2:
                    print(f"Error recovering log widget: {e2}")
        
        # Schedule the update to run in the main thread
        try:
            if self.root and hasattr(self.root, 'after'):
                self.root.after(0, _log)
            else:
                _log()
        except Exception as e:
            print(f"Error scheduling log update: {e}")
            _log()
            
    def _add_log_entry(self, log_entry: str, level: str):
        """
        Helper method to add a log entry to the text widget.
        This method is thread-safe and will schedule the update to run in the main thread.
        """
        # Just use the main log method with the existing message
        self.log(log_entry, level)
    
    def highlight_layer(self, layer_name: str, highlight: bool = True):
        """
        Highlight or unhighlight a layer with a visual effect.
        
        Args:
            layer_name: Name of the OSI layer to highlight
            highlight: Whether to highlight (True) or unhighlight (False) the layer
        """
        if layer_name not in self.layer_frames:
            return
            
        layer = self.layer_frames[layer_name]
        
        if highlight:
            # Add a highlight effect
            layer['frame'].config(style='HighlightedLayer.TFrame')
            layer['header'].config(style='HighlightedHeader.TFrame')
            
            # Schedule to remove the highlight after 1 second
            def remove_highlight():
                if layer_name in self.layer_frames:  # Check if still exists
                    self.highlight_layer(layer_name, False)
                    
            self.root.after(1000, remove_highlight)
        else:
            # Remove highlight
            layer['frame'].config(style='TFrame')
            layer['header'].config(style='LayerHeader.TFrame')
    
    def update_layer_data(self, layer_name: str, data: str):
        """
        Update the data displayed in a specific OSI layer.
        
        Args:
            layer_name: Name of the OSI layer to update
            data: Data to display in the layer
        """
        if layer_name not in self.layer_vars:
            self.log(f"Warning: Layer '{layer_name}' not found", 'WARNING')
            return
            
        try:
            # Update the variable which is bound to the text widget
            self.layer_vars[layer_name].set(data)
            
            # Log the update if there's actual data
            if data and data.strip():
                # Truncate long data for logging
                log_data = data if len(data) < 100 else f"{data[:97]}..."
                self.log(f"{layer_name}: {log_data}", 'DEBUG')
                
            # Highlight the layer to show it was updated
            self.highlight_layer(layer_name, True)
            
        except Exception as e:
            self.log(f"Error updating {layer_name} layer: {e}", 'ERROR')
    
    def _enable_ui_controls(self):
        """Re-enable UI controls after scan completes."""
        if not hasattr(self, 'left_panel') or not self.left_panel:
            return
            
        for widget in self.left_panel.winfo_children():
            if isinstance(widget, (ttk.Button, ttk.Radiobutton)):
                # Only enable if it's not the refresh button or if refresh_btn is not set yet
                if not hasattr(self, 'refresh_btn') or widget != self.refresh_btn:
                    try:
                        widget.config(state=tk.NORMAL)
                    except Exception as e:
                        print(f"Error enabling widget: {e}")

    def discover_network_devices(self):
        """Discover devices on the local network with progress feedback."""
        if not hasattr(self, 'devices_listbox') or not self.devices_listbox:
            return
            
        self.devices_listbox.delete(0, tk.END)
        self.devices_listbox.insert(tk.END, "Scanning network...")
        
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text="Scanning network...")
        
        # Disable UI controls during scan
        if hasattr(self, 'left_panel') and self.left_panel:
            for widget in self.left_panel.winfo_children():
                if isinstance(widget, (ttk.Button, ttk.Radiobutton)):
                    if hasattr(self, 'refresh_btn') and widget != self.refresh_btn:
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
                if hasattr(self, 'root') and self.root:
                    self.root.after(0, self._enable_ui_controls)
        
        # Run in a separate thread to avoid freezing the UI
        threading.Thread(target=scan, daemon=True).start()
    
    def _update_scan_status(self, message: str):
        """Update the scan status in the UI."""
        def update():
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                self.status_label.config(text=message)
        
        # Schedule the update to run in the main thread
        if self.root and hasattr(self.root, 'after'):
            self.root.after(0, update)
        else:
            update()
        self.log(message)
    
    def _update_devices_list(self, devices: list, scan_time: float):
        """Update the devices list in the UI."""
        def update():
            self.devices = devices
            self.filtered_devices = devices.copy()
            
            self.devices_listbox.delete(0, tk.END)
            
            if not devices:
                self.devices_listbox.insert(tk.END, "No devices found")
                status_text = f"Scan completed. No devices found. ({scan_time:.1f}s)"
            else:
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
                
                status_text = f"Found {len(devices)} device(s) in {scan_time:.1f} seconds"
            
            # Update status label if it exists
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                self.status_label.config(text=status_text)
            
            self.devices_listbox.config(state=tk.NORMAL)
            self._filter_devices()  # Apply any active filters
        
        # Schedule the update to run in the main thread
        if self.root and hasattr(self.root, 'after'):
            self.root.after(0, update)
        else:
            update()
            
        self.log(f"Device scan completed. {len(devices)} device(s) found in {scan_time:.1f} seconds")
        self.log(f"Device scan completed. Found {len(devices)} device(s)", 'SUCCESS')
    
    def _handle_scan_error(self, error: Exception):
        """Handle errors during device scanning."""
        error_msg = f"Error scanning network: {str(error)}"
        self.devices_listbox.delete(0, tk.END)
        self.devices_listbox.insert(tk.END, "Error scanning network")
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text=error_msg, foreground='red')
        self.log(error_msg, 'ERROR')
    
    def start_servers(self):
        """Start TCP and UDP servers for network communication."""
        try:
            # Start TCP server
            self.tcp_server = TCPServer(port=self.tcp_port)
            self.tcp_server.start()
            self.log(f"TCP Server started on port {self.tcp_port}", 'SUCCESS')
            
            # Start UDP server
            self.udp_server = UDPServer(port=self.udp_port)
            self.udp_server.start()
            self.log(f"UDP Server started on port {self.udp_port}", 'SUCCESS')
            
            # Initialize clients
            self.tcp_client = TCPClient()
            self.udp_client = UDPClient()
            
        except Exception as e:
            error_msg = f"Failed to start servers: {str(e)}"
            self.log(error_msg, 'ERROR')
            raise Exception(error_msg)
    
    def _filter_devices(self, event=None):
        """Filter devices based on search input."""
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
            if 0 <= index < len(self.filtered_devices):
                self.selected_device = self.filtered_devices[index]
                self.log(f"Selected device: {self.selected_device.get('ip', 'Unknown')}")
                self.send_btn.config(state=tk.NORMAL)
                self.test_btn.config(state=tk.NORMAL)
                self.file_btn.config(state=tk.NORMAL)
                if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                    self.status_label.config(text=f"Ready - Selected: {self.selected_device.get('ip', 'Unknown')}")
            else:
                self.send_btn.config(state=tk.DISABLED)
                self.test_btn.config(state=tk.DISABLED)
                self.file_btn.config(state=tk.DISABLED)
    
    def on_protocol_change(self):
        """Handle protocol change (TCP/UDP)."""
        self.protocol = self.protocol_var.get()
        self.log(f"Selected protocol: {self.protocol}")
        
    def test_connection(self):
        """Test connection to the selected device."""
        if not self.selected_device:
            self.log("No device selected for testing", "ERROR")
            return
            
        ip = self.selected_device.get('ip')
        if not ip:
            self.log("Selected device has no IP address", "ERROR")
            return
            
        self.log(f"Testing {self.protocol} connection to {ip}...", "INFO")
        
        def _test():
            try:
                if self.protocol == "TCP":
                    # Test TCP connection
                    import socket
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(2)  # 2 second timeout
                        result = s.connect_ex((ip, 80))  # Try common HTTP port
                        
                        if result == 0:
                            self.log(f"TCP connection to {ip} successful!", "SUCCESS")
                        else:
                            self.log(f"TCP connection to {ip} failed (Error: {result})", "ERROR")
                else:
                    # Test UDP connection (echo service on port 7)
                    import socket
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        s.settimeout(2)  # 2 second timeout
                        s.sendto(b'TEST', (ip, 7))  # Try echo service
                        data, _ = s.recvfrom(1024)
                        
                        if data == b'TEST':
                            self.log(f"UDP echo test to {ip} successful!", "SUCCESS")
                        else:
                            self.log(f"UDP echo test to {ip} failed", "ERROR")
                            
            except socket.timeout:
                self.log(f"{self.protocol} connection to {ip} timed out", "WARNING")
            except Exception as e:
                self.log(f"Connection test failed: {str(e)}", "ERROR")
        
        # Run the test in a separate thread to avoid freezing the UI
        threading.Thread(target=_test, daemon=True).start()
    
    def send_message(self):
        """Send a message to the selected device."""
        if not self.selected_device:
            messagebox.showerror("Error", "No device selected")
            return
            
        # Get message from the Text widget
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Message cannot be empty")
            return
            
        # Get the target IP from the selected device
        target_ip = self.selected_device.get('ip')
        if not target_ip:
            messagebox.showerror("Error", "Selected device has no IP address")
            return
            
        self.log(f"Sending message to {target_ip} via {self.protocol}...", "INFO")
        
        # Start a new thread to handle the message sending and OSI simulation
        threading.Thread(
            target=self.simulate_osi_flow,
            args=(message, target_ip),
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
