"""
This module defines a virtual base class that is used only for static type checking purposes.
tno.mpc.mpyc.floating_point.SecureFloatingPoint derives from this base class during static type
checking so that it can "share" type annotations with mpyc.sectypes.SecureFloat.
"""

from mpyc.sectypes import SecureNumber


class BaseSecureFloat(SecureNumber):
    """
    Virtual base class that serves as common parent to both SecureFloat and
    tno.mpc.mpyc.floating_point.SecureFloatingPoint during static type checking.
    """
