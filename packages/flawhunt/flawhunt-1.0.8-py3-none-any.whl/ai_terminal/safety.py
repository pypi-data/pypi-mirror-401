"""
Safety utilities for FlawHunt CLI.
Contains dangerous command patterns and safety checking functions.
"""
import re
from typing import List

# Dangerous command patterns
DANGEROUS_PATTERNS: List[str] = [
    # Unix/Linux dangerous patterns
    r"rm\s+-rf\s+/\b",
    r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\};\s*:",  # fork bomb
    r"mkfs\.",
    r"dd\s+if=",
    r"^\s*shutdown\b",
    r"^\s*reboot\b",
    r"^\s*halt\b",
    r"\biptables\b.*\bflush\b",
    r"\bchown\s+-R\s+root\b",
    r"\bchmod\s+0{3,4}\b",
    # Windows dangerous patterns
    r"\bdel\s+/[sq]\s+C:\\\*",
    r"\brd\s+/[sq]\s+C:\\",
    r"\bformat\s+C:",
    r"\bfdisk\s+",
    r"\bdiskpart\b",
    r"\breg\s+delete\s+HKLM",
    r"\breg\s+delete\s+HKCU",
    r"\bnetsh\s+firewall\s+set\s+opmode\s+disable",
    r"\bschtasks\s+.*\b/delete\b",
    r"\bwmic\s+.*\bdelete\b",
    r"\bshutdown\s+/[srf]",
    r"\brestart-computer\b",
    r"\bstop-computer\b",
    r"\bremove-item\s+-recurse\s+-force\s+C:\\",
]

def looks_dangerous(cmd: str) -> bool:
    """Check if a command contains dangerous patterns."""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return True
    return False