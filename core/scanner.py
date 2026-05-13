#!/usr/bin/env python3
"""
Core Scanner Engine — Orchestrates all security analysis agents.
Manages scan lifecycle, agent coordination, and result aggregation.
"""

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set
from pathlib import Path


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ScanStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Finding:
    """Represents a security finding."""
    id: str
    title: str
    severity: Severity
    category: str
    file_path: str
    line_number: int
    description: str
    recommendation: str
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    agent: str = ""
    confidence: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ScanResult:
    """Aggregated scan results from all agents."""
    scan_id: str
    target: str
    status: ScanStatus
    findings: List[Finding] = field(default_factory=list)
    agents_completed: Set[str] = field(default_factory=set)
    total_files: int = 0
    total_lines: int = 0
    scan_duration: float = 0.0
    started_at: str = ""
    completed_at: str = ""
    
    @property
    def critical_count(self) -> int:
        return len([f for f in self.findings if f.severity == Severity.CRITICAL])
    
    @property
    def high_count(self) -> int:
        return len([f for f in self.findings if f.severity == Severity.HIGH])
    
    @property
    def medium_count(self) -> int:
        return len([f for f in self.findings if f.severity == Severity.MEDIUM])
    
    @property
    def low_count(self) -> int:
        return len([f for f in self.findings if f.severity == Severity.LOW])
    
    @property
    def security_score(self) -> float:
        """Calculate security score (0-100, higher is better)."""
        if not self.findings:
            return 100.0
        
        weights = {
            Severity.CRITICAL: 25,
            Severity.HIGH: 15,
            Severity.MEDIUM: 8,
            Severity.LOW: 3,
            Severity.INFO: 0,
        }
        
        total_penalty = sum(weights.get(f.severity, 0) for f in self.findings)
        max_penalty = self.total_lines * 0.1  # Normalize by code size
        
        score = max(0, 100 - (total_penalty / max(max_penalty, 1) * 100))
        return round(score, 1)


class EventBus:
    """Pub/sub event system for agent communication."""
    
    def __init__(self):
        self._subscribers: Dict[str, List] = {}
        self._history: List[dict] = []
    
    def subscribe(self, event_type: str, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    
    async def publish(self, event_type: str, data: dict):
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        self._history.append(event)
        
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                await callback(event)
    
    def get_history(self, limit: int = 100) -> List[dict]:
        return self._history[-limit:]


class ScanEngine:
    """Main scanning engine that coordinates all agents."""
    
    def __init__(self):
        self.event_bus = EventBus()
        self.scans: Dict[str, ScanResult] = {}
        self.agents: Dict[str, 'BaseAgent'] = {}
        self._scan_counter = 0
    
    def register_agent(self, agent: 'BaseAgent'):
        """Register a security analysis agent."""
        self.agents[agent.name] = agent
        agent.set_engine(self)
    
    async def start_scan(self, target: str, options: dict = None) -> str:
        """Start a new security scan."""
        self._scan_counter += 1
        scan_id = f"SCAN-{self._scan_counter:06d}"
        
        scan = ScanResult(
            scan_id=scan_id,
            target=target,
            status=ScanStatus.RUNNING,
            started_at=datetime.now().isoformat(),
        )
        self.scans[scan_id] = scan
        
        await self.event_bus.publish("scan_started", {
            "scan_id": scan_id,
            "target": target,
        })
        
        # Run all agents concurrently
        tasks = [
            agent.analyze(scan_id, target, options or {})
            for agent in self.agents.values()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate results
        for agent_name, result in zip(self.agents.keys(), results):
            if isinstance(result, Exception):
                await self.event_bus.publish("agent_error", {
                    "scan_id": scan_id,
                    "agent": agent_name,
                    "error": str(result),
                })
            else:
                scan.findings.extend(result)
                scan.agents_completed.add(agent_name)
        
        scan.status = ScanStatus.COMPLETED
        scan.completed_at = datetime.now().isoformat()
        scan.scan_duration = time.time() - time.time()  # Placeholder
        
        await self.event_bus.publish("scan_completed", {
            "scan_id": scan_id,
            "findings_count": len(scan.findings),
            "security_score": scan.security_score,
        })
        
        return scan_id
    
    def get_scan(self, scan_id: str) -> Optional[ScanResult]:
        return self.scans.get(scan_id)
    
    def get_all_scans(self) -> List[ScanResult]:
        return list(self.scans.values())
    
    def get_stats(self) -> dict:
        total_scans = len(self.scans)
        total_findings = sum(len(s.findings) for s in self.scans.values())
        avg_score = (
            sum(s.security_score for s in self.scans.values()) / total_scans
            if total_scans > 0 else 0
        )
        
        return {
            "total_scans": total_scans,
            "total_findings": total_findings,
            "avg_security_score": round(avg_score, 1),
            "agents_registered": len(self.agents),
            "critical_findings": sum(s.critical_count for s in self.scans.values()),
            "high_findings": sum(s.high_count for s in self.scans.values()),
        }


class BaseAgent:
    """Base class for all security analysis agents."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.engine: Optional[ScanEngine] = None
    
    def set_engine(self, engine: ScanEngine):
        self.engine = engine
    
    async def analyze(self, scan_id: str, target: str, options: dict) -> List[Finding]:
        raise NotImplementedError
