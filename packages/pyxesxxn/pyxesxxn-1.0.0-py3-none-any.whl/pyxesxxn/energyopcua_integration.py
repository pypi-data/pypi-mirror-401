"""
EnergyOPCUA Integration Module for PyXESXXN

This module integrates OPC UA (Open Platform Communications Unified Architecture) 
functionality into the PyXESXXN energy system analysis framework, providing 
industrial communication capabilities for energy systems and electric machinery.
"""

from __future__ import annotations

import logging
from typing import Optional, List, Dict, Any, Callable, Union
from datetime import datetime
from enum import Enum

try:
    from pyxesxxn.energyopcua.opcua import Client, Server, Node, uamethod
    from pyxesxxn.energyopcua.opcua.common.subscription import Subscription, SubHandler
    from pyxesxxn.energyopcua.opcua.common.methods import uamethod
    _opcua_available = True
except ImportError:
    _opcua_available = False
    Client = None
    Server = None
    Node = None
    Subscription = None
    SubHandler = None
    uamethod = None

_logger = logging.getLogger(__name__)


class OPCUAConnectionStatus(Enum):
    """OPC UA connection status enumeration."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


class OPCUAMessageType(Enum):
    """OPC UA message type enumeration."""
    DATA_CHANGE = "data_change"
    EVENT = "event"
    STATUS_CHANGE = "status_change"


class EnergyOPCUAConfig:
    """Configuration for EnergyOPCUA integration."""
    
    def __init__(
        self,
        server_url: str = "opc.tcp://localhost:4840",
        timeout: int = 4,
        session_timeout: int = 3600000,
        enable_encryption: bool = False,
        certificate_path: Optional[str] = None,
        private_key_path: Optional[str] = None
    ):
        self.server_url = server_url
        self.timeout = timeout
        self.session_timeout = session_timeout
        self.enable_encryption = enable_encryption
        self.certificate_path = certificate_path
        self.private_key_path = private_key_path


class EnergyOPCUAClient:
    """
    High-level OPC UA client for energy system monitoring and control.
    
    This class provides a simplified interface for connecting to OPC UA servers,
    reading/writing energy data, and subscribing to real-time updates.
    """
    
    def __init__(self, config: Optional[EnergyOPCUAConfig] = None):
        """
        Initialize EnergyOPCUA client.
        
        Args:
            config: OPC UA configuration object
        """
        if not _opcua_available:
            raise ImportError("OPC UA library is not available. Please install required dependencies.")
        
        self.config = config or EnergyOPCUAConfig()
        self._client: Optional[Client] = None
        self._status = OPCUAConnectionStatus.DISCONNECTED
        self._subscriptions: Dict[str, Subscription] = {}
        self._handlers: Dict[str, SubHandler] = {}
        
    def connect(self) -> bool:
        """
        Connect to OPC UA server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self._status = OPCUAConnectionStatus.CONNECTING
            self._client = Client(url=self.config.server_url, timeout=self.config.timeout)
            self._client.connect()
            self._status = OPCUAConnectionStatus.CONNECTED
            _logger.info(f"Successfully connected to OPC UA server: {self.config.server_url}")
            return True
        except Exception as e:
            self._status = OPCUAConnectionStatus.ERROR
            _logger.error(f"Failed to connect to OPC UA server: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from OPC UA server."""
        if self._client:
            for sub in self._subscriptions.values():
                try:
                    sub.delete()
                except Exception as e:
                    _logger.warning(f"Error deleting subscription: {e}")
            self._subscriptions.clear()
            self._handlers.clear()
            self._client.disconnect()
            self._client = None
            self._status = OPCUAConnectionStatus.DISCONNECTED
            _logger.info("Disconnected from OPC UA server")
    
    def get_status(self) -> OPCUAConnectionStatus:
        """Get current connection status."""
        return self._status
    
    def read_node(self, node_id: str) -> Any:
        """
        Read value from a node.
        
        Args:
            node_id: Node ID (e.g., "ns=2;s=MyDevice.Temperature")
            
        Returns:
            Node value
        """
        if not self._client or self._status != OPCUAConnectionStatus.CONNECTED:
            raise RuntimeError("Client is not connected to server")
        
        try:
            node = self._client.get_node(node_id)
            value = node.get_value()
            _logger.debug(f"Read node {node_id}: {value}")
            return value
        except Exception as e:
            _logger.error(f"Error reading node {node_id}: {e}")
            raise
    
    def write_node(self, node_id: str, value: Any) -> bool:
        """
        Write value to a node.
        
        Args:
            node_id: Node ID
            value: Value to write
            
        Returns:
            True if write successful, False otherwise
        """
        if not self._client or self._status != OPCUAConnectionStatus.CONNECTED:
            raise RuntimeError("Client is not connected to server")
        
        try:
            node = self._client.get_node(node_id)
            node.set_value(value)
            _logger.debug(f"Wrote to node {node_id}: {value}")
            return True
        except Exception as e:
            _logger.error(f"Error writing to node {node_id}: {e}")
            return False
    
    def subscribe_data_change(
        self,
        node_id: str,
        handler: SubHandler,
        subscription_id: str = "default"
    ) -> Optional[Subscription]:
        """
        Subscribe to data change events for a node.
        
        Args:
            node_id: Node ID to monitor
            handler: Subscription handler object
            subscription_id: Unique identifier for the subscription
            
        Returns:
            Subscription object if successful, None otherwise
        """
        if not self._client or self._status != OPCUAConnectionStatus.CONNECTED:
            raise RuntimeError("Client is not connected to server")
        
        try:
            if subscription_id in self._subscriptions:
                _logger.warning(f"Subscription {subscription_id} already exists")
                return self._subscriptions[subscription_id]
            
            node = self._client.get_node(node_id)
            subscription = self._client.create_subscription(1000, handler)
            subscription.subscribe_data_change(node)
            
            self._subscriptions[subscription_id] = subscription
            self._handlers[subscription_id] = handler
            
            _logger.info(f"Created subscription {subscription_id} for node {node_id}")
            return subscription
        except Exception as e:
            _logger.error(f"Error creating subscription for node {node_id}: {e}")
            return None
    
    def call_method(
        self,
        object_id: str,
        method_id: str,
        *args: Any
    ) -> Any:
        """
        Call a method on an object.
        
        Args:
            object_id: Object node ID
            method_id: Method node ID
            *args: Method arguments
            
        Returns:
            Method result
        """
        if not self._client or self._status != OPCUAConnectionStatus.CONNECTED:
            raise RuntimeError("Client is not connected to server")
        
        try:
            obj = self._client.get_node(object_id)
            method = self._client.get_node(method_id)
            result = obj.call_method(method, *args)
            _logger.debug(f"Called method {method_id} on {object_id}: {result}")
            return result
        except Exception as e:
            _logger.error(f"Error calling method {method_id}: {e}")
            raise
    
    def browse_nodes(self, node_id: str = "i=85") -> List[Dict[str, Any]]:
        """
        Browse children of a node.
        
        Args:
            node_id: Parent node ID (default: RootFolder)
            
        Returns:
            List of child node information dictionaries
        """
        if not self._client or self._status != OPCUAConnectionStatus.CONNECTED:
            raise RuntimeError("Client is not connected to server")
        
        try:
            node = self._client.get_node(node_id)
            children = node.get_children()
            
            result = []
            for child in children:
                result.append({
                    "node_id": str(child.nodeid),
                    "browse_name": child.get_browse_name().Name,
                    "display_name": child.get_display_name().Text
                })
            
            return result
        except Exception as e:
            _logger.error(f"Error browsing node {node_id}: {e}")
            raise
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


class EnergyOPCUAServer:
    """
    High-level OPC UA server for energy system data exposure.
    
    This class provides a simplified interface for creating an OPC UA server
    and exposing energy system data to external clients.
    """
    
    def __init__(
        self,
        name: str = "PyXESXXN Energy Server",
        endpoint_url: str = "opc.tcp://0.0.0.0:4840/freeopcua/server/",
        namespace: str = "http://pyxesxxn.org/energy"
    ):
        """
        Initialize EnergyOPCUA server.
        
        Args:
            name: Server name
            endpoint_url: Server endpoint URL
            namespace: Namespace URI
        """
        if not _opcua_available:
            raise ImportError("OPC UA library is not available. Please install required dependencies.")
        
        self.name = name
        self.endpoint_url = endpoint_url
        self.namespace_uri = namespace
        self._server: Optional[Server] = None
        self._is_running = False
        
    def start(self) -> bool:
        """
        Start OPC UA server.
        
        Returns:
            True if server started successfully, False otherwise
        """
        try:
            self._server = Server()
            self._server.set_endpoint(self.endpoint_url)
            self._server.set_server_name(self.name)
            
            idx = self._server.register_namespace(self.namespace_uri)
            objects = self._server.get_objects_node()
            
            self._server.start()
            self._is_running = True
            _logger.info(f"OPC UA server started at {self.endpoint_url}")
            return True
        except Exception as e:
            _logger.error(f"Failed to start OPC UA server: {e}")
            return False
    
    def stop(self) -> None:
        """Stop OPC UA server."""
        if self._server and self._is_running:
            self._server.stop()
            self._is_running = False
            _logger.info("OPC UA server stopped")
    
    def add_variable(
        self,
        parent_id: str,
        node_id: str,
        browse_name: str,
        initial_value: Any = None,
        description: str = ""
    ) -> Optional[Node]:
        """
        Add a variable node to the address space.
        
        Args:
            parent_id: Parent node ID
            node_id: Variable node ID
            browse_name: Browse name for the variable
            initial_value: Initial value
            description: Variable description
            
        Returns:
            Node object if successful, None otherwise
        """
        if not self._server or not self._is_running:
            raise RuntimeError("Server is not running")
        
        try:
            parent = self._server.get_node(parent_id)
            var = parent.add_variable(idx=self._server.get_namespace_index(self.namespace_uri),
                                     nodeid=node_id,
                                     browse_name=browse_name,
                                     initial_value=initial_value)
            if description:
                var.set_attribute(13, description)
            _logger.info(f"Added variable {browse_name} to {parent_id}")
            return var
        except Exception as e:
            _logger.error(f"Error adding variable {browse_name}: {e}")
            return None
    
    def add_object(
        self,
        parent_id: str,
        node_id: str,
        browse_name: str,
        description: str = ""
    ) -> Optional[Node]:
        """
        Add an object node to the address space.
        
        Args:
            parent_id: Parent node ID
            node_id: Object node ID
            browse_name: Browse name for the object
            description: Object description
            
        Returns:
            Node object if successful, None otherwise
        """
        if not self._server or not self._is_running:
            raise RuntimeError("Server is not running")
        
        try:
            parent = self._server.get_node(parent_id)
            obj = parent.add_object(idx=self._server.get_namespace_index(self.namespace_uri),
                                    nodeid=node_id,
                                    browse_name=browse_name)
            if description:
                obj.set_attribute(13, description)
            _logger.info(f"Added object {browse_name} to {parent_id}")
            return obj
        except Exception as e:
            _logger.error(f"Error adding object {browse_name}: {e}")
            return None
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


def check_opcua_available() -> bool:
    """
    Check if OPC UA library is available.
    
    Returns:
        True if available, False otherwise
    """
    return _opcua_available


def get_opcua_version() -> Optional[str]:
    """
    Get OPC UA library version.
    
    Returns:
        Version string if available, None otherwise
    """
    if _opcua_available:
        try:
            from pyxesxxn.energyopcua.opcua import __version__
            return __version__
        except (ImportError, AttributeError):
            return "unknown"
    return None
