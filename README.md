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

   ```

## Backend

**Create a Virtual Environment** (Optional but recommended):

- Navigate into `./backend` directory and run the following command.

   - Linux / macOs
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   - Windows
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

**Install the Dependencies:**

```bash
pip install -r requirements.txt
```

**Run Backend App**

    uvicorn app.main:app --reload

**Run Test Model**

1. Navigate into `./backend/app/models/t5` directory.

2. Train the model by running the following command:

   ```
   python train_t5_model.py
   ```

3. Test the trained model by running the following command:
   ```
   python use_trained_t5_model.py
   ```
4. Test the untrained T5 model by running the following command:
   ```
   python train_t5_model.py
   ```
