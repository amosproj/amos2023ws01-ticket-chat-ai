# Backend

## Project Structure

    amos2023ws01-ticket-chat-ai/
    Backend
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

1. **Install Python**: go to [python.org](https://wiki.python.org/moin/BeginnersGuide/Download)

2. **Install MongoDB Community Server**: go
   to [mongodb.com](https://www.mongodb.com/docs/manual/administration/install-community/)

3. **Navigate to Backend**:

    ```bash
    cd amos2023ws01-ticket-chat-ai/Backend
    ```

4. **Create and Activate a Virtual Environment** (Optional but recommended):

    ```bash
    python3 -m venv venv
    ```
   In a Unix-based System run:
    ```bash
    source venv/bin/activate
    ```
   In Windows run:
   ```bash
   venv\Scripts\activate
   ```

5. **Install the Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment Variables for the EmailProxy:**

    Navigate into `./backend` directory.
    Rename .env_example to .env and set your Email Password inside the .env

## Running and Testing the Project

1. **Start the backend**:

    ```bash
    uvicorn app.main:app --reload
    ```

2. **Use the endpoints**: go to [SwaggerUI](http://localhost:8000/docs) **OR**
   try [Postman](https://www.postman.com/downloads/) with the base URL `http://localhost:8000/api/v1` + router path

   - Example of how to test endpoint with postman (Model is automatically run when we run the endpoint). 
      ![Example of how to test endpoint with postman](images/endpoint_example.png)
3. **Run the tests**:

    ```bash
    pytest test/
    ```

## Run Test Model

1. Navigate into `./backend/app/models/t5` directory.

2. Train the model by running the following command:

   ```bash
   python train_t5_model.py
   ```

3. Test the trained model by running the following command:

   ```bash
   python use_trained_t5_model.py
   ```

4. Test the untrained T5 model by running the following command:

   ```bash
   python train_t5_model.py
   ```

## Useful Tools

- IDE: VS Code, PyCharm
- MongoDB: MongoDB Compass