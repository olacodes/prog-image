# Process Service

![Process Service](https://github.com/olacodes/prog-image/actions/workflows/process-service.yml/badge.svg)

[![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Process service is a Restful api service that allows you to process images like, compression, adding filters, rotate images,and thumbnail creation

## Technologies

- [Python 3.9](https://python.org) : Base programming language for development
- [FastAPI](https://fastapi.tiangolo.com/) : Development framework used for the application
- [Pillow](https://pillow.readthedocs.io/en/stable/) : A python Library for image processing
- [Celery](https://github.com/celery/celery): A simple, flexible, and reliable distributed system to process vast amounts of tasks
- [Flower](https://github.com/mher/flower): A web based tool for monitoring and administrating Celery clusters.
- [Redis](https://github.com/redis/redis-py): A NoSQL Database that serves as a Celery Broker and Result Backend
- [Github Actions](https://docs.github.com/en/free-pro-team@latest/actions) : Continuous Integration and Deployment
- [Docker Engine and Docker Compose](https://www.docker.com/) : Containerization of the application and services orchestration

## A Simple Architecture

![Process Service](/static/process_service_arch.jpg)

## Getting Started

Getting started with this service is very simple, all you need is to have Git and Docker Engine installed on your machine.

- Clone the repository `git clone https://github.com/olacodes/prog-image.git`
- change directory `cd prog-image/process_service`.
- Run `docker-compose -f common-services.yml -f process-compose.yml up --build`
  - **NB:** _Running the above command for the first time will download all docker-images and third party packages needed for the app. This will take up to 5 minutes or more for the first build, others will be in a blink of an eye_

At this moment, your project should be up and running and start up the following Servers:

- FastAPI Development Server: http://localhost:9000
- Redis Server: http://localhost:6379
- Flower: http://localhost:5555

## Exploring The App

The following endpoints are available from the `BASE_URL: http://localhost:9000`

| Endpoints | Query Params | Methods | Content Type Accept |
| --------- | ------------ | ------- | ------------------- |
| Compression
| /api/vi/compress/files |size_ratio=0.9, width=200 | Post | multipart/form-data |
| /api/vi/compress/urls |quality=10, height=200 | Post | application/json |
| Filters
| /api/vi/filters/files |method=blur, smooth, emboss | Post | multipart/form-data |
| /api/vi/filters/urls |sharpen, edge_enhance, detail| Post | application/json |
| Rotation
| /api/vi/rotate/files |angle = 90, expand = True | Post | multipart/form-data |
| /api/vi/rotate/urls |angle = 90, expand = True | Post | application/json |
| Thumbnail
| /api/vi/thumbnail/files |width = 200, height = 200 | Post | multipart/form-data |
| /api/vi/thumbnail/urls |width = 200, height=200 | Post | application/json |

## License

The MIT License - Copyright (c) 2022 - Present, ProgImage.com Process Service.

## Author

Sodiq Olatunde
