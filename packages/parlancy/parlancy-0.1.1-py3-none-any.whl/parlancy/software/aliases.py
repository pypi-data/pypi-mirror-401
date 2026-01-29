from typing import NewType, Literal
from parlancy.filesystem import AbsolutePath

PackageName = NewType("PackageName", str)
"""A software package identifer - it's name"""

PackageVersion = NewType("PackageVersion", str)
"""A software package version identifier - using SemVer"""

PackagePath = NewType("PackagePath", AbsolutePath)
"""A path to the package's root directory - required: absolute path"""

VersionReleaseType = Literal["MAJOR","MINOR","PATCH"]