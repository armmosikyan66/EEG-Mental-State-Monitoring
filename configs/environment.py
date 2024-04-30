# Import necessary modules and decorators.
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from a .env file into the program's environment.
load_dotenv()


class EnvironmentSettings(BaseSettings):
    """
    A Pydantic model that defines and validates the types of environment variables required by the application.
    These settings are loaded from the environment and automatically validated against the specified types.
    """
    API_VERSION: str  # Expected to be a string defining the API version.
    APP_NAME: str  # Expected to be a string defining the application name.
    PORT: int  # Expected to be an integer defining the port on which the application will run.
    DEBUG_MODE: bool  # Expected to be a boolean indicating if the application is in debug mode.
    HOST: str  # Expected to be a string defining the host for the application.
    LOG_LEVEL: str  # Expected to be a string defining the log level of the application (e.g., DEBUG, INFO).
    BOARD_ID: str  # Expected to be a string identifying the specific hardware board to be used.


@lru_cache
def get_environment_variables():
    """
    Returns an instance of the EnvironmentSettings with values loaded from the environment.
    This function uses LRU caching to ensure that the settings are loaded and validated only once,
    thereby improving performance by avoiding redundant validations on each call.

    Returns:
        EnvironmentSettings: The validated configuration settings from environment variables.
    """
    return EnvironmentSettings()
