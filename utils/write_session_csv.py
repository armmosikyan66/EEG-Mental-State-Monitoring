from brainflow.data_filter import DataFilter


def write_session_csv(data, output_path):
    DataFilter.write_file(data, output_path, 'w')
