from pathlib import Path
from typing import Any, NewType, TypeGuard

RelativePath = NewType("RelativePath", Path)
"""File system path, relative to another filesystem object other than the root object"""
def isRelativePath( value: Any ) -> TypeGuard[RelativePath]:
    if isinstance(value, Path):
        return not value.absolute
    return False

AbsolutePath = NewType("AbsolutePath", Path)
"""File system path, relative to the root object"""
def isAbsolutePath( value: Any ) -> TypeGuard[AbsolutePath]:
    if isinstance(value, Path):
        return value.absolute
    return False
