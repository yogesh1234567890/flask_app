# Flask App

This project is a Flask-based application for building APIs. Below are the instructions for setting up, running, and accessing the application.

---

## Installation and Setup

## 📋 Prerequisites

Before you start, make sure you have the following tools installed:

- [Docker](https://www.docker.com/get-started) 🐳
- [Docker Compose](https://docs.docker.com/compose/install/) 🛠️

---

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yogesh1234567890/flask_app.git
   ```

2. Build the Docker containers:

    ```bash
    docker-compose build
   ```


3. Start the Containers: Start all the services using Docker Compose:
    ```bash
    docker-compose up
   ```


   This command will start the Flask application and any other services (e.g., Redis, Celery) defined in docker-compose.yml.

4. Access the Application:
   Open your browser and navigate to: http://127.0.0.1:5001/swagger/.
   The Flask app will be running on port 5001 by default.
   
5. Run the Celery Worker: 
   In a separate terminal window, start the Celery worker to process background tasks:

   ```bash
   docker-compose run celery
   ```

This ensures that tasks submitted by the Flask app are processed asynchronously.

6.Testing the API: Use tools like Postman to test the API endpoints. Example:
   ```bash
      POST http://localhost:5001/upload
      GET http://localhost:5001/status/{task_id}
   ```



7.Stop the Containers: To stop and remove all running containers:
   ```bash
      docker-compose down
   ```

This will clean up containers, networks, and volumes defined in docker-compose.yml.

