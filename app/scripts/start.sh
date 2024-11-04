#!/bin/bash

# Exit in case of error
set -e

docker compose build

sleep 1;

# Build and run containers
docker compose up -d

# Hack to wait for postgres container to be up before running alembic migrations

sleep 5;

docker compose run --rm backend alembic upgrade head

docker compose run --rm backend python3 app/initialize.py