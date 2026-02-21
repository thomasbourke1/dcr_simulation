# SPAD Simulation: SPDE & DCR Reproduction

A repository for reproducing simulation results from Kang et al., ‘Dark Count Probability and Quantum Efficiency of Avalanche Photodiodes for Single-Photon Detection’.

## Overview

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

## References

[1] Kang, Y., H. X. Lu, Y. H. Lo, D. S. Bethune, and W. P. Risk. ‘Dark Count Probability and Quantum Efficiency of Avalanche Photodiodes for Single-Photon Detection’. Applied Physics Letters 83, no. 14 (2003): 2955–57. https://doi.org/10.1063/1.1616666.
