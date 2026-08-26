# libs/__init__.py
import sys, os
sys.path.append(os.path.dirname(__file__))

# ... the rest of your __init__.py code goes below ...
# Core Instrument and Communication Classes
from .instrument import (
    Instrument,
    Rest_Ports,
    ApiError,
    CouldNotConnect,
    NotConnected,
    BadUrl,
    TunnelError,
)
from .genericcryostat import (
    GenericCryostat,
    PidScheduleItem,
    connect_cryostat,
)
from .ssh_tunnel import tunnel

# Montana Instrument Wrappers
from .cryocore import CryoCore
from .rook import Rook
from .xpcryostation import XPCryostation
from .fsr import Fsr

# Optional / Specialized Wrappers (if present in your libs folder)
try:
    from .scryostation import SCryostation
except ImportError:
    pass

# Utilities and Helpers
from .TcPlot import TcPlot
#from .gui_helpers import resource_path, load_ui
from . import mirs_helpers

# Define what gets imported with: from libs import *
__all__ = [
    "Instrument",
    "Rest_Ports",
    "ApiError",
    "CouldNotConnect",
    "NotConnected",
    "BadUrl",
    "TunnelError",
    "GenericCryostat",
    "PidScheduleItem",
    "connect_cryostat",
    "tunnel",
    "CryoCore",
    "Rook",
    "XPCryostation",
    "Fsr",
    "TcPlot",
    "mirs_helpers",
]