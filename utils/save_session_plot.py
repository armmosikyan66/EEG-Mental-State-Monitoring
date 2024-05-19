# It imports necessary modules from the matplotlib, numpy, and pandas libraries

import matplotlib
import numpy as np
import pandas as pd

# Use Agg backend for matplotlib (non-interactive mode, suitable for saving plots to files)
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Function to save a plot of EEG session data
def save_session_plot(data, eeg_channels, output_path):
    # Create a pandas DataFrame from the transposed EEG session data
    df = pd.DataFrame(np.transpose(data))

    # Create a new figure for the plot
    plt.figure()

    # Plot the EEG channels specified in eeg_channels on separate subplots
    df[eeg_channels].plot(subplots=True)

    # Save the plot to the specified output path
    plt.savefig(output_path)
