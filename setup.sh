#/bin/sh

virtualenv venv --distribute
source venv/bin/activate
pip install -r requirements.txt
