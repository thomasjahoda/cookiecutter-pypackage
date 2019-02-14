#!/usr/bin/env bash

if [[ $0 == $BASH_SOURCE ]]; then
    echo "source this script!"
    exit 1
fi

eval "$(_MANAGED_INFONOVA_SERVICE_TOOLS_COMPLETE=source {{cookiecutter.project_slug}})"

