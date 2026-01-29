from typing import Protocol

class SkillFunction(Protocol):
    """MCP Skill Interface"""
    __name__: str
    __doc__: str | None
