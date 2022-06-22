# ProgImage.com Storage Service

![Storage Service](https://github.com/olacodes/prog-image/actions/workflows/ci.yml/badge.svg)

[![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Technologies

- [Python 3.9](https://python.org) : Base programming language for development
- [FastAPI](https://fastapi.tiangolo.com/) : Development framework used for the application
- [Django Rest Framework](https://www.django-rest-framework.org/) : Provides API development tools for easy API development
- [Pillow](https://pillow.readthedocs.io/en/stable/) : A python Library for image processing
- [Bash Scripting](https://www.codecademy.com/learn/learn-the-command-line/modules/bash-scripting) : Create convenient script for easy development experience
- [Celery](https://github.com/celery/celery): A simple, flexible, and reliable distributed system to process vast amounts of tasks
- [Flower](https://github.com/mher/flower): A web based tool for monitoring and administrating Celery clusters.
- [SQLite](https://www.sqlite.org/index.html): Application relational databases for development
- [Redis](https://github.com/redis/redis-py): A NoSQL Database that serves as a Celery Broker and Result Backend
- [Github Actions](https://docs.github.com/en/free-pro-team@latest/actions) : Continuous Integration and Deployment
- [Docker Engine and Docker Compose](https://www.docker.com/) : Containerization of the application and services orchestration

## A Simple Architecture

## Getting Started

Getting started with this project is very simple, all you need is to have Git and Docker Engine installed on your machine.

- Clone the repository `git clone https://github.com/olacodes/prog-image.git`
- change directory `cd prog-image/storage_service`.
- Run `docker-compose up --build`
  - **NB:** _Running the above command for the first time will download all docker-images and third party packages needed for the app. This will take up to 5 minutes or more for the first build, others will be in a blink of an eye_

At this moment, your project should be up and running and start up the following Servers:

- FastAPI Development Server: http://localhost:8000
- Redis Server: http://localhost:6379
- Flower: http://localhost:5555

## Exploring The App

## License

The MIT License - Copyright (c) 2022 - Present, ProgImage.com Storage Service.

## Author

Sodiq Olatunde
