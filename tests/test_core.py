#!/usr/bin/env python3
"""SentinelAI Tests — Unit tests for core components."""

import asyncio
import pytest
from core.scanner import ScanEngine, Severity, ScanStatus, Finding
from agents import StaticAnalyzerAgent, VulnerabilityDetectorAgent


class TestScanEngine:
    """Tests for the scan engine."""
    
    def test_engine_initialization(self):
        engine = ScanEngine()
        assert len(engine.agents) == 0
        assert len(engine.scans) == 0
    
    def test_agent_registration(self):
        engine = ScanEngine()
        agent = StaticAnalyzerAgent()
        engine.register_agent(agent)
        assert "StaticAnalyzer" in engine.agents
    
    def test_stats_empty(self):
        engine = ScanEngine()
        stats = engine.get_stats()
        assert stats["total_scans"] == 0
        assert stats["total_findings"] == 0


class TestFinding:
    """Tests for Finding dataclass."""
    
    def test_finding_creation(self):
        finding = Finding(
            id="TEST-001",
            title="Test Finding",
            severity=Severity.HIGH,
            category="test",
            file_path="test.py",
            line_number=10,
            description="Test description",
            recommendation="Fix it",
        )
        assert finding.id == "TEST-001"
        assert finding.severity == Severity.HIGH
    
    def test_severity_levels(self):
        assert Severity.CRITICAL.value == "critical"
        assert Severity.HIGH.value == "high"
        assert Severity.MEDIUM.value == "medium"
        assert Severity.LOW.value == "low"


class TestAgents:
    """Tests for security agents."""
    
    def test_static_analyzer_init(self):
        agent = StaticAnalyzerAgent()
        assert agent.name == "StaticAnalyzer"
        assert len(agent.patterns) > 0
    
    def test_vuln_detector_init(self):
        agent = VulnerabilityDetectorAgent()
        assert agent.name == "VulnDetector"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
