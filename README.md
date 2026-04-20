# The Singer Sargent Archives - CS 3200 Final Project

This is a template repo for Dr. Fontenot's Spring 2026 CS 3200 Course Project.

It includes most of the infrastructure setup (containers), sample databases, and example UI pages. Explore it fully and ask questions!

## Prerequisites

- A GitHub Account
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.
- A distribution of Python running on your laptop. The distribution supported by the course is [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install).
  - Create a new Python 3.11 environment in `conda` named `db-proj` by running:  
     ```bash
     conda create -n db-proj python=3.11
     ```
  - Install the Python dependencies listed in `api/requirements.txt` and `app/src/requirements.txt` into your local Python environment. You can do this by running `pip install -r requirements.txt` in each respective directory.
     ```bash
     cd api
     pip install -r requirements.txt
     cd ../app/src
     pip install -r requirements.txt
     ```
     Note that the `..` means go to the parent folder of the folder you're currently in (which is `api/` after the first command).
     > **Why install locally if everything runs in Docker?** Installing the packages locally lets your IDE (VSCode) provide autocompletion, linting, and error highlighting as you write code. The app itself always runs inside the Docker containers — the local install is just for editor support.
- VSCode with the Python Plugin installed
  - You may use some other Python/code editor.  However, Course staff will only support VS Code. 


## Structure of the Repo

- This repository is organized into five main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
  - `./datasets` - folder for storing datasets

- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database. 