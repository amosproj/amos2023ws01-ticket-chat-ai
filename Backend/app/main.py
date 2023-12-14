from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import ticket_api
from app.dependency.collection import get_user_collection
from app.dependency.repository import get_user_repository
from app.repository.user_repository import UserRepository
from app.service.user_db_routine_service import UserDBRoutineService
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

print("starting routine")
collection = get_user_collection()
user_repo_service: UserRepository = get_user_repository(collection)
user_db_routine_service = UserDBRoutineService(user_repo_service)
user_db_routine_service.start_routine()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=AppConfig.app_port)
