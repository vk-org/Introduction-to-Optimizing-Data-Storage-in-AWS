#!/bin/bash
. venv/bin/activate
export FLASK_APP=main.py
python -m flask run --host=0.0.0.0 -p 80 >> server_access.log 2>&1 &
