@echo off

REM Check uv.lock consistency and update if needed

REM Check if pyproject.toml exists
if not exist "pyproject.toml" (
    echo No pyproject.toml found, skipping uv.lock check
    exit /b 0
)

REM Check if uv.lock exists
if not exist "uv.lock" (
    REM If uv.lock doesn't exist, create it
    uv lock
    if errorlevel 1 (
        echo Error: uv lock failed
        exit /b 1
    ) else (
        echo Created uv.lock file
        exit /b 0
    )
)

REM Use uv lock --check as the sole standard to determine if uv.lock needs update
uv lock --check

REM Check if uv lock --check succeeded
if errorlevel 1 (
    REM Only update if uv lock --check fails
    uv lock
    if errorlevel 1 (
        echo Error: uv lock failed
        exit /b 1
    ) else (
        echo Updated uv.lock file
        exit /b 0
    )
) else (
    echo uv.lock file is already consistent
    exit /b 0
)
