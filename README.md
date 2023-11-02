# Ticket-Chat-AI Project (AMOS WS 2023)

# Backend

## Project Structure

    amos2023ws01-ticket-chat-ai/
    bakcned
    │
    └── app
        ├── api                     
        │      └── v1
        │          └── text_endpoint.py
        │
        |
        ├── main.py
        │
        │
        └── requirements.txt


## Setup

1. **Clone the Repository**:

   ```bash
   git clone git@github.com:amosproj/amos2023ws01-ticket-chat-ai.git
   cd amos2023ws01-ticket-chat-ai/backend

2. **Create a Virtual Environment** (Optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. **Install the Dependencies:**

    ```bash
    pip install -r requirements.txt

## Running the Project

    uvicorn app.main:app --reload
