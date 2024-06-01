# Analyzing Relaxation Sessions with BrainFlow and OpenBCI Cyton

## Introduction

This project aims to provide a comprehensive framework for analyzing relaxation sessions using EEG data collected with the OpenBCI Cyton board, utilizing the BrainFlow library for data acquisition, processing, and analysis. Our goal is to unlock insights into the physiological markers of relaxation, contributing to the fields of neurofeedback, meditation research, and personal well-being.

## Features

- **Real-time EEG Data Acquisition:** Utilizes BrainFlow's integration with the OpenBCI Cyton board to collect EEG data in real-time.
- **Data Analysis Pipeline:** A step-by-step analysis pipeline, from preprocessing to feature extraction, focusing on indicators of relaxation.
- **Visualization Tools:** Tools for visualizing EEG signals and analysis results, aiding in the interpretation of relaxation states.
- **Customizable Session Parameters:** Allows for customization of session parameters to cater to different research needs and objectives.
- **Exportable Results:** Capability to export session results for further analysis or sharing with research communities.

## Installation

### Prerequisites

- Python 3.11
- OpenBCI Cyton Board

### Setup

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/armmosikyan66/EEG-Mental-State-Monitoring
   ```
2. Create virtual env and Install the required Python packages
   ```
   make init
   ```

## Getting Started

To begin analyzing relaxation sessions:

1. Ensure your OpenBCI Cyton board is properly set up and connected.
2. Run the main analysis script:
   ```
   make start
   ```
3. Follow the on-screen prompts to configure your session parameters.


This command initiates the project, starting data acquisition and analysis.

## Cleaning Up

To clean up the project directory (e.g., remove virtual environment and temporary files), run:

```
make clean
```
## Data Analysis

This project applies various signal processing techniques to analyze the EEG data:

- **Preprocessing:** Filters the raw EEG data to remove noise and artifacts.
- **Feature Extraction:** Identifies features correlated with relaxation, such as specific frequency bands.
- **Statistical Analysis:** Compares relaxation metrics across sessions to assess effectiveness.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
