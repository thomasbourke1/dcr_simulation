# SPAD Simulation: SPDE & DCR Reproduction

A repository for reproducing simulation results from Kang et al., ‘Dark Count Probability and Quantum Efficiency of Avalanche Photodiodes for Single-Photon Detection’.

## Overview
This is a model to calculate the dark count rate (DCR) and single-photon detection efficiency (SPDE) for a gated SPAD. In this operation, the SPAD is periodically biased above and below it's breakdown voltage $V_B$. The key free parameters of the model are the primary dark current $I_{DM}$ and the avalanche breakdown probability $P_a$, which can be calculated from the McIntyre model [2].

## Method

In Geiger mode, the SPAD is periodically biased above and below breakdown with a short voltage pulse. A detection event occurs when a carrier — either
photon-generated or thermally generated — triggers an avalanche during the gate. This model assumes four independent sources fo such carriers:

1. **Primary dark carriers** generated inside the multiplication region during the gate pulse
2. **Pre-pulse dark carriers** generated before the pulse and amplified by the DC gain
3. **Afterpulse carriers (type 1)** released from traps during the gate pulse
4. **Afterpulse carriers (type 2)** released from traps before the gate pulse arrives

## Key equations

### Key Equations

**Primary dark carriers during gate pulse (Eq. 2):**
$$N_{DM1} = \frac{I_{DM} \tau}{q}$$

**Pre-pulse dark carriers amplified by DC gain (Eq. 3):**
$$N_{DM2} = \frac{I_{DM} M_0 \tau^*_{tr}}{q}, \qquad \tau^*_{tr} = \frac{M_0}{2\pi \cdot GB}$$

**Afterpulse carriers released during gate pulse (Eq. 4):**
$$N_{t1} = P_d N_{tr} \frac{\exp(\tau/\tau_d) - 1}{\exp(\Delta T/\tau_d) - 1}$$

**Afterpulse carriers released before gate pulse (Eq. 5):**
$$N_{t2} = P_d N_{tr} \frac{\exp(\tau^*_{tr}/\tau_d) - 1}{\exp(\Delta T/\tau_d) - 1}$$

where the average number of trapped carriers per pulse is:
$$N_{tr} = \frac{c M_g}{1 - c}$$

**Total dark carriers per pulse (Eq. 6):**
$$N_d = N_{DM1} + N_{DM2} + N_{t1} + N_{t2}$$

**Dark count probability — solved self-consistently (Eq. 7):**
$$P_d = 1 - \exp\!\left(-P_a \left[\frac{I_{DM}\tau}{q} + \frac{I_{DM}M_0^2}{2\pi q \cdot GB} + P_d N_{tr}\frac{\exp(\tau/\tau_d)-1}{\exp(\Delta T/\tau_d)-1} + P_d N_{tr}\frac{\exp(\tau^*_{tr}/\tau_d)-1}{\exp(\Delta T/\tau_d)-1}\right]\right)$$

**Single-photon detection efficiency (Eq. 8):**
$$\text{SPDE} = \frac{P_{on} - P_d}{P_{ph}}, \qquad P_{ph} = 1 - e^{-N_0}$$

**$P_{on}$ with optical input — solved self-consistently (Eq. 11):**
$$P_{on} = 1 - \exp\!\left(-P_a \left[N_{DM1} + N_{DM2} + P_{on} N_{tr}\frac{\exp(\tau/\tau_d)-1}{\exp(\Delta T/\tau_d)-1} + P_{on} N_{tr}\frac{\exp(\tau^*_{tr}/\tau_d)-1}{\exp(\Delta T/\tau_d)-1} + \eta N_0\right]\right)$$

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