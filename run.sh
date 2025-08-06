#!/bin/bash

# Start MongoDB
docker-compose up -d mongodb

echo "Select scenario:"
echo "1) Run Python app"
echo "2) Run Go microservices and CLI"
echo "3) Run both Python app and Go microservices"
echo "4) Exit"

read -p "Enter choice: " choice

case $choice in
    1)
        docker-compose up python-app
        ;;
    2)
        docker-compose up employee-service department-service
        docker-compose run --rm cli
        ;;
    3)
        docker-compose up -d employee-service department-service
        docker-compose up python-app
        docker-compose run --rm cli
        ;;
    4)
        echo "Exiting..."
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

# Cleanup
docker-compose down