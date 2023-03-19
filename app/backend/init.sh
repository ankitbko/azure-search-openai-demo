#!/bin/bash

# reinstall hnswlib to avoid illegal instruction (core dumped) exception due to change in host OS flavor.
pip install --upgrade --force-reinstall hnswlib
gunicorn --timeout 600 --chdir=/code -b=0.0.0.0:80 app:app