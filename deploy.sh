#!/bin/bash

# Provide your Docker Hub credentials via environment variables
DOCKER_HUB_USERNAME="eduardomdcup"
DOCKER_HUB_PASSWORD="PRxMm9buY2sXWR"

# Log in to Docker Hub using environment variables
echo "$DOCKER_HUB_PASSWORD" | docker login --username "$DOCKER_HUB_USERNAME" --password-stdin

# Pull the latest version of the Docker image
docker pull eduardomdcup/dynamicity_unm:latest

# Stop and remove any existing container with the same name
#docker stop dynamiCITY_prod || true
#docker rm dynamiCITY_prod || true

# Run a new container with the pulled image
docker run -d --name dynamiCITY_prod -p 8000:8000 eduardomdcup/dynamicity_unm:latest

# Logout from Docker Hub
docker logout