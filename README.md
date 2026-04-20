# The Singer Sargent Archives - CS 3200 Final Project

# Quickstart: Running the Project
## Setting Up the .env File
In your api directory set up a `.env` file with the following variables.

      SECRET_KEY= <a random secret>
      DB_USER=root
      DB_HOST=db
      DB_PORT=3306
      DB_NAME=Singer-Sargent-Archive
      MYSQL_ROOT_PASSWORD= <a secure password>
## Running The Docker Containers
In your `26S-Singer-Sargent-Archive` directory, run the command `docker composed down` to close all current running containers, then run `docker compose up -d` to run the containers that house the project.

The Streamlit website can be accessed by going to the port that the `web-app` container is running on

# Roles Overview
## Archivist
## Curator
## Director
## Researcher
---
Made with ♥ by Yuval Ailon, Doruk Akalin, Joel Guerra, Austin Lok, and Cooper Tarbuck 