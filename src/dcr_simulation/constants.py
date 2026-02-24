"""
Contains physical constants and experimental parameters

Features:
- 
"""

#Standard library imports

#Third party imports

#Local application imports

# -----------------------------


# Physical constants
ELECTRON_CHARGE =   1.602e-19 # Coulombs

# Experimental parameters - calibrated or set by experimentalist
f = 100e3 # Pulse repetition rate
tau = 2e-9 # Gate pulse width [s]
tau_d = 200e-9 # Detrap time constant [s]
N_0 = 0.1 # Mean photons per pulse
delta_T = 1 / f # Reciprocal of pulse repetiion rate 1GHz = 1ns [s]

# Physical parameters of SPAD / APD
M_0 = 10 # DC Avalanche gain
M_g = 1e8 # Geiger mode gain
GB = 30e9 # Gain bandwidth product [Hz]
c= 0.01 # Trapping ratio [1%]
P_a = 0.1 # Avalanche probability (could also find from McIntyre model) -> Free parameter in Fig. 1