# It imports necessary modules from the brainflow library

from brainflow.data_filter import DataFilter

# Function to write EEG session data to a CSV file
def write_session_csv(data, output_path):
    # Write the data to the specified output path in 'w' (write) mode
    DataFilter.write_file(data, output_path, 'w')
