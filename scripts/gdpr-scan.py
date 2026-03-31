#!/usr/bin/env python3
"""
GDPR/DSGVO Pre-Commit Scanner for Claude Code.

Scans staged files for personal data patterns before allowing git commit.
Runs as a PreToolUse hook — blocks commit if sensitive data is found.

Patterns detected:
  - Real email addresses (not @example.org/com/net)
  - JWT tokens (eyJ...)
  - Swiss AHV/SSN numbers (756.XXXX.XXXX.XX)
  - IBAN numbers
  - Phone numbers (CH/DE/FR/AT formats)
  - API keys / tokens / secrets in assignments
  - Connection strings with passwords
  - Private keys (RSA/EC/SSH)
  - Hardcoded passwords in config files

Exit code 0 = clean, exit code 1 = blocked (findings reported).
Reads tool_input from stdin (Claude Code hook format).

Zero tokens — pure Python.
"""

import sys
import json
import os
import re
import subprocess
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# File extensions to scan (skip binaries, images, etc.)
SCAN_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".xml", ".html", ".htm",
    ".cs", ".py", ".js", ".ts", ".tsx", ".jsx", ".css", ".scss",
    ".sql", ".sh", ".bash", ".ps1", ".bat", ".cmd",
    ".env", ".config", ".cfg", ".ini", ".toml",
    ".csproj", ".sln", ".props",
}

# Files to always skip
SKIP_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "CHANGELOG.md", "changelog.md",
}

# Directories to skip
SKIP_DIRS = {"node_modules", "bin", "obj", ".git", "dist", "build", "__pycache__"}

# Safe email domains (not flagged)
SAFE_EMAIL_DOMAINS = {
    "example.org", "example.com", "example.net",
    "demoarchiv.example", "test.example",
    "localhost", "noreply",
}

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "name": "REAL_EMAIL",
        "description": "Real email address (not @example.org/com)",
        "regex": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "severity": "high",
        "filter": lambda m: not any(m.group().lower().endswith(f"@{d}") for d in SAFE_EMAIL_DOMAINS)
                            and not m.group().lower().endswith("@anthropic.com")
                            and "@" in m.group(),
    },
    {
        "name": "JWT_TOKEN",
        "description": "JWT token (may contain personal data in payload)",
        "regex": r'eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]+',
        "severity": "critical",
    },
    {
        "name": "AHV_NUMBER",
        "description": "Swiss AHV/SSN number (756.XXXX.XXXX.XX)",
        "regex": r'756\.\d{4}\.\d{4}\.\d{2}',
        "severity": "critical",
    },
    {
        "name": "IBAN",
        "description": "IBAN number",
        "regex": r'\b[A-Z]{2}\d{2}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{0,4}\b',
        "severity": "critical",
    },
    {
        "name": "PHONE_CH_DE",
        "description": "Phone number (CH/DE/AT/FR format)",
        "regex": r'(?<!\d)(\+41|0041|0\d{2})[\s./-]?\d{3}[\s./-]?\d{2}[\s./-]?\d{2}(?!\d)',
        "severity": "medium",
        "filter": lambda m: m.group().replace(" ", "").replace("-", "") != "+41000000000",
    },
    {
        "name": "PHONE_DE",
        "description": "German phone number",
        "regex": r'(?<!\d)(\+49|0049|0\d{2,4})[\s./-]?\d{3,4}[\s./-]?\d{2,4}[\s./-]?\d{0,4}(?!\d)',
        "severity": "medium",
        "filter": lambda m: len(re.sub(r'\D', '', m.group())) >= 10,
    },
    {
        "name": "API_KEY_ASSIGNMENT",
        "description": "API key or secret in assignment",
        "regex": r'(?i)(api[_-]?key|api[_-]?secret|access[_-]?token|auth[_-]?token|secret[_-]?key|private[_-]?key|client[_-]?secret)\s*[=:]\s*["\']?[A-Za-z0-9_\-/.+]{20,}',
        "severity": "high",
        "filter": lambda m: "CHANGE_ME" not in m.group() and "placeholder" not in m.group().lower()
                            and "${" not in m.group() and "{{" not in m.group(),
    },
    {
        "name": "CONNECTION_STRING",
        "description": "Connection string with password",
        "regex": r'(?i)(password|pwd)\s*=\s*["\']?[^"\'\s;]{3,}',
        "severity": "high",
        "filter": lambda m: "CHANGE_ME" not in m.group() and "${" not in m.group()
                            and "{{" not in m.group() and "placeholder" not in m.group().lower(),
    },
    {
        "name": "PRIVATE_KEY",
        "description": "Private key header",
        "regex": r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
        "severity": "critical",
    },
    {
        "name": "SK_ANT_TOKEN",
        "description": "Anthropic API token (sk-ant-*)",
        "regex": r'sk-ant-[a-zA-Z0-9_-]{20,}',
        "severity": "critical",
    },
    {
        "name": "GENERIC_SECRET",
        "description": "Generic secret/password pattern",
        "regex": r'(?i)(password|passwd|secret)\s*[=:]\s*["\'][^"\']{8,}["\']',
        "severity": "high",
        "filter": lambda m: "CHANGE_ME" not in m.group() and "example" not in m.group().lower()
                            and "placeholder" not in m.group().lower(),
    },
]

# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def get_staged_files():
    """Get list of staged files from git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return []
        return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
    except Exception:
        return []


def get_staged_content(filepath):
    """Get staged content of a file."""
    try:
        result = subprocess.run(
            ["git", "show", f":{filepath}"],
            capture_output=True, text=True, timeout=10,
        )
        return result.stdout if result.returncode == 0 else ""
    except Exception:
        return ""


def should_scan(filepath):
    """Check if file should be scanned."""
    name = os.path.basename(filepath)
    if name in SKIP_FILES:
        return False

    parts = Path(filepath).parts
    if any(d in SKIP_DIRS for d in parts):
        return False

    ext = os.path.splitext(filepath)[1].lower()
    if ext not in SCAN_EXTENSIONS:
        return False

    return True


def scan_content(content, filepath):
    """Scan content for GDPR-relevant patterns."""
    findings = []

    for i, line in enumerate(content.split("\n"), 1):
        for pattern in PATTERNS:
            for match in re.finditer(pattern["regex"], line):
                # Apply custom filter if present
                if "filter" in pattern:
                    if not pattern["filter"](match):
                        continue

                findings.append({
                    "file": filepath,
                    "line": i,
                    "pattern": pattern["name"],
                    "severity": pattern["severity"],
                    "description": pattern["description"],
                    "match": match.group()[:80],  # Truncate for safety
                })

    return findings


# ---------------------------------------------------------------------------
# Main (Hook Mode)
# ---------------------------------------------------------------------------

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Only run on git commit commands
    cmd = hook_input.get("tool_input", {}).get("command", "")
    if not cmd.strip().startswith("git commit"):
        sys.exit(0)

    # Get staged files
    files = get_staged_files()
    if not files:
        sys.exit(0)

    all_findings = []

    for filepath in files:
        if not should_scan(filepath):
            continue

        content = get_staged_content(filepath)
        if not content:
            continue

        findings = scan_content(content, filepath)
        all_findings.extend(findings)

    if not all_findings:
        # Clean — allow commit
        sys.exit(0)

    # Block commit — report findings
    critical = [f for f in all_findings if f["severity"] == "critical"]
    high = [f for f in all_findings if f["severity"] == "high"]
    medium = [f for f in all_findings if f["severity"] == "medium"]

    lines = []
    lines.append("GDPR/DSGVO SCAN: Potential personal data found in staged files!")
    lines.append(f"  {len(critical)} critical | {len(high)} high | {len(medium)} medium")
    lines.append("")

    for f in all_findings:
        severity_icon = {"critical": "!!!", "high": "!!", "medium": "!"}.get(f["severity"], "?")
        lines.append(f"  [{severity_icon}] {f['file']}:{f['line']} — {f['description']}")
        # Mask sensitive data in output (show first/last 4 chars only)
        masked = f["match"][:4] + "****" + f["match"][-4:] if len(f["match"]) > 12 else "****"
        lines.append(f"       Match: {masked}")

    lines.append("")
    lines.append("Commit blocked. Fix the findings above before committing.")
    lines.append("If this is a false positive, use: git commit --no-verify")

    result = {
        "decision": "block",
        "reason": "\n".join(lines)
    }
    print(json.dumps(result))
    sys.exit(0)


# ---------------------------------------------------------------------------
# Standalone Mode (manual scan)
# ---------------------------------------------------------------------------

def scan_directory(directory):
    """Scan a directory for GDPR-relevant patterns (standalone mode)."""
    all_findings = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            filepath = os.path.join(root, name)
            rel_path = os.path.relpath(filepath, directory)

            if not should_scan(rel_path):
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                findings = scan_content(content, rel_path)
                all_findings.extend(findings)
            except Exception:
                continue

    return all_findings


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        # Standalone mode: scan a directory
        directory = sys.argv[1]
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a directory")
            sys.exit(1)

        findings = scan_directory(directory)

        if not findings:
            print("GDPR scan: No personal data patterns found.")
            sys.exit(0)

        critical = [f for f in findings if f["severity"] == "critical"]
        high = [f for f in findings if f["severity"] == "high"]
        medium = [f for f in findings if f["severity"] == "medium"]

        print(f"GDPR SCAN: {len(findings)} findings ({len(critical)} critical, {len(high)} high, {len(medium)} medium)")
        print()

        for f in findings:
            icon = {"critical": "!!!", "high": "!!", "medium": "!"}.get(f["severity"], "?")
            masked = f["match"][:4] + "****" + f["match"][-4:] if len(f["match"]) > 12 else "****"
            print(f"  [{icon}] {f['file']}:{f['line']} — {f['description']} — {masked}")

        sys.exit(1 if critical or high else 0)
    else:
        # Hook mode: read from stdin
        main()
