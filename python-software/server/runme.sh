#!/bin/bash

#exit on error
set -e

#set up variables
VENV_DIR="venv"
APP_FILE="app.py"

#create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "> Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

#activate virtual environment
echo "> Activating virtual environment..."
source "$VENV_DIR/bin/activate"

#install required modules
echo "> Installing packages..."
pip install python-osc pyserial  #modules to install

#run the Python application
if [ -f "$APP_FILE" ]; then
  echo "Running $APP_FILE..."
  python "$APP_FILE"
else
  echo "Python app file $APP_FILE not found!"
fi