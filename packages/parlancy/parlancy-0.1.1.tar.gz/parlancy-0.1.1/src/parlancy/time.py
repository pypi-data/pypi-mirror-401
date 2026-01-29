from typing import NewType

SecondsDuration = NewType("SecondsDuration", int)
"""A duration measured in Seconds"""

MilliSecondsDuration = NewType('MilliSecondDuration', int)
"""A duration measured in Milliseconds"""

MilliSecondEpochTime = NewType("MilliSecondEpochTime", int)
"""EpochTime measured in Milliseconds, used in Typescript/Javascript and Browsers"""

EpochTime = NewType("EpochTime", int)
"""Number of seconds since 1st Jan 1970 - commonly called "Unix Epoch Time""""
