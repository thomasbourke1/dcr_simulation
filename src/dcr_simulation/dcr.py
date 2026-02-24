"""
Contains functions to calculate the DCR of a SPAD

Features:
- 
"""

#Standard library imports

#Third party imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

#Local application imports

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

    
    
class DCR_SPDE():
    """Plots DCR vs SPDE

    __init__() initializes some default parameters to plot. The user can also input their own parameters via
    """
    
    def __init__(self, params='default'):
        """Initializes params. Should also be able to setup parameters from user input
        """

        #Physical constants
        self.ELECTRONIC_CHARGE = 1.602e-19 # Electronic charge [C]
        
        if params == 'default':
            # Experimental parameters - calibrated or set by experimentalist
            self.f = 100e3 # Pulse repetition rate [Hz]
            self.tau = 2e-9 # Gate pulse width [s]
            self.tau_d = 200e-9 # Detrap time constant [s]
            self.N_0 = 0.1 # Mean photons per pulse
            self.delta_T = 1 / self.f # Reciprocal of pulse repetiion rate 1GHz = 1ns [s]

            # Physical parameters of SPAD / APD
            self.M_0 = 10 # DC Avalanche gain
            self.M_g = 1e8 # Geiger mode gain
            self.GB = 30e9 # Gain bandwidth product [Hz]
            self.c= 0.01 # Trapping ratio [1%]
            
            # Effective free parameters -> Have physical origin but can be set by user
            
            self.P_a = 0.1 # Avalanche probability (could also find from McIntyre model) -> Free parameter in Fig. 1
            self.I_DM = 1e-12 # Primary dark current -> Defaults to 1pA, can be set as series [A]
        
        

    def compute_initial_params(self):
        """Computes parameters from parameters inputted via __init__()

        Returns:
            factor_Nt1, factor_Nt2 _type_: Fractions in Eq. 4 and 5
        """
        
        self.tau_tr = self.M_0 / (2 * np.pi * self.GB) # Effective transit time of carriers 
        
        # Afterpulsing parameters
        self.N_tr = self.c * self.M_g / (1-self.c) # Average number of carriers trapped after a current pulse. Just above Eq. 4 in paper.
        
        # Afterpulse exponential factors in Eq. 4 and 5.
        exp_tau_tau_d = np.exp(self.tau / self.tau_d)
        exp_DT_tau_d = np.exp(self.delta_T / self.tau_d)
        exp_tau_tr_tau_d = np.exp(self.tau_tr / self.tau_d)
        
        factor_Nt1 = (exp_tau_tau_d - 1) / (exp_DT_tau_d - 1) # Eq. (4) factor
        factor_Nt2 = (exp_tau_tr_tau_d - 1) / (exp_DT_tau_d - 1) # Eq. (5) factor
        
        # Photons
        self.P_ph = 1- np.exp(-self.N_0) # Probability that pulse contains at least one photon
    
        return factor_Nt1, factor_Nt2
    
    def compute_DCR_SPDE(self, inVar=None, inVarName=None):
        """
        Compute DCR and SPDE, optionally iterating over multiple values of a parameter.

        Args:
            inVar: Single value or list of values for the parameter to iterate over.
                If None, uses the instance attribute as-is.
            inVarName: String name of the instance attribute to vary (e.g. 'I_DM').
                    If None, no parameter is varied.

        Returns:
            List of (Pd_vals, SPDE_vals) tuples, one per inVar value.
            If inVar is None, returns a single-element list.
        """

        # Normalise inputs so we always iterate over a list
        if inVar is not None:
            if not isinstance(inVar, (list, np.ndarray)):
                inVar = [inVar]
        else:
            inVar = [None]  # Single run with current instance attributes

        results = []  # List of (Pd_vals, SPDE_vals) per inVar value

        for var in inVar:

            # Temporarily override the instance attribute if a var is provided
            if var is not None and inVarName is not None:
                original_val = getattr(self, inVarName)
                setattr(self, inVarName, var)
                self.compute_initial_params()  # Recompute dependent params

            factor_Nt1, factor_Nt2 = self.compute_initial_params()

            Pa_values = np.linspace(1e-4, 0.99, 2000)

            N_DM1 = self.I_DM * self.tau / self.ELECTRONIC_CHARGE
            N_DM2 = self.I_DM * self.M_0 * self.tau_tr / self.ELECTRONIC_CHARGE

            Pd_vals = []
            SPDE_vals = []

            for Pa in Pa_values:

                def equation(Pd):
                    Nd = (N_DM1 + N_DM2
                        + Pd * self.N_tr * factor_Nt1
                        + Pd * self.N_tr * factor_Nt2)
                    return Pd - (1 - np.exp(-Nd * Pa))

                Pd_sol = fsolve(equation, x0=N_DM1 * Pa, full_output=False)[0]
                Pd_sol = float(np.clip(Pd_sol, 0, 1))

                def equation_on(Pon):
                    Nd_on = (N_DM1 + N_DM2
                            + Pon * self.N_tr * factor_Nt1
                            + Pon * self.N_tr * factor_Nt2
                            + Pa * self.N_0)
                    return Pon - (1 - np.exp(-Nd_on * Pa))

                Pon_sol = fsolve(equation_on, x0=(N_DM1 + Pa * self.N_0) * Pa,
                                full_output=False)[0]
                Pon_sol = float(np.clip(Pon_sol, 0, 1))

                SPQE = (Pon_sol - Pd_sol) / self.P_ph

                Pd_vals.append(Pd_sol * self.f)
                SPDE_vals.append(SPQE * 100)

            results.append((Pd_vals, SPDE_vals))

            # Restore original attribute value
            if var is not None and inVarName is not None:
                setattr(self, inVarName, original_val)

        return results


    def plot(self, results, inVar=None, inVarName=None, savePath=None, upper_xlim: float=None) -> None:

        fig, ax = plt.subplots(figsize=(7, 6))

        for i, (Pd_vals, SPDE_vals) in enumerate(results):

            # Build a readable label
            if inVar is not None and inVarName is not None:
                val = inVar[i] if isinstance(inVar, (list, np.ndarray)) else inVar
                label = f'{inVarName} = {val:.2e}'
            else:
                label = 'Simulation'

            ax.semilogy(SPDE_vals, Pd_vals, lw=2, label=label)

        ax.set_xlabel('Single-photon detection efficiency (%)', fontsize=13)
        ax.set_ylabel('Dark Count Rate (Hz)', fontsize=13)

        if upper_xlim:
            ax.set_xlim(0,upper_xlim)

        ax.legend(fontsize=9)
        ax.grid(True, which='both', alpha=0.3)
        plt.tight_layout()

        if savePath:
            plt.savefig(savePath, dpi=150)

        plt.show()


    def run_pipeline(self, inVar=None, inVarName=None, savePath=None, upper_xlim=None):

        self.compute_initial_params()

        results = self.compute_DCR_SPDE(inVar=inVar, inVarName=inVarName)

        self.plot(results, inVar=inVar, inVarName=inVarName, savePath=savePath, upper_xlim=upper_xlim)