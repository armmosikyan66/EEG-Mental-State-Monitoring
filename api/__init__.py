from fastapi import APIRouter

from api.v1.relaxation import relaxation
from api.v1.concentration import concentration

routes = APIRouter(prefix="/api/v1")

routes.include_router(relaxation)
routes.include_router(concentration)
