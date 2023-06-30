#!/bin/bash

# creates the venv
python3 -m venv .venv

# activates
source .venv/bin/activate

# pip it
python3 -m pip install --upgrade pip
pip install -r requirements.txt


