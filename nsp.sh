#!/bin/bash

python -m venv .nsp
source .nsp/bin/activate
pip install -r $PWD/requirements.txt
python $PWD/src/application.py --configuration $1
