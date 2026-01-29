from typing import get_args, Any, Literal, TypeGuard

FileAccessMode = Literal["r", "rb", "r+", "rb+", "w", "wb", "w+", "wb+", "a", "ab", "a+", "ab+", "x", "xb", "x+", "xb+"]
def isFileAccessMode( value: Any ) -> TypeGuard[FileAccessMode]:
    valid_modes = get_args(FileAccessMode)
    return isinstance(value, str) and value in valid_modes
