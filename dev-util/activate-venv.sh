#!/usr/bin/env bash

source ~/.bashrc
if [[ $0 == $BASH_SOURCE ]]; then
    echo "source this script!"
    exit 1
fi
if [ -z "$VIRTUALENVWRAPPER_SCRIPT" ]; then
    echo "The venv managed virtualenvwrapper is expected to be used but the variable VIRTUALENVWRAPPER_SCRIPT was not found.
Set the variable VIRTUALENVWRAPPER_SCRIPT (and related vars) in your .bashrc or other global configuration file."
    exit 1
fi

source "${VIRTUALENVWRAPPER_SCRIPT}"

workon cookiecutter-pypackage

echo "Activated venv."
