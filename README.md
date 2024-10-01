# python-strompris-api

## Setup
### Virtual Environment
It's recommended to work within a Python virtual environment to isolate your project's dependencies. To activate the virtual environment, use the following command:
- On Windows: 
  ```shell
  .\venv\Scripts\activate
  ```
- On macOS/Linux: 
  ```shell
  source venv/bin/activate
  ```

### Installing Dependencies
Once your environment is active, you can install all required libraries using the provided requirements.txt file:
```shell
pip install -r requirements.txt
```

### Setup environment variables
- Create .env file from .env.example.
- Add variables in .env.
    ```
    CLIENT_ID=clientId
    CLIENT_SECRET=clientSecret
    ```

## Running Test
To start test, run the following command:
```shell
pytest
```