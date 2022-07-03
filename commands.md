# Check folder structure of a single process

docker exec -t -i process_service /bin/bash

## Run Test Locally
docker-compose exec storage_service pytest
docker-compose exec process_service pytest

## Run Flake 8 Locally
docker-compose exec storage_service flake8 storage_service

## Run Isort to automagically sort your imports
docker-compose exec storage_service isort storage_service
