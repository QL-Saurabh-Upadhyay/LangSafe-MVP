"""
Configuration management for QL Tracker.

This module handles loading and parsing the trackconfig.toml configuration file.
"""

from pathlib import Path
from typing import Any, Dict, Optional

try:
    import tomllib
except ImportError:
    import tomli as tomllib


class TrackerConfig:
    """Configuration class for QL Tracker."""
    
    def __init__(self) -> None:
        self.api_key: Optional[str] = None
        self.host: Optional[str] = None
        self.log_to_file: bool = False
        self.log_file_path: Optional[str] = None
        self.pretty_print: bool = True
        self.enable_logging: bool = True
        self.log_level: str = "INFO"
        
        # Queue settings
        self.queue_max_batch_size: int = 10
        self.queue_flush_interval_secs: float = 5.0
        
        # Storage settings
        self.storage_backend: str = "remote"
        self.storage_output_path: str = "logs/ql-tracker.jsonl"
    
    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration from a dictionary."""
        if "log_to_file" in config_dict:
            self.log_to_file = bool(config_dict["log_to_file"])
        
        if "log_file_path" in config_dict:
            self.log_file_path = str(config_dict["log_file_path"])
        
        if "pretty_print" in config_dict:
            self.pretty_print = bool(config_dict["pretty_print"])
        
        if "enable_logging" in config_dict:
            self.enable_logging = bool(config_dict["enable_logging"])
        
        if "log_level" in config_dict:
            self.log_level = str(config_dict["log_level"])
        
        # Queue settings
        if "queue" in config_dict:
            queue_config = config_dict["queue"]
            if "max_batch_size" in queue_config:
                self.queue_max_batch_size = int(queue_config["max_batch_size"])
            if "flush_interval_secs" in queue_config:
                self.queue_flush_interval_secs = float(queue_config["flush_interval_secs"])
        
        # Storage settings
        if "storage" in config_dict:
            storage_config = config_dict["storage"]
            if "backend" in storage_config:
                self.storage_backend = str(storage_config["backend"])
            if "output_path" in storage_config:
                self.storage_output_path = str(storage_config["output_path"])


# Global configuration instance
_config = TrackerConfig()


def load_config(config_path: Optional[str] = None) -> TrackerConfig:
    """
    Load configuration from trackconfig.toml file.
    
    Args:
        config_path: Optional path to the configuration file.
                    If None, looks for trackconfig.toml in current directory.
    
    Returns:
        TrackerConfig: The loaded configuration object.
    """
    global _config
    
    if config_path is None:
        config_path = "trackconfig.toml"
    
    config_file = Path(config_path)
    
    if not config_file.exists():
        return _config
    
    try:
        with open(config_file, "rb") as f:
            config_data = tomllib.load(f)
        
        # Extract tracker configuration
        tracker_config = config_data.get("tracker", {})
        _config.update_from_dict(tracker_config)
        
    except Exception as e:
        # If there's an error loading config, use defaults
        print(f"Warning: Could not load configuration from {config_path}: {e}")
    
    return _config


def get_config() -> TrackerConfig:
    """
    Get the current configuration.
    
    Returns:
        TrackerConfig: The current configuration object.
    """
    return _config


def reset_config() -> None:
    """Reset configuration to defaults."""
    global _config
    _config = TrackerConfig() 