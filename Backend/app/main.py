from fastapi import FastAPI
from api.v1 import text_endpoint

app = FastAPI()

# Include the router from the text_endpoint module
app.include_router(text_endpoint.router, prefix="/api/v1")
