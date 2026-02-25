# Infrared Brain Signal Scattering: A Monte Carlo Statistical Analysis

###### This project simulates the scattering of infrared signals through inhomogeneous, multi-layered brain structures using Monte Carlo methods. Originally developed as a Master’s diploma project, it has been refactored into a modular Python application to demonstrate expertise in stochastic modeling, statistical hypothesis testing, and interactive data visualization.


## Project Overview

###### The goal is to analyze how light photons behave as they pass through various layers of the human head (e.g., scalp, skull, CSF, and brain tissue). Since direct measurement is invasive and complex, this project uses a simulation-first approach to generate synthetic data and validate its statistical distribution.



https://github.com/user-attachments/assets/bc09a049-0c5a-44c1-b319-4ea5f41c84c3



### Core Objectives:
* **Modeling:** Constructing simplified one-, two-, and three-layer models to approximate and validate parameters for a complex four-layer brain model.
* **Simulation:** Implementing a Monte Carlo algorithm to track photon paths and scattering events.
* **Statistical Validation:** Applying the Pearson chi-squared test and Gaussian distribution fitting to analyze the resulting signal intensity data.

## Tech Stack
* **Language:** Python 3.x
* **Interface:** Streamlit (Web-based Dashboard)
* **Numerical Computing:** NumPy, SciPy
* **Data Visualization:** Matplotlib, Plotly
* **Software Architecture:** Object-Oriented Programming (OOP)

## System Architecture
| Module  | Class | Responsibility |
| ------- |:-----:| -------------- 
| layers_manager.py | LayersManager |Defines physical properties (refractive index, absorption/scattering coefficients) for the multi-layer model. |
| monte_carlo_simulation.py | SimulationMonteCarlo | Handles the stochastic logic of photon movement, boundary interactions, and energy deposition. |
| statistic.py | StatisticalAnalyzer | Processes simulation output; calculates Mean, Dispersion, and performs Pearson’s Goodness-of-Fit tests. |
| main.py | Main | The entry point that orchestrates the simulation and renders the Streamlit UI. |

## Methodology & Statistical Analysis
1. **The Monte Carlo Method**<br>
The simulation tracks thousands of individual "photons." At each step, a random number generator determines:
    * The distance the photon travels.
    * The angle of scattering (Henyey-Greenstein phase function).
    * Whether the photon is absorbed, reflected, or transmitted at layer boundaries.

2. **Statistical Testing**<br>
Once the simulation concludes, the resulting dataset of scattering intensities is analyzed:
    * _**Descriptive Statistics:**_ Calculation of the Mean and Dispersion (Variance) to characterize signal stability.
    * __**Distribution Fitting:**_ We test the hypothesis that the scattered signal follows a Gaussian (Normal) distribution, which is critical for signal processing applications.
    * _**Pearson Test:**_ A chi-squared test is used to determine the "Goodness of Fit," providing a p-value to accept or reject the distribution hypothesis.

## How to Run
1. Clone the repository:
```
git clone https://github.com/KanOlha/monte-carlo-brain-scattering.git
cd monte-carlo-brain-scattering
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Launch the Dashboard:
```
streamlit run app.py
```

## Key Results
* **Interactive Controls:** Users can adjust the thickness and scattering coefficients of individual brain layers in real-time.
* **Visual Feedback:** Real-time generation of histograms and probability density functions (PDF) for the scattered signal.
* **Model Comparison:** Data demonstrates how a simplified 3-layer model can effectively approximate the statistical mean of a full 4-layer structure under specific conditions.

## ⚖️ License
This project is part of a Master's Thesis at LVIV POLYTECHNIC NATIONAL UNIVERSITY. All rights are reserved. 
For inquiries regarding the use of this simulation logic, please contact Olha Kanikovska.

_!This project is for educational and simulation purposes only. It is not intended for clinical use or medical diagnosis._
