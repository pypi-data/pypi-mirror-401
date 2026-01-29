from pathlib import Path
from typing import NewType


McpSkillName = NewType("McpSkillName", Path)
"""Name of a skill - which in MCP is a categorical to segment functions, resources and tools into"""
