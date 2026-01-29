"""
Configuration Management for Entropic Core
Handles tier-based feature access and configuration
"""

import logging
import os
from typing import Any, Dict, Optional

import yaml

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages configuration for different tiers

    Tiers:
    - open_source: Basic features, local only
    - pro: Advanced features, cloud storage
    - enterprise: All features, SLA, support
    """

    DEFAULT_CONFIG = {
        "open_source": {
            "modules": ["core"],
            "cloud_storage": False,
            "max_agents": 50,
            "dashboard": False,
            "api": False,
            "advanced_analytics": False,
            "support_level": "community",
        },
        "pro": {
            "modules": ["core", "advanced"],
            "cloud_storage": True,
            "max_agents": 500,
            "dashboard": "basic",
            "api": True,
            "advanced_analytics": True,
            "support_level": "email",
        },
        "enterprise": {
            "modules": ["core", "advanced", "visualization", "enterprise"],
            "cloud_storage": True,
            "max_agents": -1,  # Unlimited
            "dashboard": "full",
            "api": True,
            "advanced_analytics": True,
            "multi_system": True,
            "compliance": True,
            "support_level": "priority",
            "sla": "99.9%",
        },
    }

    def __init__(self, tier: str = "open_source", config_path: Optional[str] = None):
        """
        Initialize configuration manager

        Args:
            tier: Subscription tier (open_source, pro, enterprise)
            config_path: Optional path to custom config file
        """
        self.tier = tier
        self.config_path = config_path
        self.config = self._load_config()

        logger.info(f"ConfigManager initialized with tier: {tier}")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or defaults"""
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    custom_config = yaml.safe_load(f)
                    logger.info(f"Loaded custom config from {self.config_path}")
                    return custom_config.get(self.tier, self.DEFAULT_CONFIG[self.tier])
            except Exception as e:
                logger.error(f"Error loading custom config: {e}")

        return self.DEFAULT_CONFIG.get(self.tier, self.DEFAULT_CONFIG["open_source"])

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def is_feature_enabled(self, feature: str) -> bool:
        """
        Check if a feature is enabled for current tier

        Args:
            feature: Feature name to check

        Returns:
            True if feature is enabled
        """
        # Check modules
        if feature in [
            "causal_analyzer",
            "predictive_engine",
            "simulation",
            "security",
        ]:
            return "advanced" in self.config.get("modules", [])

        if feature in ["dashboard", "reports", "alerts"]:
            return "visualization" in self.config.get("modules", [])

        if feature in ["orchestrator", "compliance", "marketplace"]:
            return "enterprise" in self.config.get("modules", [])

        # Direct feature checks
        return self.config.get(feature, False)

    def validate_agent_count(self, count: int) -> bool:
        """
        Validate agent count against tier limits

        Args:
            count: Number of agents

        Returns:
            True if within limits
        """
        max_agents = self.config.get("max_agents", 0)

        if max_agents == -1:  # Unlimited
            return True

        return count <= max_agents

    def get_tier_info(self) -> Dict[str, Any]:
        """Get information about current tier"""
        return {
            "tier": self.tier,
            "config": self.config,
            "features": {
                "core_monitoring": True,
                "advanced_analytics": self.is_feature_enabled("advanced_analytics"),
                "dashboard": self.config.get("dashboard", False),
                "api": self.is_feature_enabled("api"),
                "cloud_storage": self.is_feature_enabled("cloud_storage"),
                "multi_system": self.is_feature_enabled("multi_system"),
                "compliance": self.is_feature_enabled("compliance"),
            },
        }

    def upgrade_tier(self, new_tier: str, api_key: Optional[str] = None):
        """
        Upgrade to a different tier

        Args:
            new_tier: Target tier
            api_key: API key for validation (enterprise only)
        """
        if new_tier not in self.DEFAULT_CONFIG:
            raise ValueError(f"Invalid tier: {new_tier}")

        if new_tier == "enterprise" and not api_key:
            raise ValueError("Enterprise tier requires API key")

        self.tier = new_tier
        self.config = self._load_config()
        logger.info(f"Upgraded to tier: {new_tier}")

    def export_config(self, path: str):
        """
        Export current configuration to file

        Args:
            path: Output file path
        """
        try:
            config_data = {self.tier: self.config}

            with open(path, "w") as f:
                yaml.dump(config_data, f, default_flow_style=False)

            logger.info(f"Configuration exported to {path}")
        except Exception as e:
            logger.error(f"Error exporting config: {e}")
            raise
