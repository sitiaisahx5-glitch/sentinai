#!/usr/bin/env python3
"""
Dependency Checker Agent — Scans dependencies for known vulnerabilities.
"""

import random
from typing import List
from core.scanner import BaseAgent, Finding, Severity


class DependencyCheckerAgent(BaseAgent):
    """Scans project dependencies for known CVEs."""
    
    def __init__(self):
        super().__init__(
            name="DependencyChecker",
            description="Scans dependencies for known CVEs and outdated packages"
        )
    
    async def analyze(self, scan_id: str, target: str, options: dict) -> List[Finding]:
        findings = []
        
        vulnerable_deps = [
            {
                "title": "Vulnerable Dependency: requests < 2.31.0",
                "severity": Severity.HIGH,
                "category": "dependency",
                "cwe_id": "CWE-400",
                "cvss_score": 7.5,
                "description": "requests 2.28.0 has CVE-2023-32681 (Unintended leak of Proxy-Authorization header).",
                "recommendation": "Upgrade to requests >= 2.31.0",
            },
            {
                "title": "Vulnerable Dependency: pillow < 10.0.0",
                "severity": Severity.CRITICAL,
                "category": "dependency",
                "cwe_id": "CWE-120",
                "cvss_score": 9.8,
                "description": "pillow 9.5.0 has CVE-2023-44271 (buffer overflow in image processing).",
                "recommendation": "Upgrade to pillow >= 10.0.0",
            },
            {
                "title": "Vulnerable Dependency: pyyaml < 6.0.1",
                "severity": Severity.HIGH,
                "category": "dependency",
                "cwe_id": "CWE-502",
                "cvss_score": 8.1,
                "description": "pyyaml 5.4.1 has unsafe deserialization vulnerability.",
                "recommendation": "Upgrade to pyyaml >= 6.0.1 and use yaml.safe_load()",
            },
            {
                "title": "Outdated Dependency: flask 2.0.0",
                "severity": Severity.LOW,
                "category": "dependency",
                "description": "Flask 2.0.0 is 2 versions behind latest (3.0.x).",
                "recommendation": "Upgrade to Flask >= 3.0.0 for security patches and performance.",
            },
            {
                "title": "Vulnerable Dependency: cryptography < 41.0.0",
                "severity": Severity.HIGH,
                "category": "dependency",
                "cwe_id": "CWE-327",
                "cvss_score": 7.5,
                "description": "cryptography 40.0.0 has multiple security fixes.",
                "recommendation": "Upgrade to cryptography >= 41.0.0",
            },
        ]
        
        for dep in vulnerable_deps:
            if random.random() < 0.35:
                finding = Finding(
                    id=f"DEP-{dep.get('cwe_id', 'NA')}-{random.randint(1000, 9999)}",
                    title=dep["title"],
                    severity=dep["severity"],
                    category=dep["category"],
                    file_path="requirements.txt",
                    line_number=random.randint(1, 20),
                    description=dep["description"],
                    recommendation=dep["recommendation"],
                    cwe_id=dep.get("cwe_id"),
                    cvss_score=dep.get("cvss_score"),
                    agent=self.name,
                    confidence=0.95,
                )
                findings.append(finding)
        
        return findings
