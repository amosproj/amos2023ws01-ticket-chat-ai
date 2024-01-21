from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import ticket_api
from app.dependency.collection import (
    get_user_collection,
    get_service_collection,
    get_category_collection,
    get_valid_category_collection,
    get_location_collection,
)
from app.dependency.repository import (
    get_user_repository,
    get_service_repository,
    get_category_repository,
    get_valid_category_repository,
    get_location_repository,
)
from app.repository.user_repository import UserRepository
from app.repository.service_repository import ServiceRepository
from app.repository.location_repository import LocationRepository
from app.repository.category_repository import CategoryRepository
from app.repository.valid_category_repository import ValidCategoryRepository
from app.service.category_db_routine_service import CategoryDBRoutineService
from app.service.valid_category_db_routine_service import ValidCategoryDBRoutineService
from app.service.location_db_routine_service import LocationDBRoutineService
from app.service.user_db_routine_service import UserDBRoutineService
from app.service.service_entity_db_routine_service import ServiceDBRoutineService

from config import AppConfig

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:9876",  # frontend test port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the router from the text_endpoint module
app.include_router(ticket_api.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    user_collection = get_user_collection()
    user_repo_service: UserRepository = get_user_repository(user_collection)
    user_db_routine_service = UserDBRoutineService(user_repo_service)
    user_db_routine_service.start_routine()

    service_collection = get_service_collection()
    service_repo_service: ServiceRepository = get_service_repository(service_collection)
    service_entity_db_routine_service = ServiceDBRoutineService(service_repo_service)
    service_entity_db_routine_service.start_routine()

    location_collection = get_location_collection()
    location_repo_service: LocationRepository = get_location_repository(
        location_collection
    )
    location_db_routine_service = LocationDBRoutineService(location_repo_service)
    location_db_routine_service.start_routine()

    category_collection = get_category_collection()
    category_repo_service: CategoryRepository = get_category_repository(
        category_collection
    )
    category_db_routine_service = CategoryDBRoutineService(category_repo_service)
    category_db_routine_service.start_routine()

    valid_category_collection = get_valid_category_collection()
    valid_category_repo_service: ValidCategoryRepository = get_valid_category_repository(
        valid_category_collection
    )
    valid_category_db_routine_service = ValidCategoryDBRoutineService(
        valid_category_repo_service
    )
    valid_category_db_routine_service.start_routine()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=AppConfig.app_port)
