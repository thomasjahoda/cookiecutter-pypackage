#!/usr/bin/env bash

echo "The virtualenv {{cookiecutter.project_slug}} is expected to have been created already via virtualenvwrapper"
source activate-venv.sh || exit 1

cd ..

pip install --upgrade -r "requirements/setup.txt" -r "requirements/runtime.txt" -r "requirements/test.txt" || exit 1

echo "Now installing project in development mode:"
pip install -e . || exit 1
