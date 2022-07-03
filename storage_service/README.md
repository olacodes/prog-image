# Storage Service

![Storage Service](https://github.com/olacodes/prog-image/actions/workflows/storage-service.yml/badge.svg)

[![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Technologies

- [Python 3.9](https://python.org) : Base programming language for development
- [FastAPI](https://fastapi.tiangolo.com/) : Development framework used for the application
- [Amazon S3](https://aws.amazon.com/s3/): Amazon Simple Storage Service (Amazon S3) is an object storage service offering scalability, data availability, security, and performance.
- [Pillow](https://pillow.readthedocs.io/en/stable/) : A python Library for image processing
- [Celery](https://github.com/celery/celery): A simple, flexible, and reliable distributed system to process vast amounts of tasks
- [Flower](https://github.com/mher/flower): A web based tool for monitoring and administrating Celery clusters.
- [Redis](https://github.com/redis/redis-py): A NoSQL Database that serves as a Celery Broker and Result Backend
- [Github Actions](https://docs.github.com/en/free-pro-team@latest/actions) : Continuous Integration and Deployment
- [Docker Engine and Docker Compose](https://www.docker.com/) : Containerization of the application and services orchestration

## A Simple Architecture

![Storage Service](/static/storage_service.jpg)

## Getting Started

Getting started with this service is very simple, all you need is to have Git and Docker Engine installed on your machine.

- Clone the repository `git clone https://github.com/olacodes/prog-image.git`
- change directory `cd prog-image/storage_service`.
- Run `docker-compose -f common-services.yml -f storage-compose.yml up --build`
  - **NB:** _Running the above command for the first time will download all docker-images and third party packages needed for the app. This will take up to 5 minutes or more for the first build, others will be in a blink of an eye_

At this moment, your project should be up and running and start up the following Servers:

- FastAPI Development Server: http://localhost:8000
- Redis Server: http://localhost:6379
- Flower: http://localhost:5555

## Exploring The App

The following endpoints are available

| Endpoints | Methods | Content Type Accept |
| --------- | ------- | ------------------- |
| Storage
| /api/v1/images/ | Post | multipart/form-data |
| /api/v1/images/urls | Post | application/json |
| Retrieve
| /api/v1/images/ | Get | application/json |
| /api/v1/images/{image_name} | Get | application/json |
| /api/v1/images/file/{file_name}| Get | application/json |

## License

The MIT License - Copyright (c) 2022 - Present, ProgImage.com Storage Service.

## Author

Sodiq Olatunde
