# TDD and BDD Final Project: Product Account Service

[![CI Build](https://github.com/sushant-me/tdd-bdd-final-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/sushant-me/tdd-bdd-final-project/actions/workflows/ci-build.yaml)

## Project Overview
This project demonstrates a production-ready Microservice developed using **Test Driven Development (TDD)** and **Behavior Driven Development (BDD)**. It provides a RESTful API for managing product accounts, secured with security headers and automated via CI/CD pipelines.

## Key Features
* **RESTful API**: Full CRUD (Create, Read, Update, Delete) and List functionality.
* **TDD**: Unit tests with 100% coverage using `nosetests` and `coverage`.
* **BDD**: Acceptance tests using `Behave` and `Selenium`.
* **CI/CD**: Automated testing and linting via GitHub Actions.
* **Security**: Implemented Flask-Talisman for security headers and CORS policies.
* **Containerization**: Dockerized application deployed to Kubernetes/OpenShift.

## Development Environment
To run the service locally, ensure you have Python 3.9+ and PostgreSQL installed.

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
