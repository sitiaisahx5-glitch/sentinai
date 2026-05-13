#!/usr/bin/env python3
"""SentinelAI Configuration — Centralized configuration management."""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ScanConfig:
    """Scan engine configuration."""
    max_concurrent_agents: int = 5
    scan_timeout: int = 300  # seconds
    max_file_size: int = 1_000_000  # 1MB
    excluded_dirs: List[str] = field(default_factory=lambda: [
        "__pycache__", ".git", "node_modules", "venv", ".venv",
        "dist", "build", ".tox", ".mypy_cache",
    ])
    excluded_extensions: List[str] = field(default_factory=lambda: [
        ".pyc", ".pyo", ".so", ".dll", ".exe", ".bin",
        ".jpg", ".png", ".gif", ".mp4", ".zip", ".tar",
    ])


@dataclass
class AgentConfig:
    """Agent-specific configuration."""
    static_analyzer_enabled: bool = True
    vuln_detector_enabled: bool = True
    vuln_detector_model: str = "mimo-v2.5-pro"
    vuln_detector_confidence: float = 0.7
    code_quality_enabled: bool = True
    code_quality_max_complexity: int = 15
    code_quality_max_lines: int = 50
    dependency_checker_enabled: bool = True
    secrets_scanner_enabled: bool = True
    secrets_scanner_entropy: float = 4.5


@dataclass
class DashboardConfig:
    """Dashboard configuration."""
    host: str = "0.0.0.0"
    port: int = 8081
    debug: bool = False
    ws_update_interval: float = 1.5  # seconds


@dataclass
class AppConfig:
    """Main application configuration."""
    scan: ScanConfig = field(default_factory=ScanConfig)
    agents: AgentConfig = field(default_factory=AgentConfig)
    dashboard: DashboardConfig = field(default_factory=DashboardConfig)
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        return cls(
            scan=ScanConfig(
                max_concurrent_agents=int(os.getenv("SCAN_MAX_AGENTS", "5")),
                scan_timeout=int(os.getenv("SCAN_TIMEOUT", "300")),
            ),
            agents=AgentConfig(
                vuln_detector_model=os.getenv("MIMO_MODEL", "mimo-v2.5-pro"),
            ),
            dashboard=DashboardConfig(
                port=int(os.getenv("PORT", "8081")),
                debug=os.getenv("DEBUG", "false").lower() == "true",
            ),
        )


# Default configuration
DEFAULT_CONFIG = AppConfig()
