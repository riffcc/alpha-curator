#!/bin/bash
pip3 install virtualenv
python3 -m venv venv
source venv/bin/activate
pip3 install PyMySQL
pip3 install grizzled-python
pip3 install psycopg2
pip3 install sqlalchemy
pip3 install queries
