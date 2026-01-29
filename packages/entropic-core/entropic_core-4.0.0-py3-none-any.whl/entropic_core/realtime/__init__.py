"""Real-time Dashboard and Streaming Modules"""

from .live_dashboard import (
    DashboardConfig,
    DashboardEvent,
    EventType,
    LiveDashboard,
    create_dashboard,
)

__all__ = [
    "LiveDashboard",
    "DashboardConfig",
    "DashboardEvent",
    "EventType",
    "create_dashboard",
]

__module_version__ = "3.0.0"
