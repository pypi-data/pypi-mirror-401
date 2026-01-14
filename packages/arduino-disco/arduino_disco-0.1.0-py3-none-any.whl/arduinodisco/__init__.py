from .discovery import discover_boards, DiscoveryResult
from .arduino_db import BoardDefinition
from .ports import SerialPortInfo

__version__ = "0.1.0"

__all__ = [
    "discover_boards",
    "DiscoveryResult",
    "BoardDefinition",
    "SerialPortInfo",
]