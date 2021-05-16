#!/bin/bash

for dependencies_file in ./requirements/*; do
    echo -e "" 
    echo -e "Installing dependencies from ${dependencies_file##*/}"
    echo -e ""
    echo -e ""
    pip install -r "$dependencies_file" --upgrade --force-reinstall --no-cache-dir
    echo -e ""
done
