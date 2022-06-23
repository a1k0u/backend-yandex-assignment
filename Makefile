# Variables for python project
VENV_NAME=venv
VENV_PATH=$(shell pwd)/$(VENV_NAME)/bin
PYTHON=$(VENV_PATH)/python3
PIP=$(VENV_PATH)/pip3
APP=$(shell pwd)/handlers/app.py

create:
	python3 -m venv $(VENV_NAME)

run:
	$(PYTHON) $(APP)

install:
	$(PIP) install -r requirements.txt

freeze:
	$(PIP) freeze > requirements.txt

database:
	touch db.sqlite

docker_build:
	docker build -t basic-flask:latest --build-arg APP_IMAGE=python:3.9.5-alpine .

docker_run:
	docker container run -p 5000:5000 -dit --name flaskApp basic-flask:latest