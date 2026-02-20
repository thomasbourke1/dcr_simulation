"""
Contains functions to calculate the DCR of a SPAD

Features:
- 
"""

#Standard library imports

#Third party imports

#Local application imports
from dcr_simulation.constants import ELECTRON_CHARGE

# -----------------------------


def N_DM1(tau_gate_pulse_width: float, I_DM_primary_dark_current: float):
    """Calculate the primary dark carriers injected or generated in the multiplication region during a SPAD gate

    Args:
        tau_gate_pulse_width (float): Gate pulse width / Hz
        I_DM_primary_dark_current (_type_): Primary dark current / A

    Returns:
        _type_: N_DM1
    """
    N_DM1 = I_DM_primary_dark_current * tau_gate_pulse_width / ELECTRON_CHARGE
    return N_DM1

