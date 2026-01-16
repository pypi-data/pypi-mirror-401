"""Format path handler module."""

import os
from pathlib import Path

from tqdm import tqdm

from ...utils.logging import log_info
from .python_formatter import (
    _run_format_command,
    format_with_python_tools,
)
from .rust_formatter import format_rust_code


class FormatPathHandler:
    """Handler for formatting paths."""

    def _get_all_python_files(self, path):
        """Get all Python files in the given path recursively."""
        import sys
        from pathlib import Path as PathClass

        python_files = []

        # Convert to Path object if needed
        if (
            hasattr(path, "exists")
            and hasattr(path, "is_file")
            and hasattr(path, "is_dir")
            and hasattr(path, "name")
        ):
            path_obj = path
        else:
            path_obj = PathClass(path)

        if path_obj.exists():
            if path_obj.is_file() and path_obj.suffix == ".py":
                python_files.append(path_obj)
            elif path_obj.is_dir():
                # Recursively find all Python files in the directory
                for file_path in path_obj.rglob("*.py"):
                    python_files.append(file_path)

        return python_files

    def _step_by_step_processing(self, paths, env, quiet, unsafe):
        """Process files in step-by-step mode."""
        import sys

        # Get all Python files from all specified paths
        all_python_files = []
        for path in paths:
            python_files = self._get_all_python_files(path)
            all_python_files.extend(python_files)

        # Process files one by one
        success = True
        if not quiet and all_python_files:
            # Initialize progress bar with fixed width
            with tqdm(
                total=len(all_python_files),
                unit="file",
                ncols=100,  # Fixed total width
                dynamic_ncols=False,  # Disable dynamic adjustment
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
            ) as pbar:
                for file_path in all_python_files:
                    file_success = self._format_python_file(
                        file_path, str(file_path), env, quiet, unsafe
                    )
                    if not file_success:
                        if not quiet:
                            print(f"\nFormatting failed for file: {file_path}")
                            print("Stopping at first error as requested.")
                        success = False
                        sys.exit(1)
                    # Update progress bar with fixed width filename in description
                    max_len = 28
                    if len(file_path.name) > max_len:
                        # Truncate to max_len - 3 characters + ellipsis
                        truncated_name = file_path.name[: max_len - 3] + "..."
                    else:
                        truncated_name = file_path.name
                    # Set description with fixed width
                    pbar.set_description(f"Processing {truncated_name:<28}")
                    pbar.update(1)
        else:
            # No progress bar if quiet or no files
            for file_path in all_python_files:
                file_success = self._format_python_file(
                    file_path, str(file_path), env, quiet, unsafe
                )
                if not file_success:
                    if not quiet:
                        print(f"Formatting failed for file: {file_path}")
                        print("Stopping at first error as requested.")
                    success = False
                    sys.exit(1)

        # Run pre-commit on all files after step-by-step processing is complete
        if success and all_python_files:
            self._run_pre_commit_on_all_files(env, quiet)

    def _non_step_by_step_processing(self, paths, env, quiet, unsafe):
        """Process files in normal (non-step-by-step) mode."""
        from pathlib import Path as PathClass

        # Original behavior: process paths normally
        for path in paths:
            # Convert to Path object if needed
            if (
                hasattr(path, "exists")
                and hasattr(path, "is_file")
                and hasattr(path, "is_dir")
                and hasattr(path, "name")
            ):
                path_obj = path
            else:
                path_obj = PathClass(path)

            if path_obj.exists():
                if path_obj.is_file() and path_obj.suffix == ".py":
                    self._format_python_file(path_obj, path, env, quiet, unsafe)
                elif path_obj.is_dir():
                    self._format_directory(path_obj, path, env, quiet, unsafe)
            else:
                if not quiet:
                    print(f"Warning: Path {path} does not exist")

    def format_specified_paths(
        self, paths, env, quiet, unsafe=False, step_by_step=False
    ):
        """Format specified paths."""
        if step_by_step:
            self._step_by_step_processing(paths, env, quiet, unsafe)
        else:
            self._non_step_by_step_processing(paths, env, quiet, unsafe)

    def _format_python_file(self, path_obj, original_path, env, quiet, unsafe):
        """Format a single Python file."""
        try:
            # In step-by-step mode, we want to suppress all output except errors
            step_by_step_quiet = quiet or True  # Always quiet in step-by-step mode

            # Format with ruff check
            ruff_check_cmd = ["uv", "run", "ruff", "check", "--fix"]
            if unsafe:
                ruff_check_cmd.append("--unsafe-fixes")
            ruff_check_cmd.append(str(path_obj))

            check_success, check_output = _run_format_command(
                ruff_check_cmd, env, step_by_step_quiet, passthrough=False
            )
            if not check_success:
                # Only print errors when we have a failure
                if not quiet:
                    print(check_output)
                return False

            # Format with ruff format
            format_success, format_output = _run_format_command(
                [
                    "uv",
                    "run",
                    "ruff",
                    "format",
                    str(path_obj),
                ],
                env,
                step_by_step_quiet,
                passthrough=False,
            )
            if not format_success:
                # Only print errors when we have a failure
                if not quiet:
                    print(format_output)
                return False

            return True
        except Exception as e:
            if not quiet:
                print(f"Warning: Failed to format {original_path}: {e}")
            return False

    def _format_directory(self, path_obj, original_path, env, quiet, unsafe):
        """Format a directory."""
        # Format with Python tools
        format_with_python_tools(str(path_obj), env, quiet, unsafe=unsafe)

        # Special handling for rust directory
        if path_obj.name == "rust":
            format_rust_code(str(path_obj), env, quiet)

        # Run pre-commit on the directory
        self._run_pre_commit_on_directory(path_obj, original_path, env, quiet)

    def _get_pre_commit_config_path(self):
        """Find the pre-commit config path."""
        precommit_config_path = ".pre-commit-config.yaml"
        if not os.path.exists(precommit_config_path):
            precommit_config_path = ".wl/.pre-commit-config.yaml"
        return precommit_config_path

    def _run_pre_commit_command(
        self, command_args, env, quiet, description=None, original_path=None
    ):
        """Run pre-commit command with given arguments."""
        from ...utils.subprocess_utils import SubprocessExecutor

        try:
            executor = SubprocessExecutor()
            precommit_config_path = self._get_pre_commit_config_path()

            # Only run pre-commit if config exists
            if os.path.exists(precommit_config_path):
                if not quiet and description:
                    print(description)

                command = (
                    [
                        "uv",
                        "run",
                        "pre-commit",
                        "run",
                    ]
                    + command_args
                    + [
                        "--config",
                        precommit_config_path,
                    ]
                )

                # Execute pre-commit directly with SubprocessExecutor to handle its exit codes properly
                # Pre-commit returns non-zero exit code if it fixes issues, which is expected behavior
                result = executor.run(command, env=env, quiet=quiet)

                # Always log that pre-commit was run, regardless of exit code
                if not quiet and result.stdout:
                    print(result.stdout)

        except Exception as e:
            if not quiet:
                if original_path:
                    print(f"Warning: Pre-commit failed for {original_path}: {e}")
                else:
                    print(f"Warning: Pre-commit failed: {e}")

    def _run_pre_commit_on_all_files(self, env, quiet):
        """Run pre-commit on all files after step-by-step processing is complete."""
        command_args = ["--all-files"]
        description = "\nRunning pre-commit on all files..."
        self._run_pre_commit_command(command_args, env, quiet, description)

    def _run_pre_commit_on_file(self, path_obj, original_path, env, quiet):
        """Run pre-commit on a single file."""
        command_args = ["--files", str(path_obj)]
        self._run_pre_commit_command(
            command_args, env, quiet, original_path=original_path
        )

    def _run_pre_commit_on_directory(self, path_obj, original_path, env, quiet):
        """Run pre-commit on a directory."""
        command_args = ["--all-files"]
        self._run_pre_commit_command(
            command_args, env, quiet, original_path=original_path
        )

    def _step_by_step_defaults(
        self, current_path: Path, env: dict, quiet: bool, unsafe: bool
    ) -> None:
        """Process default paths in step-by-step mode."""
        import sys
        from pathlib import Path

        src_path = current_path / "src"
        tools_path = current_path / "tools"
        examples_path = current_path / "examples"
        tests_path = current_path / "tests"

        # Get all Python files from all default paths
        all_python_files = []
        for path in [src_path, tools_path, examples_path, tests_path]:
            if path.exists():
                python_files = self._get_all_python_files(path)
                all_python_files.extend(python_files)

        # Process files one by one
        success = True
        if not quiet and all_python_files:
            # Initialize progress bar with fixed width
            with tqdm(
                total=len(all_python_files),
                unit="file",
                ncols=100,  # Fixed total width
                dynamic_ncols=False,  # Disable dynamic adjustment
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
            ) as pbar:
                for file_path in all_python_files:
                    file_success = self._format_python_file(
                        file_path, str(file_path), env, quiet, unsafe
                    )
                    if not file_success:
                        if not quiet:
                            print(f"\nFormatting failed for file: {file_path}")
                            print("Stopping at first error as requested.")
                        success = False
                        sys.exit(1)
                    # Update progress bar with fixed width filename in description
                    max_len = 28
                    if len(file_path.name) > max_len:
                        # Truncate to max_len - 3 characters + ellipsis
                        truncated_name = file_path.name[: max_len - 3] + "..."
                    else:
                        truncated_name = file_path.name
                    # Set description with fixed width
                    pbar.set_description(f"Processing {truncated_name:<28}")
                    pbar.update(1)
        else:
            # No progress bar if quiet or no files
            for file_path in all_python_files:
                file_success = self._format_python_file(
                    file_path, str(file_path), env, quiet, unsafe
                )
                if not file_success:
                    if not quiet:
                        print(f"Formatting failed for file: {file_path}")
                        print("Stopping at first error as requested.")
                    success = False
                    sys.exit(1)

        # Run pre-commit on all files after step-by-step processing is complete
        if success and all_python_files:
            self._run_pre_commit_on_all_files(env, quiet)

    def _non_step_by_step_defaults(
        self, current_path: Path, env: dict, quiet: bool, unsafe: bool, for_lint: bool
    ) -> None:
        """Process default paths in normal (non-step-by-step) mode."""
        src_path = current_path / "src"
        tools_path = current_path / "tools"
        examples_path = current_path / "examples"
        tests_path = current_path / "tests"
        rust_path = current_path / "rust"

        if src_path.exists():
            log_info("Formatting src directory...")
            format_with_python_tools(str(src_path), env, quiet, unsafe=unsafe)
        if tools_path.exists():
            log_info("Formatting tools directory...")
            format_with_python_tools(str(tools_path), env, quiet, unsafe=unsafe)
        if examples_path.exists():
            log_info("Formatting examples directory...")
            format_with_python_tools(str(examples_path), env, quiet, unsafe=unsafe)
        if tests_path.exists():
            log_info("Formatting tests directory...")
            format_with_python_tools(str(tests_path), env, quiet, unsafe=unsafe)
        # Type stubs generation removed from format; handled in build dist
        if rust_path.exists() and not for_lint:
            log_info("Formatting Rust code...")
            format_rust_code(str(rust_path), env, quiet)

        # Run pre-commit on all files
        try:
            precommit_config_path = self._get_pre_commit_config_path()
            if os.path.exists(precommit_config_path):
                log_info("Running pre-commit hooks...")
                # Use the existing method to run pre-commit on all files
                self._run_pre_commit_on_all_files(env, quiet)
            else:
                if not quiet:
                    print(
                        "Warning: .pre-commit-config.yaml not found in current directory or .wl directory, skipping pre-commit hooks"
                    )
        except Exception as e:
            if not quiet:
                print(f"Warning: Pre-commit hooks failed: {e}")

    def format_defaults(
        self,
        current_path: Path,
        env: dict,
        quiet: bool,
        unsafe: bool,
        for_lint: bool,
        step_by_step=False,
    ) -> None:
        """Format default paths."""
        if step_by_step:
            self._step_by_step_defaults(current_path, env, quiet, unsafe)
        else:
            self._non_step_by_step_defaults(current_path, env, quiet, unsafe, for_lint)
