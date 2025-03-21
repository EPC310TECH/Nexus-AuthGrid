#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Print all environment variables to verify
echo "Environment variables set from .env file:"
while IFS= read -r line; do
    if [[ ! "$line" =~ ^# && "$line" =~ .*=.* ]]; then
        varname=$(echo "$line" | cut -d '=' -f 1)
        echo "$varname=${!varname}"
    fi
done < .env