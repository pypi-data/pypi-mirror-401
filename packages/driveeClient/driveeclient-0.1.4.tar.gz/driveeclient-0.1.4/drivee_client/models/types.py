"""Shared types and enums used across the Drivee integration."""

from enum import Enum

class ChargePointStatus(str, Enum):
    """Valid charge point operational statuses."""
    AVAILABLE = "Available"
    PREPARING = "Preparing"
    CHARGING = "Charging"
    FINISHING = "Finishing"

class EVSEStatus(str, Enum):
    """Valid EVSE operational statuses."""
    AVAILABLE = "Available"
    CHARGING = "charging"
    SUSPENDED = "suspended"
    PENDING = "pending"
    READY = "ready"
    PREPARING = "preparing"
    FINISHING = "finishing"

class ConnectorStatus(str, Enum):
    """Valid connector operational statuses."""
    AVAILABLE = "Available"
    ACTIVE = "active"

class ConnectorType(str, Enum):
    """Valid connector types."""
    TYPE1 = "Type1"
    TYPE2 = "Type2"
    CCS = "CCS"
    CHADEMO = "CHAdeMO"
    TESLA = "Tesla"
    NACS = "NACS"

class ConnectorFormat(str, Enum):
    """Valid connector physical formats."""
    SOCKET = "socket"
    CABLE = "cable"

class ChargingSessionStatus(str, Enum):
    """Valid charging session statuses."""
    ACTIVE = "Active"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    STOPPED = "Stopped"