@echo off

REM Check uv.lock consistency and update if needed

REM Check if pyproject.toml exists
if not exist "pyproject.toml" (
    echo No pyproject.toml found, skipping uv.lock check
    exit /b 0
)

REM Use uv lock to check and update lockfile
uv lock --check

REM Check if uv lock --check succeeded
if errorlevel 1 (
    REM Update the lockfile
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
