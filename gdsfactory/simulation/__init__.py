import sys
import warnings

try:
    import gplugins
except ImportError as e:
    msg = 'You need to install gplugins with "pip install gplugins"'
    raise ImportError(msg) from e


message = """
gdsfactory.simulation have been moved to gplugins

Make sure you have gplugins installed and use gplugins instead of gdsfactory.simulation

You can replace:
    import gdsfactory.simulation -> import gplugins

You can install gplugins with:
    pip install gplugins
"""

warnings.warn(message)
sys.modules["gdsfactory.simulation"] = gplugins
