# Check folder structure of a single process

docker exec -t -i process_service /bin/bash

## Run Test Locally
docker-compose exec storage_service pytest
docker-compose exec process_service pytest
