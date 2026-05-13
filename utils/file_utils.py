#!/usr/bin/env python3
"""SentinelAI Utilities — Helper functions for file analysis."""

import hashlib
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


def get_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def count_lines(file_path: str) -> Tuple[int, int, int]:
    """Count total, code, and comment lines in a file."""
    total = 0
    code = 0
    comments = 0
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            in_multiline = False
            for line in f:
                total += 1
                stripped = line.strip()
                
                if not stripped:
                    continue
                
                # Python multi-line strings
                if '"""' in stripped or "'''" in stripped:
                    in_multiline = not in_multiline
                    comments += 1
                elif in_multiline:
                    comments += 1
                elif stripped.startswith("#"):
                    comments += 1
                else:
                    code += 1
    except Exception:
        pass
    
    return total, code, comments


def scan_directory(
    root: str,
    extensions: Set[str] = None,
    exclude_dirs: Set[str] = None,
) -> List[Dict]:
    """Scan directory for source files."""
    if extensions is None:
        extensions = {".py", ".js", ".ts", ".java", ".go", ".rs", ".c", ".cpp"}
    
    if exclude_dirs is None:
        exclude_dirs = {
            "__pycache__", ".git", "node_modules", "venv", ".venv",
            "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
        }
    
    files = []
    root_path = Path(root)
    
    for path in root_path.rglob("*"):
        if path.is_file() and path.suffix in extensions:
            # Check if any parent directory is excluded
            if any(excluded in path.parts for excluded in exclude_dirs):
                continue
            
            total, code, comments = count_lines(str(path))
            
            files.append({
                "path": str(path.relative_to(root_path)),
                "absolute": str(path),
                "extension": path.suffix,
                "size": path.stat().st_size,
                "total_lines": total,
                "code_lines": code,
                "comment_lines": comments,
                "hash": get_file_hash(str(path)),
            })
    
    return sorted(files, key=lambda f: f["path"])


def extract_imports(file_path: str) -> List[str]:
    """Extract import statements from Python file."""
    imports = []
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("import ") or stripped.startswith("from "):
                    imports.append(stripped)
    except Exception:
        pass
    
    return imports


def calculate_complexity(file_path: str) -> int:
    """Estimate cyclomatic complexity of Python file."""
    complexity = 1  # Base complexity
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
            # Count decision points
            patterns = [
                r"\bif\b", r"\belif\b", r"\bfor\b", r"\bwhile\b",
                r"\band\b", r"\bor\b", r"\bexcept\b", r"\bwith\b",
            ]
            
            for pattern in patterns:
                complexity += len(re.findall(pattern, content))
    except Exception:
        pass
    
    return complexity


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
