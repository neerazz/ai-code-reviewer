# AI-Powered Code Review & Migration Assistant

This project is an intelligent code review system that uses LLMs to provide context-aware code reviews, suggest optimizations, detect security vulnerabilities, and automate code migrations across different frameworks/versions.

## Documentation

For detailed documentation, please see the [GitHub Pages site](https://your-org.github.io/ai-code-reviewer/).

## Project Structure

The project is organized as a monorepo with the following structure:

-   `ai-code-reviewer/`
    -   `backend/`: The FastAPI backend application.
    -   `frontend/`: The React frontend application.
    -   `extensions/`: Browser and IDE extensions.
    -   `ml/`: Machine learning models and components.
    -   `infrastructure/`: Kubernetes and Terraform configurations.
    -   `docs/`: Project documentation.
    -   `docker-compose.yml`: A script to start both the frontend and backend services.

For more information on the individual directories, please see the `README.md` file in each directory.

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

Please see the `CONTRIBUTING.md` file for guidelines on how to contribute to this project. To contribute to the documentation, please see the `docs/` directory.
