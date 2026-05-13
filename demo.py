#!/usr/bin/env python3
"""
SentinelAI Demo — Demonstrates the multi-agent security scanning platform.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.scanner import ScanEngine, Severity
from agents import (
    StaticAnalyzerAgent,
    VulnerabilityDetectorAgent,
    CodeQualityAgent,
    DependencyCheckerAgent,
    SecretsScannerAgent,
)


async def run_demo():
    """Run a complete security scan demo."""
    print("=" * 70)
    print("🛡️  SentinelAI — Multi-Agent Code Security Platform")
    print("=" * 70)
    
    # Initialize engine
    engine = ScanEngine()
    
    # Register all agents
    agents = [
        StaticAnalyzerAgent(),
        VulnerabilityDetectorAgent(),
        CodeQualityAgent(),
        DependencyCheckerAgent(),
        SecretsScannerAgent(),
    ]
    
    for agent in agents:
        engine.register_agent(agent)
        print(f"  ✓ Registered agent: {agent.name}")
    
    print(f"\n📊 Engine Stats: {len(engine.agents)} agents registered")
    
    # Run a scan
    print("\n" + "=" * 70)
    print("🔍 Starting Security Scan...")
    print("=" * 70)
    
    scan_id = await engine.start_scan("my-web-app", {"deep": True})
    scan = engine.get_scan(scan_id)
    
    print(f"\n📋 Scan ID: {scan_id}")
    print(f"   Status: {scan.status.value}")
    print(f"   Findings: {len(scan.findings)}")
    print(f"   Security Score: {scan.security_score}%")
    
    # Display findings by severity
    print("\n" + "=" * 70)
    print("🚨 Findings by Severity")
    print("=" * 70)
    
    for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
        findings = [f for f in scan.findings if f.severity == severity]
        if findings:
            print(f"\n  {severity.value.upper()} ({len(findings)} findings):")
            for f in findings[:3]:  # Show top 3
                print(f"    • {f.title}")
                print(f"      File: {f.file_path}:{f.line_number}")
                print(f"      Agent: {f.agent} | Confidence: {f.confidence:.0%}")
                if f.cwe_id:
                    print(f"      CWE: {f.cwe_id} | CVSS: {f.cvss_score}")
    
    # Agent performance
    print("\n" + "=" * 70)
    print("🤖 Agent Performance")
    print("=" * 70)
    
    for agent_name in scan.agents_completed:
        agent_findings = [f for f in scan.findings if f.agent == agent_name]
        print(f"  {agent_name}: {len(agent_findings)} findings")
    
    # Overall stats
    print("\n" + "=" * 70)
    print("📈 Platform Statistics")
    print("=" * 70)
    
    stats = engine.get_stats()
    print(f"  Total Scans: {stats['total_scans']}")
    print(f"  Total Findings: {stats['total_findings']}")
    print(f"  Avg Security Score: {stats['avg_security_score']}%")
    print(f"  Critical Findings: {stats['critical_findings']}")
    print(f"  High Findings: {stats['high_findings']}")
    
    print("\n" + "=" * 70)
    print("✅ Scan Complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_demo())
