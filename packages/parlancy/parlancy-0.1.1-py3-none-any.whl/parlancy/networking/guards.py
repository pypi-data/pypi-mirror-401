from .aliases import IpAddress, IpAddressV4, IpAddressV6
from typing import TypeGuard, Any



def isIpAddress( value:Any ) -> TypeGuard[IpAddress]:
    """Checks if the string is either a valid IPv4 or IPv6 address."""
    return isIpAddressV4(value) or isIpAddressV6(value)


def isIpAddressV4( value: Any ) -> TypeGuard[IpAddressV4]:
    """Validates IPv4: 4 octets (0-255) separated by 3 periods."""
    try:
        ipaddress.IPv4Address(value)
        return True
    except ValueError:
        return False


def isIpAddressV6( value: Any ) -> TypeGuard[IpAddressV6]:
    """Validates if a string is a correctly formed IPv6 address."""
    try:
        ipaddress.IPv6Address(value)
        return True
    except ValueError:
        return False
