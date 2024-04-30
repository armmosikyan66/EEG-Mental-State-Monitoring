# Import necessary components from FastAPI to set up the API router and WebSocket communication.
from fastapi import APIRouter, WebSocket, Depends

# Import the RelaxationService which will handle relaxation-related logic over WebSocket.
from services.relaxation_service import RelaxationService

# Create an instance of APIRouter, which helps in declaring and managing different routes.
concentration = APIRouter()


@concentration.websocket("/relaxation")  # Define a new WebSocket route for relaxation-related interactions.
async def websocket_endpoint(websocket: WebSocket, relaxation_service: RelaxationService = Depends()):
    await relaxation_service.get_relaxation(websocket)
