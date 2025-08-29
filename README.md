Full-Stack QA Project: Automated Testing for a To-Do Web App
This repository contains a complete QA project demonstrating the full lifecycle of software testing, from initial development and manual testing to a fully automated CI/CD pipeline for a modern web application.

The core application is a feature-rich To-Do list built with Python and Flask. It has been designed and tested using a multi-layered strategy that covers UI, API, and DevOps practices.

Core Application & Design
The foundation is a Python-based web application built using the Flask framework and SQLAlchemy for database interactions. Initially created with basic functionality, the app underwent a complete UI/UX redesign to improve its visual appeal and usability, incorporating features like task priorities and due dates.

Multi-Layered Testing Strategy 🧪
The project implements a thorough testing strategy that covers all layers of the application:

Manual Testing: Establishes a baseline for quality by creating a formal test plan and writing detailed manual test cases for all features, including positive and negative scenarios.

UI Automation: Uses Selenium and PyTest to automate user interactions. These tests translate the manual test cases into code that simulates a user clicking through the application in a real web browser.

API Automation: Bypasses the UI to test the backend logic directly using Flask's Test Client. These tests are significantly faster and more stable than UI tests, making them ideal for rapid feedback in a CI environment.

DevOps and Automation 🚀
To ensure consistency and full automation, the project incorporates modern DevOps practices:

Containerization: The entire Flask application is packaged into a Docker container, creating a lightweight, portable, and consistent environment that solves the "it works on my machine" problem.

Continuous Integration (CI/CD): An automated testing pipeline is built using GitHub Actions. This pipeline automatically runs all the API tests every time code is pushed to the repository, providing immediate feedback and ensuring that new changes haven't introduced any bugs.

Tech Stack 🛠️
Backend: Python, Flask, SQLAlchemy

Frontend: HTML, CSS

Testing: PyTest, Selenium, Flask Test Client

Containerization: Docker

CI/CD: GitHub Actions

How to Run the Project
Running Locally
Clone the repository: git clone <repository-url>

Navigate to the project directory: cd qa-todo-project

Create and activate a virtual environment.

Install dependencies: pip install -r requirements-dev.txt

Run the application: python app.py

Access the app at http://12.0.0.1:5000.

Running with Docker
Ensure Docker Desktop is installed and running.

Build the Docker image: docker build -t clarity-tasks-app .

Run the container: docker run -p 5001:5000 -d clarity-tasks-app

Access the app at http://localhost:5001.

Running the Tests
Make sure you are in the project directory with the virtual environment activated.

To run UI tests: pytest test_app_ui.py (requires the Flask app to be running locally).

To run API tests: pytest test_app_api.py (does not require the app to be running).