from fastapi import FastAPI
from config import AppConfig
from app.api.v1 import text_endpoint
from fastapi.middleware.cors import CORSMiddleware
from app.email import email_proxy_service

app = FastAPI()

origins = [
    "http://localhost:4200",  # Remove the trailing slash
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the router from the text_endpoint module
app.include_router(text_endpoint.router, prefix="/api/v1")


@app.on_event("startup")
def start_email_proxy():
    email_proxy_service.run_proxy()



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=AppConfig.app_port)

