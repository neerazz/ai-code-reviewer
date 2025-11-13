# Backend

This directory contains the FastAPI backend for the AI-Powered Code Review & Migration Assistant.

## Structure

The backend is structured as follows:

-   `api/`: The API endpoints.
    -   `routers/`: The API routers.
    -   `schemas/`: The Pydantic schemas.
-   `Dockerfile`: The Dockerfile for building the backend image.
-   `requirements.txt`: The Python dependencies.

## Running Locally

To run the backend locally, you will need to have Python 3.9+ and `pip` installed.

1.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the server:**

    ```bash
    uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
    ```

The `--reload` flag will automatically reload the server when you make changes to the code.
