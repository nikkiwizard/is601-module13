## Module 13

## DockerHub URL:
https://hub.docker.com/repository/docker/nikkiwizard/601_module13/general

## Github Actions Run:
![Actions](screenshots/actions.png "Github Actions Workflow screenshot")

## Playwright E2E Tests:
![Playwright](screenshots/playwright.png "Playwright E2E Tests")

## Registration:
![Registration](screenshots/register.png "Registration Page")

## Login:
![Login](screenshots/login.png "Login Page")

## DockerHub Screenshot:
![DockerHub](screenshots/dockerhub.png "Dockerhub screenshot")

## Running Tests
Before running tests, be sure that Docker is up and running with the following command: <br>
docker compose up --build

To run tests locally, follow these commands: <br>
python3 -m venv venv <br>
source venv/bin/activate <br>
pip install -r requirements.txt <br>
docker compose exec web pytest <br>

A note: You could run the Playwright tests by running <br>
docker compose exec web pytest tests/e2e <br>

You can also manually test your application by doing manual checks via OpenAPI going to http://localhost:8000/docs. You can test registration, login, auth, and all the calculation endpoints by clicking "Try it out". 