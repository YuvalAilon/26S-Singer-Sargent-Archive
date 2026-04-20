# The Singer Sargent Archives - CS 3200 Final Project

The Singer-Sargent archives is a data driven application that aims to help museums keep track of their collections. 

It is built with a MySQL & Flask backend and a Streamlit frontend.

[Demo Video](https://youtu.be/gWvkZsjE2hQ)

Made with ♥ by Yuval Ailon, Doruk Akalin, Joel Guerra, Austin Lok, and Cooper Tarbuck

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
The Archivist is responsible for adding newly aquired artifacts to the collection, updating current entries in the database, and removing old entries from the database.

For better organization, the archivist can add similar artifacts (like multiple clothes in a fashion line, or a set of prints) to an artifact set.

To ensure the museum's collection has high quality data, an archivist can look up all pieces that have two or more fields missing, so that they can be filled in.

## Curator
The curator is responsible for creating new exhibits, and must know what loans are currently ongoing and what galleries are free to host their exhibits.

They handle loans, and have poweful filters for both artifacts and galleries, to find the perfect space for the perfect artworks.

## Director
The Director is responsible for handling donors, gallery expansions, and unpcoming returns.

They can see how how much individual donors have donated and their contact information, in order to send thank you letters and invitations to galas.

They can also create new expansion projects, and approve or deny existing ones.

## Researcher
The researcher does not work at the museum, but instead wants to use powerful search tools on the museum's collection.

They can search the collection by various filters (like artist name, style, and year of an artwork) as well as browse exhibits.

They also have access to museum stats, such as the amount of different styles of work each branch has, and the rate at which it rotates exhibits.

---
