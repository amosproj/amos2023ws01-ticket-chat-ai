from fastapi import FastAPI
from config import AppConfig  # Import the AppConfig class from the configuration file
from app.api.v1 import text_endpoint

app = FastAPI()

# Include the router from the text_endpoint module
app.include_router(text_endpoint.router, prefix="/api/v1")

if __name__ == "__main__":
   import uvicorn

   uvicorn.run(app, host="0.0.0.0", port=AppConfig.app_port)  # Use the configured port from the AppConfig class
