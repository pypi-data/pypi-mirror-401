from typing import NewType, TypeAlias

IpAddressV4 = NewType("IpAddressV4", str)
"""IP Address (Version 4)"""

IpAddressV6 = NewType("IpAddressV6", str)
"""IP Address (Version 6)"""

type IpAddress = IpAddressV4 | IpAddressV6
"""IP Address"""

HostName = NewType("HostName", str)
"""Computer Host Name"""

DomainName = NewType('DomainName', str)

FQDN = NewType('FQDN', DomainName)
"""Fully Qualified Domain Name"""
