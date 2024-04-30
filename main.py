import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing board configurations, typically for initializing and managing hardware interfaces or other setups
from configs.board import board
# Importing a module to load environment variables which typically hold settings necessary for the application configuration
from configs.environment import get_environment_variables
# Import routes that define the HTTP endpoints of the application
from api import routes

# Load environment variables from the configured source
env = get_environment_variables()

# Initialize FastAPI app with metadata from environment variables
app = FastAPI(
    title=env.APP_NAME,  # Title of the application, as a string
    version=env.API_VERSION,  # Version of the API, as a string
)

# Set up Cross-Origin Resource Sharing (CORS) middleware
# This configuration allows the API to handle requests from different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from all origins
    allow_credentials=True,  # Allows cookies and other credentials
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


# Event handler for application startup
@app.on_event("startup")
async def startup():
    """
    Performs application initialization tasks:
    - Sets up the board session and starts data streaming
    - Ensures a static directory is available for storing files
    """
    # Prepare the session for board operations, like connecting or configuring hardware
    board.prepare_session()
    # Start streaming data from the board, if applicable (e.g., sensor data, video feeds)
    board.start_stream()

    # Ensure the existence of a directory to store static files
    directory_name = "./static"
    os.makedirs(directory_name, exist_ok=True)


# Event handler for application shutdown
@app.on_event("shutdown")
async def shutdown():
    """
    Clean-up tasks when application is shutting down:
    - Stops data streaming and releases board resources
    """
    # Stop streaming data from the board
    board.stop_stream()
    # Release any sessions or resources held by the board
    board.release_session()


# Include the routes from the routes module into the FastAPI application
# This step is crucial to make the defined endpoints accessible
app.include_router(routes)
