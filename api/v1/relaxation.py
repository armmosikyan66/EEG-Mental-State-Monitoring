# Import necessary components from FastAPI to set up the API router and WebSocket communication.
from fastapi import APIRouter, WebSocket, Depends

# Import the RelaxationService which will handle relaxation-related logic over WebSocket.
from services.relaxation_service import RelaxationService

# Create an instance of APIRouter, which helps in declaring and managing different routes.
relaxation = APIRouter()


@relaxation.websocket("/relaxation")  # Define a new WebSocket route for relaxation-related interactions.
async def websocket_endpoint(websocket: WebSocket, relaxation_service: RelaxationService = Depends()):
    """
    Asynchronous WebSocket endpoint to manage a continuous relaxation monitoring session.

    This endpoint accepts WebSocket connections and uses the RelaxationService to handle
    the business logic required to track and respond to user relaxation states in real-time.

    Args:
        websocket (WebSocket): The WebSocket connection object provided by FastAPI.
        relaxation_service (RelaxationService): An instance of RelaxationService, injected by FastAPI's
                                                dependency injection system using the Depends function.

    The WebSocket endpoint `/relaxation` listens for connections and, once a connection is established,
    delegates the handling of the session to the RelaxationService.
    """
    # The function call below manages the entire process of receiving, processing, and responding over WebSocket.
    await relaxation_service.get_relaxation(websocket)
