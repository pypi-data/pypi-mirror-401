#!/bin/sh

# Check uv.lock consistency and update if needed

# Check if pyproject.toml exists
if [ ! -f pyproject.toml ]; then
    echo "No pyproject.toml found, skipping uv.lock check"
    exit 0
fi

# Check if uv.lock exists
if [ ! -f uv.lock ]; then
    # If uv.lock doesn't exist, create it
    if uv lock; then
        echo "Created uv.lock file"
        exit 0
    else
        echo "Error: uv lock failed" >&2
        exit 1
    fi
fi

# Use uv lock --check as the sole standard to determine if uv.lock needs update
if uv lock --check; then
    echo "uv.lock file is already consistent"
    exit 0
else
    # Only update if uv lock --check fails
    if uv lock; then
        echo "Updated uv.lock file"
        exit 0
    else
        echo "Error: uv lock failed" >&2
        exit 1
    fi
fi
