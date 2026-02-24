# SPAD Simulation: SPDE & DCR Reproduction

A repository for reproducing simulation results from Kang et al., ‘Dark Count Probability and Quantum Efficiency of Avalanche Photodiodes for Single-Photon Detection’.

## Overview
This is a model to calculate the dark count rate (DCR) and single-photon detection efficiency (SPDE) for a gated SPAD. In this operation, the SPAD is periodically biased above and below it's breakdown voltage $V_B$. The key free parameters of the model are the primary dark current $I_{DM}$ and the avalanche breakdown probability $P_a$, which can be calculated from the McIntyre model [2].

## Installation

```bash
# clone the repo
git clone https://github.com/thomasbourke1/dcr_simulation.git

# go into the project directory
cd dcr_simulation

# create a virtual environment to install dependencies
python -m venv venv

# activate virtual enviornment (Windows)
.\venv\Scripts\activate

# activate virtual environment (Mac / Linux)
source venv/bin/activate

# install project dependencies from pyproject.toml
pip install -e . 
```

## Usage

Run `run_dcr_spde.py` to generate DCR plotted against SPDE.

## References

[1] Kang, Y., H. X. Lu, Y. H. Lo, D. S. Bethune, and W. P. Risk. ‘Dark Count Probability and Quantum Efficiency of Avalanche Photodiodes for Single-Photon Detection’. Applied Physics Letters 83, no. 14 (2003): 2955–57. https://doi.org/10.1063/1.1616666.
[2] McIntyre, R. J. ‘On the Avalanche Initiation Probability of Avalanche Diodes above the Breakdown Voltage’. IEEE Transactions on Electron Devices 20, no. 7 (1973): 637–41. https://doi.org/10.1109/T-ED.1973.17715.