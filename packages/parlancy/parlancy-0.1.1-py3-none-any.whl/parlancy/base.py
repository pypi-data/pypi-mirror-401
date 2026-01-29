from typing_extensions import TypedDict

TypeGuardBaseOpts = TypedDict("TypeGuardBaseOpts", { "check": bool, "resolve": bool, "throw": bool }, total=False)
