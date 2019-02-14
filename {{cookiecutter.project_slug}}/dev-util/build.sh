#!/usr/bin/env bash

source activate-venv.sh || exit 1

output_logs_if_successful=false
cd ..

function execute_and_translate_to_absolute_filenames() {
    command=$*
    echo -n "$command ... "
    output="$(${command} 2>&1)"
    exit_code=$?
    if [ ${exit_code} != 0 ]; then
        output="$(echo "$output" | sed -e "s|^{{cookiecutter.project_slug}}/|$(pwd)/{{cookiecutter.project_slug}}/|g")"
        output="$(echo "$output" | sed -e "s|^tests/|$(pwd)/tests/|g")"
        echo "failed with exit code ${exit_code}"
        echo "$output"
        exit 1
    fi
    if [ ${output_logs_if_successful} == "true" ]; then
        echo "$output"
    fi
    echo "success"
}

export EXECUTE_HEAVY_INTEGRATION_TESTS=false
export EXECUTE_LIGHTWEIGHT_INTEGRATION_TESTS=true
execute_and_translate_to_absolute_filenames make test
execute_and_translate_to_absolute_filenames make lint
execute_and_translate_to_absolute_filenames make type-check

execute_and_translate_to_absolute_filenames make install

