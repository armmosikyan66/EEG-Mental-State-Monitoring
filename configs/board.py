# Import required modules and decorators.
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

# Import custom configuration function for environment variables.
from configs.environment import get_environment_variables

# Retrieve and store environment variables for the application.
env = get_environment_variables()


def load_board() -> BoardShim:
    """
    Load and return a cached instance of the EEG board configuration. This function uses LRU caching to
    store the configuration and prevent unnecessary re-initializations, enhancing performance.

    Returns:
        BoardShim: The initialized board object.
    """
    params = BrainFlowInputParams()  # Create an instance of BrainFlowInputParams.
    params.serial_port = env.BOARD_ID  # Set the serial port for the EEG device connection.
    board = BoardShim(BoardIds.CYTON_BOARD, params)  # Initialize the BoardShim with the Cyton board type and parameters.

    return board  # Return the configured board instance.

board = load_board()