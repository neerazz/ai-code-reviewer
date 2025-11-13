---
sidebar_position: 2
---

# Installation

To get the project up and running, you will need to have Docker and Docker Compose installed on your local machine.

## Prerequisites

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

## Running the Application

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
