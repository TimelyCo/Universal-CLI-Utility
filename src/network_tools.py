"""
Network utilities module for Universal CLI Utility
"""
import os
import socket
import subprocess
import platform
import logging
from typing import Dict, Any, List, Tuple

class NetworkUtilities:
    """Handles network operations"""
    
    def __init__(self):
        self.logger = logging.getLogger("ucli.network_utils")
        
    def ping(self, host: str, count: int = 4, **kwargs) -> None:
        """
        Ping a host
        
        Args:
            host: Host to ping
            count: Number of packets to send
        """
        self.logger.info(f"Pinging {host} ({count} packets)")
        
        try:
            # Determine the ping command based on the OS
            system = platform.system().lower()
            
            if system == "windows":
                cmd = ["ping", "-n", str(count), host]
            else:  # Linux, MacOS, etc.
                cmd = ["ping", "-c", str(count), host]
                
            # Execute ping command
            print(f"Pinging {host} with {count} packets...")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                print(stdout)
            else:
                print(f"Error: {stderr}")
                
        except Exception as e:
            self.logger.error(f"Error pinging {host}: {e}")
            print(f"Error: {e}")
            
    def scan(self, host: str, ports: str = "1-1000", **kwargs) -> None:
        """
        Scan ports on a host
        
        Args:
            host: Host to scan
            ports: Port range (e.g., 1-1000, 80,443,8080)
        """
        self.logger.info(f"Scanning ports on {host} (ports: {ports})")
        
        try:
            # Resolve host
            print(f"Resolving host {host}...")
            try:
                ip = socket.gethostbyname(host)
                print(f"Host {host} resolved to {ip}")
            except socket.gaierror:
                print(f"Error: Could not resolve host {host}")
                return
                
            # Parse port range
            port_list = []
            for part in ports.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    port_list.extend(range(start, end + 1))
                else:
                    port_list.append(int(part))
                    
            # Scan ports
            print(f"Scanning {len(port_list)} ports on {host}...")
            open_ports = []
            
            for port in port_list:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    service = self._get_service_name(port)
                    open_ports.append((port, service))
                sock.close()
                
            # Display results
            if open_ports:
                print(f"Found {len(open_ports)} open ports on {host}:")
                for port, service in open_ports:
                    print(f"  Port {port}: {service}")
            else:
                print(f"No open ports found on {host}")
                
        except Exception as e:
            self.logger.error(f"Error scanning ports on {host}: {e}")
            print(f"Error: {e}")
            
    def _get_service_name(self, port: int) -> str:
        """Get service name for a port number"""
        try:
            return socket.getservbyport(port)
        except (socket.error, OSError):
            return "unknown"