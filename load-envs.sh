#!/bin/bash

echo "[LOG]: export env variables for database."
while IFS= read -r line; do export "$line"; done < .env
