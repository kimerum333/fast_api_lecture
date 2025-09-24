#!/bin/bash

deactivate 2> /dev/null
source .venv/bin/activate
uvicorn src.main:app --reload
