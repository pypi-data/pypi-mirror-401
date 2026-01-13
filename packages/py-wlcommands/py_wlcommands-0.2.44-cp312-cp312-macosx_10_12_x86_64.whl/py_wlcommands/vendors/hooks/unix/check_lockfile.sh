#!/bin/sh

# Check uv.lock consistency and update if needed

# Check if pyproject.toml exists
if [ ! -f pyproject.toml ]; then
    echo "No pyproject.toml found, skipping uv.lock check"
    exit 0
fi

# Use uv lock to check and update lockfile
if uv lock --check; then
    echo "uv.lock file is already consistent"
    exit 0
else
    # Update the lockfile
    if uv lock; then
        echo "Updated uv.lock file"
        exit 0
    else
        echo "Error: uv lock failed" >&2
        exit 1
    fi
fi
