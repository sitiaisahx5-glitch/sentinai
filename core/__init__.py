#!/usr/bin/env python3
"""
SentinelAI — Multi-Agent Code Security Analysis Platform
=========================================================

5 specialized AI agents collaborate to detect vulnerabilities,
analyze code quality, and provide actionable security insights.

Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    SentinelAI Core Engine                    │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Static   │  │ Vuln     │  │ Code     │  │ Dep      │   │
│  │ Analyzer │  │ Detector │  │ Quality  │  │ Checker  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │              │              │              │         │
│  ┌────┴──────────────┴──────────────┴──────────────┴─────┐  │
│  │              Event Bus (Pub/Sub)                      │  │
│  └────┬──────────────┬──────────────┬──────────────┬─────┘  │
│       │              │              │              │         │
│  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  │
│  │ Report   │  │ Dashboard│  │ Alert    │  │ Fix      │  │
│  │ Generator│  │ Server   │  │ System   │  │ Suggester│  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘

Author: sitiaisahx5-glitch
License: MIT
"""

__version__ = "2.0.0"
__author__ = "sitiaisahx5-glitch"
