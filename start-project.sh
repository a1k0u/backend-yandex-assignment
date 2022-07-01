#!/bin/bash

<< StartProjectDoc
  For ubuntu users:
  - Exports all environmental variables,
  - creates virtual env from python,
  - installs all dependencies for project,
  - downloads Postgres,
  - opens console of DB where user have to insert commands
    which will be in stdout, user should copy and paste it.
  - creates tables in DB.
StartProjectDoc

LOG="\033[41m\033[30m[LOG]:\033[0m"
LINE="\033[42m\033[30m---------------------------------------------------------------\033[0m"

echo "$LOG export env variables for database."
while IFS= read -r line; do export "$line"; done < .env

echo -e "$LOG set virtual environment for python."
make create

echo -e "$LOG install all dependencies for python project."
make install

echo -e "$LOG download postgresql for ubuntu."
sudo apt-get install postgresql-12

echo -e "$LOG download libs for psycopg2."
sudo apt-get install libpq-dev gcc

echo -e "$LOG now you'll open db and paste this commands into console:"
echo -e "$LINE\n"
echo "CREATE DATABASE $PGDB;"
echo "CREATE USER $PGUSER WITH PASSWORD '$PGPASSWD';"
echo "GRANT ALL PRIVILEGES ON DATABASE $PGDB TO $PGUSER;"
echo "\q"
echo -e "\n$LINE"
sudo -u postgres psql

echo -e "$LOG check out engine connection."
make db_engine

echo -e "$LOG create tables for db."
make init_tables
