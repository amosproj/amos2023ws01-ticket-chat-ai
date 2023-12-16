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

6. **Set environment Variables for the EmailProxy:**

   Navigate into `./backend` directory. Rename .env_example to .env and set your Email Password inside the .env

7. **Initialise and starting .exe (only tested for windows right now)**

   `start_only.py` starts Backend, Frontend, Proxy and MongoDB. (MongoDB has to be installed on the standard path).

   `start.oy` starts Backend, Frontend, Proxy and MongoDB and installs all dependencies for frontend and backend. (MongoDB has to be installed on the standard path).

   Navigate into `./backend` directory. 

   In Windows run:

   When everything is setted up and only .exe is needed.

   ```bash
   pyinstaller --hidden-import uvicorn --onefile start_only.py
   ```

   For the first time, when no dependencies have been installed, and only Python, Node.js, and MongoDB have been installed:

   ```bash
   pyinstaller --hidden-import uvicorn --onefile start.py
   ```

   After that, 3 things will be created:
      
      backend/start.spec   (dont track it, keep it local)
      backend/build        (dont track it, keep it local)
      backend/dist         (dont track it, keep it local)
   
   In the dist folder, there is a file `start.exe`. Drag it into the root level, where the backend and frontend folders are. You can then execute the file there.

## Running and Testing the Project

1. **Start Database**:
    - Mac:
       ```bash
       brew services start mongodb-community@7.0
       ```
    - Windows:
      ```bash
      elevate -w net start MongoDB
      ```
      Alternative:
      1. Add the path to `mongod.exe` to the environment variables in order to use it globally.
      2. Create a storage directory at any location, for example, `...\data\db`, if you have not already done so.
      3. Run `mongod` with path to storage location for example:
         ```bash
         mongod --dbpath E:\workspace\Uni\ws23-24\AMOS\data\db
         ```
    - Linux:
      ```bash
      sudo systemctl start mongod
      ```

2. **Start the Backend API**:

    ```bash
    uvicorn app.main:app --reload
    ```

3. **Use the endpoints**: go to [SwaggerUI](http://localhost:8000/docs) **OR**
   try [Postman](https://www.postman.com/downloads/) with the base URL `http://localhost:8000/api/v1` + router path

    - Example of how to test endpoint with postman (Model is automatically run when we run the endpoint).
      ![Example of how to test endpoint with postman](images/endpoint_example.png)
4. **Run the tests**:

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

## Run the Email Proxy

1. Start Backend API
2. Navigate to `app/email` and run:
   ```bash
    python main.py
   ```

## Useful Tools

- IDE: VS Code, PyCharm
- MongoDB: MongoDB Compass