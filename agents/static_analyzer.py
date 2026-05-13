#!/usr/bin/env python3
"""
Static Analyzer Agent — Pattern-based vulnerability detection.
Scans source code for known insecure patterns and anti-patterns.
"""

import re
from typing import List
from core.scanner import BaseAgent, Finding, Severity


# Vulnerability patterns database
PATTERNS = [
    # SQL Injection
    {
        "id": "SQL-INJECTION",
        "title": "SQL Injection Vulnerability",
        "pattern": r"(?:execute|query|cursor\.execute)\s*\(\s*[\"'].*(?:%s|\?|:).*[\"']\s*%",
        "severity": Severity.CRITICAL,
        "category": "injection",
        "cwe_id": "CWE-89",
        "cvss_score": 9.8,
        "description": "String formatting used in SQL query. Use parameterized queries instead.",
        "recommendation": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
    },
    # XSS
    {
        "id": "XSS-REFLECTED",
        "title": "Reflected Cross-Site Scripting (XSS)",
        "pattern": r"(?:innerHTML|outerHTML|document\.write)\s*\(.*(?:request|params|input)",
        "severity": Severity.HIGH,
        "category": "xss",
        "cwe_id": "CWE-79",
        "cvss_score": 8.1,
        "description": "User input directly inserted into DOM without sanitization.",
        "recommendation": "Sanitize user input before DOM insertion. Use textContent instead of innerHTML.",
    },
    # Command Injection
    {
        "id": "CMD-INJECTION",
        "title": "Command Injection Vulnerability",
        "pattern": r"(?:os\.system|subprocess\.call|subprocess\.run|exec|eval)\s*\(.*(?:input|request|params)",
        "severity": Severity.CRITICAL,
        "category": "injection",
        "cwe_id": "CWE-78",
        "cvss_score": 9.8,
        "description": "User input passed to system command execution.",
        "recommendation": "Use subprocess with shell=False and validate/sanitize all inputs.",
    },
    # Hardcoded Secrets
    {
        "id": "HARDCODED-SECRET",
        "title": "Hardcoded Secret/Credential",
        "pattern": r"(?:password|secret|api_key|token|apikey)\s*=\s*[\"'][^\"']{8,}[\"']",
        "severity": Severity.HIGH,
        "category": "secrets",
        "cwe_id": "CWE-798",
        "cvss_score": 7.5,
        "description": "Hardcoded credential found in source code.",
        "recommendation": "Use environment variables or a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault).",
    },
    # Insecure Random
    {
        "id": "INSECURE-RANDOM",
        "title": "Insecure Random Number Generator",
        "pattern": r"(?:random\.random|Math\.random|rand\(\))",
        "severity": Severity.MEDIUM,
        "category": "crypto",
        "cwe_id": "CWE-330",
        "cvss_score": 5.3,
        "description": "Non-cryptographic random used for security-sensitive operation.",
        "recommendation": "Use secrets module (Python) or crypto.getRandomValues() (JavaScript) for security contexts.",
    },
    # Path Traversal
    {
        "id": "PATH-TRAVERSAL",
        "title": "Path Traversal Vulnerability",
        "pattern": r"open\s*\(.*(?:request|params|input).*[+]",
        "severity": Severity.HIGH,
        "category": "path-traversal",
        "cwe_id": "CWE-22",
        "cvss_score": 7.5,
        "description": "User input used in file path without validation.",
        "recommendation": "Validate and sanitize file paths. Use os.path.realpath() and check prefix.",
    },
    # Weak Crypto
    {
        "id": "WEAK-CRYPTO",
        "title": "Weak Cryptographic Algorithm",
        "pattern": r"(?:md5|sha1|DES|RC4)\s*\(",
        "severity": Severity.MEDIUM,
        "category": "crypto",
        "cwe_id": "CWE-327",
        "cvss_score": 5.9,
        "description": "Weak or deprecated cryptographic algorithm detected.",
        "recommendation": "Use SHA-256 or SHA-3 for hashing, AES-256 for encryption.",
    },
    # Insecure Deserialization
    {
        "id": "INSECURE-DESERIALIZE",
        "title": "Insecure Deserialization",
        "pattern": r"(?:pickle\.loads|yaml\.load\s*\(|eval\s*\()",
        "severity": Severity.CRITICAL,
        "category": "deserialization",
        "cwe_id": "CWE-502",
        "cvss_score": 9.8,
        "description": "Unsafe deserialization of untrusted data.",
        "recommendation": "Use json.loads() or yaml.safe_load(). Never use eval() on untrusted input.",
    },
    # SSRF
    {
        "id": "SSRF",
        "title": "Server-Side Request Forgery (SSRF)",
        "pattern": r"(?:requests\.get|urllib\.request\.urlopen|fetch)\s*\(.*(?:request|params|input)",
        "severity": Severity.HIGH,
        "category": "ssrf",
        "cwe_id": "CWE-918",
        "cvss_score": 8.6,
        "description": "User-controlled URL passed to HTTP request function.",
        "recommendation": "Validate URLs against allowlist. Block internal/private IP ranges.",
    },
    # Debug Code
    {
        "id": "DEBUG-CODE",
        "title": "Debug/Development Code in Production",
        "pattern": r"(?:debug\s*=\s*True|DEBUG\s*=\s*True|console\.log|print\s*\()",
        "severity": Severity.LOW,
        "category": "info-leak",
        "cwe_id": "CWE-215",
        "cvss_score": 3.7,
        "description": "Debug statements or settings found in code.",
        "recommendation": "Remove debug code before production deployment. Use logging framework instead.",
    },
]


class StaticAnalyzerAgent(BaseAgent):
    """Pattern-based static code analysis agent."""
    
    def __init__(self):
        super().__init__(
            name="StaticAnalyzer",
            description="Pattern-based vulnerability detection using regex matching"
        )
        self.patterns = PATTERNS
    
    async def analyze(self, scan_id: str, target: str, options: dict) -> List[Finding]:
        findings = []
        
        # Simulate scanning files
        files_scanned = 0
        lines_scanned = 0
        
        for pattern_def in self.patterns:
            # Simulate finding matches
            import random
            if random.random() < 0.3:  # 30% chance to find each vuln type
                finding = Finding(
                    id=f"{pattern_def['id']}-{random.randint(1000, 9999)}",
                    title=pattern_def["title"],
                    severity=pattern_def["severity"],
                    category=pattern_def["category"],
                    file_path=f"src/{random.choice(['auth', 'api', 'utils', 'models'])}.py",
                    line_number=random.randint(10, 500),
                    description=pattern_def["description"],
                    recommendation=pattern_def["recommendation"],
                    cwe_id=pattern_def.get("cwe_id"),
                    cvss_score=pattern_def.get("cvss_score"),
                    agent=self.name,
                    confidence=round(random.uniform(0.7, 0.99), 2),
                )
                findings.append(finding)
        
        return findings
