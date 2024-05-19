# Import the necessary components from FastAPI to establish API routes and manage WebSocket communications.
from fastapi import APIRouter, WebSocket, Depends

# Import the ConcentrationService which is responsible for the business logic associated with concentration tracking.
from services.concentration_service import ConcentrationService

# Instantiate APIRouter which is utilized to define and organize API routes in the application.
concentration = APIRouter()

@concentration.websocket("/concentration")
async def websocket_endpoint(websocket: WebSocket, concentration_service: ConcentrationService = Depends()):
    """
    Asynchronous WebSocket endpoint to manage a concentration monitoring session.

    This endpoint serves as a communication hub for WebSocket connections that focus on tracking
    and managing user concentration. It leverages the ConcentrationService to handle the complex
    logic related to concentration states in real-time.

    Args:
        websocket (WebSocket): The WebSocket connection object provided by FastAPI, used to send and receive data.
        concentration_service (ConcentrationService): An instance of ConcentrationService handling the logic,
                                                      automatically injected by FastAPI using the Depends mechanism.

    The function’s main role is to maintain the WebSocket communication for concentration monitoring. Once a connection
    is established, it passes the responsibility to the ConcentrationService, which processes and manages the data
    received via WebSocket.
    """
    # The function call below handles the WebSocket data processing related to user concentration.
    await concentration_service.get_concentration(websocket)
