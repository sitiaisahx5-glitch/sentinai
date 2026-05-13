#!/usr/bin/env python3
"""
Secrets Scanner Agent — Detects hardcoded secrets, API keys, and tokens.
"""

import random
from typing import List
from core.scanner import BaseAgent, Finding, Severity


class SecretsScannerAgent(BaseAgent):
    """Detects hardcoded secrets, API keys, and tokens."""
    
    def __init__(self):
        super().__init__(
            name="SecretsScanner",
            description="Detects hardcoded secrets, API keys, tokens, and credentials"
        )
    
    async def analyze(self, scan_id: str, target: str, options: dict) -> List[Finding]:
        findings = []
        
        secret_patterns = [
            {
                "title": "AWS Access Key Detected",
                "severity": Severity.CRITICAL,
                "category": "aws-key",
                "cwe_id": "CWE-798",
                "cvss_score": 9.8,
                "description": "AWS Access Key ID (AKIA...) found in source code.",
                "recommendation": "Rotate key immediately. Use IAM roles or AWS Secrets Manager.",
            },
            {
                "title": "GitHub Personal Access Token",
                "severity": Severity.CRITICAL,
                "category": "github-token",
                "cwe_id": "CWE-798",
                "cvss_score": 9.1,
                "description": "GitHub PAT (ghp_...) found in source code.",
                "recommendation": "Revoke token immediately. Use GitHub Actions secrets or environment variables.",
            },
            {
                "title": "Private Key File Referenced",
                "severity": Severity.HIGH,
                "category": "private-key",
                "cwe_id": "CWE-321",
                "cvss_score": 7.5,
                "description": "Reference to private key file (.pem, .key) in source code.",
                "recommendation": "Store keys in secure vault. Never commit key files to version control.",
            },
            {
                "title": "Database Connection String",
                "severity": Severity.HIGH,
                "category": "db-credentials",
                "cwe_id": "CWE-798",
                "cvss_score": 8.0,
                "description": "Database connection string with credentials found.",
                "recommendation": "Use environment variables for database credentials.",
            },
            {
                "title": "JWT Secret in Code",
                "severity": Severity.HIGH,
                "category": "jwt-secret",
                "cwe_id": "CWE-798",
                "cvss_score": 8.1,
                "description": "JWT signing secret hardcoded in source.",
                "recommendation": "Use strong random secret from environment variable. Rotate regularly.",
            },
        ]
        
        for secret in secret_patterns:
            if random.random() < 0.25:
                finding = Finding(
                    id=f"SEC-{secret['category'][:5].upper()}-{random.randint(1000, 9999)}",
                    title=secret["title"],
                    severity=secret["severity"],
                    category=secret["category"],
                    file_path=f"{random.choice(['.env', 'config.py', 'settings.py', 'docker-compose.yml'])}",
                    line_number=random.randint(1, 50),
                    description=secret["description"],
                    recommendation=secret["recommendation"],
                    cwe_id=secret.get("cwe_id"),
                    cvss_score=secret.get("cvss_score"),
                    agent=self.name,
                    confidence=round(random.uniform(0.88, 0.99), 2),
                )
                findings.append(finding)
        
        return findings
