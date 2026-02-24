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

    
    
class DCR_SPDE:
    """Plots DCR vs SPDE

    __init__() initializes some default parameters to plot. The user can also input their own parameters via
    """
    
    def __init__(self):
        
        #Physical constants
        self.ELECTRONIC_CHARGE = 1.602e-19 # Electronic charge [C]
        
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
    
    
    def compute_DCR_SPDE(self):
        
        
        factor_Nt1, factor_Nt2 = self.compute_initial_params()
        
        Pa_values = np.linspace(1e-4, 0.99, 2000) # Breakdown probability - the free parameter (can also be calculated from McIntyre model)
        
        
        N_DM1 = self.I_DM * self.tau / self.ELECTRONIC_CHARGE # Primary dark carriers during pulse - Eq. 2
        N_DM2 = self.I_DM * self.M_0 * self.tau_tr / self.ELECTRONIC_CHARGE # Dark carriers generated before pulse - Eq. 3
        
        Pd_vals = [] # To be calculated
        SPDE_vals = [] # To be calculated
        
        for Pa in Pa_values:
            # Solve Eq. 7 self consistiently for P_d
            def equation(Pd):
                Nd = (N_DM1 + N_DM2
                      + Pd * self.N_tr * factor_Nt1
                      + Pd * self.N_tr * factor_Nt2)
                return Pd - (1 - np.exp(-Nd * Pa))
            
            Pd_sol = fsolve(equation, x0=N_DM1 * Pa, full_output=False)[0]
            Pd_sol = float(np.clip(Pd_sol, 0, 1))
        
            eta = Pa # Conventional quantum efficiency of detector
            
            def equation_on(Pon):
                """Calculate probability of a current pulse triggered by a light or dark carrier when the single photon source is on. Needed to calculate SPDE

                Args:
                    Pon (_type_): Described above

                Returns:
                    _type_: _description_
                """
                Nd_on = (N_DM1 + N_DM2
                     + Pon * self.N_tr * factor_Nt1
                     + Pon * self.N_tr * factor_Nt2
                     + Pa * self.N_0)           # eta*N0 term -> Light counts per pulse
                return Pon - (1 - np.exp(-Nd_on * Pa))
            
                
            Pon_sol = fsolve(equation_on, x0=(N_DM1 + Pa * self.N_0) * Pa,
                        full_output=False)[0]
            Pon_sol = float(np.clip(Pon_sol, 0, 1))

            # SPQE = (P_on - P_d) / P_ph   [Eq. 8]
            SPQE = (Pon_sol - Pd_sol) / self.P_ph

            Pd_vals.append(Pd_sol*self.f) # times by f for DCR (currently dark count probability per pulse)
            SPDE_vals.append(SPQE * 100)   # convert to %
        
            # print(Pd_vals, SPDE_vals)
        
        return Pd_vals, SPDE_vals
    
    
    def plot(self, Pd_vals, SPDE_vals, savePath=None) -> None:
    
    
        fig, ax = plt.subplots(figsize=(7, 6))
        
        
        
        ax.semilogy(SPDE_vals, Pd_vals, lw=2, label=None)
        
        ax.set_xlabel('Single-photon detection efficiency (%)', fontsize=13)
        ax.set_ylabel('Dark Count Rate (Hz)', fontsize=13)
        # ax.set_title('Fig. 1 — Kang et al. APL 83, 2955 (2003)\n'
        #             r'$f$=100 kHz, $\tau$=2 ns, $\tau_d$=200 ns, '
        #             r'$c$=1%, $N_0$=0.3, $M_g$=10$^8$, GB=30 GHz',
        #             fontsize=10)
        ax.legend(fontsize=9)
        # ax.set_xlim([0, 40])
        # ax.set_ylim([1e-7, 1e0])
        ax.grid(True, which='both', alpha=0.3)

        plt.tight_layout()
        # plt.savefig('results/figures/dcr_spde.png', dpi=150)
        
        if savePath:
            plt.savefig(savePath, dpi=150)
            
        
        plt.show()
    
    
    def run_pipeline(self, savePath=None):
        
        self.compute_initial_params()
        
        DCR_vals, SPDE_vals = self.compute_DCR_SPDE()
        
        self.plot(DCR_vals, SPDE_vals, savePath)
        