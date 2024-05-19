# Importing APIRouter from the fastapi package to create and manage different API routes
from fastapi import APIRouter

# Importing specific routers for the relaxation and concentration functionalities
# These routers are defined in their respective modules within the 'api.v1' package
from api.v1.relaxation import relaxation
from api.v1.concentration import concentration

# Creating an instance of APIRouter, which serves as the root router for the application
# The prefix '/api/v1' is set to all routes that will be included in this router
# This helps in organizing the API versioning and managing all v1 APIs from a central router
routes = APIRouter(prefix="/api/v1")

# Including the relaxation router under the root API router
# This router will handle all requests related to relaxation features
routes.include_router(relaxation)

# Including the concentration router under the root API router
# This router will manage all requests related to concentration features
routes.include_router(concentration)
