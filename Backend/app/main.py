from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import text_endpoint
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
app.include_router(text_endpoint.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=AppConfig.app_port)
