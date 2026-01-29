"""
Configuration Management - 100% Free & Open Source
"""

from enum import Enum
from typing import Any, Dict


class Tier(Enum):
    """
    Tier enum for backward compatibility.
    Note: All features are 100% free and open source.
    """

    OPEN_SOURCE = "open_source"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class Config:
    """
    Simple configuration manager - NO TIERS, NO RESTRICTIONS.
    All features are completely free and open source.
    """

    def __init__(self, **kwargs):
        """Initialize configuration with custom settings"""
        self.custom_config = kwargs

    def get(self, key: str, default: Any = None) -> Any:
        """Gets configuration value"""
        return self.custom_config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets configuration value"""
        self.custom_config[key] = value

    def has_feature(self, feature: str) -> bool:
        """All features are always available - 100% free"""
        return True

    def can_use_module(self, module: str) -> bool:
        """All modules are always available - 100% free"""
        return True

    def validate_agent_count(self, count: int) -> bool:
        """No limits on agent count - 100% free"""
        return True

    def get_config_info(self) -> Dict[str, Any]:
        """Returns configuration information"""
        return {
            "free_and_open_source": True,
            "no_limits": True,
            "all_features_enabled": True,
            "custom_config": self.custom_config,
        }
