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

   Navigate into `./backend` directory. Rename .env_example to .env and set your Email Password inside the .env

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
    - Only tests:
      ```bash
      pytest test/
      ```
    - Tests with code coverage:
      ```bash
      pytest --cov=app --cov-branch test/
      ```

## Run Test Model

### T5

1. Train the model by navigating to `./backend/app/models/train/text_generation_t5` and running the following command:

   ```bash
   python train.py
   ```

2. Test our trained model which is hosted on hugging face by navigating to `./backend/app/models/ai_ticket_service/t5` and running the following command:

   ```bash
   python use_trained_t5_model.py
   ```

3. Test the untrained T5 model by navigating to `./backend/app/models/ai_ticket_service/t5` and running the following command:

   ```bash
   python use_untrained_t5_model.py
   ```
   
### Text Classification (Roberta)
1. To train the model, you first need to navigate to the training script's directory:

   ```bash
   cd ./backend/app/models/train/text_classification
   ```
2. Prepare a JSON-formatted string for both your classes and data paths. For example, if you have three classes "Class1", "Class2", "Class3" and your data is located at "path/to/data1.json" and "path/to/data2.json", your JSON strings would look like:
 - Classes: '["Class1", "Class2", "Class3"]'
 - Data Paths: '["path/to/data1.json", "path/to/data2.json"]'

3. Run the training command with the necessary arguments. Here's an example command that includes arguments for classes, ticket field, and data paths:

   ```bash
   python train.py --batch_size 4 --epochs 4 --lr 2e-5 --no_cuda --save_model --classes '["Class1", "Class2", "Class3"]' --ticket_field "service" --data_paths '["path/to/data1.json", "path/to/data2.json"]'
   ```
 - `--batch_size`: The number of training samples to work through before the model's internal parameters are updated.
 - `--epochs`: The number of complete passes through the training dataset.
 - `--lr`: The learning rate used by the optimizer.
 - `--no_cuda`: Add this flag if you do not wish to use CUDA for training even if it's available.
 - `--save_model`: Add this flag if you wish to save the model after training.
 - `--classes`: The list of classes for the classifier in a JSON-formatted string.
 - `--ticket_field`: The field name for ticket classification.
 - `--data_paths`: The list of paths to your training data files in a JSON-formatted string.

## Run the Email Proxy

1. Start Backend API
2. Navigate to `app/email` and run:
   ```bash
    python main.py
   ```

## Format the code

[Black](https://black.readthedocs.io/en/stable/) is a Python code formatter that automatically formats your code.

- Format a single file:
  ```bash
  black your_file.py
  ```

- Format multiple files or a directory:
  ```bash
  black file1.py file2.py directory/
  ```

## Useful Tools

- IDE: VS Code, PyCharm
- MongoDB: MongoDB Compass