#!/usr/bin/env bash

if [[ $0 == $BASH_SOURCE ]]; then
    echo "source this script!"
    exit 1
fi

eval "$(_{{cookiecutter.project_slug.upper()}}_COMPLETE=source {{cookiecutter.project_slug}})"

