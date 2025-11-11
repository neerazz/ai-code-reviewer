# AI-Powered Code Review & Migration Assistant

This project is an intelligent code review system that uses LLMs to provide context-aware code reviews, suggest optimizations, detect security vulnerabilities, and automate code migrations across different frameworks/versions.

## Project Structure

The project is organized as a monorepo with the following structure:

-   `ai-code-reviewer/`
    -   `backend/`: The FastAPI backend application.
        -   `api/`: The API endpoints.
            -   `routers/`: The API routers.
            -   `schemas/`: The Pydantic schemas.
    -   `frontend/`: The React frontend application.
        -   `src/`: The source code.
            -   `components/`: The React components.
    -   `extensions/`: Browser and IDE extensions.
    -   `ml/`: Machine learning models and components.
    -   `infrastructure/`: Kubernetes and Terraform configurations.
    -   `docs/`: Project documentation.
    -   `docker-compose.yml`: A script to start both the frontend and backend services.

## Getting Started

To get the project up and running, you will need to have Docker and Docker Compose installed on your local machine.

### Prerequisites

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ai-code-reviewer.git
    cd ai-code-reviewer
    ```

2.  **Start the services:**

    ```bash
    docker-compose up -d
    ```

    This command will build and start the frontend and backend services in detached mode.

3.  **Access the application:**

    -   **Frontend:** Open your web browser and navigate to [http://localhost:3000](http://localhost:3000).
    -   **Backend:** The API is accessible at [http://localhost:8000](http://localhost:8000).

## Usage

1.  **Open the web application** in your browser.
2.  **Enter a code snippet** in the text area.
3.  **Click the "Review" button** to submit the code for analysis.
4.  **View the review results** displayed on the screen.

## Contributing

We welcome contributions to the AI-Powered Code Review & Migration Assistant! To contribute, please follow these steps:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix.
3.  **Make your changes** and commit them with a descriptive message.
4.  **Push your changes** to your forked repository.
5.  **Create a pull request** to the main repository.

We appreciate your contributions and will review your pull request as soon as possible.
