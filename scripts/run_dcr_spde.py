from dcr_simulation.dcr import DCR_SPDE

sim = DCR_SPDE()

# sim.run_pipeline(savePath='results/figures/dcr_spde_I_DM.png',
#                  inVar=[0.1e-12, 1e-12, 10e-12], # Plot multiple primary dark currents
#                  inVarName='I_DM')

sim.run_pipeline(savePath='results/figures/dcr_spde_M_0.png',
                 inVar=[30, 20, 10], # Plot multiple M_0 - average DC gain
                 inVarName='M_0',
                 upper_xlim=40)