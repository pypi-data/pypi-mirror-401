"""Lint reporter module.
Handles report generation for lint command.
"""

from pathlib import Path

from ...utils.logging import log_info
from ...utils.subprocess_utils import SubprocessExecutor, SubprocessResult


class LintReporter:
    """Reporter for lint command."""

    def generate_report(
        self,
        result: SubprocessResult,
        project_root: Path,
        quiet: bool,
        paths: list[str] | None,
        fix: bool,
    ) -> None:
        # Create todos directory in current working directory
        todos_dir = Path("todos")
        todos_dir.mkdir(exist_ok=True)

        report_file = todos_dir / "lint_report.md"
        error_file = todos_dir / "error.md"

        # Generate main lint report content
        lint_report_content = self._generate_lint_report(
            result, project_root, paths, fix, quiet
        )
        self._write_report_file(report_file, lint_report_content)

        # Generate error report content
        error_report_content = self._generate_error_report(project_root)
        self._write_report_file(error_file, error_report_content)

        # Handle large files report if needed
        large_files = self._find_large_python_files(project_root, paths)
        if large_files:
            self._generate_packaging_todo(large_files, project_root, quiet)

        # Log report generation messages
        if not quiet:
            log_info(
                f"Lint report generated at {report_file}",
                f"静态检查报告已生成到 {report_file}",
            )
            log_info(
                f"Error report generated at {error_file}",
                f"错误报告已生成到 {error_file}",
            )

    def _run_precommit_dry_run(self, project_root: Path, quiet: bool) -> str:
        """
        Run pre-commit dry-run and return only the failed results.
        """
        try:
            # Check if pre-commit config exists in .wl directory
            precommit_config = project_root / ".wl" / ".pre-commit-config.yaml"
            if precommit_config.exists():
                cmd = [
                    "pre-commit",
                    "run",
                    "--all-files",
                    "--config",
                    str(precommit_config),
                ]
            else:
                # Try default location
                cmd = ["pre-commit", "run", "--all-files"]

            result = SubprocessExecutor().run(cmd, cwd=project_root, quiet=True)

            # Combine stdout and stderr
            full_output = []
            if result.stdout:
                full_output.append(result.stdout)
            if result.stderr:
                full_output.append(result.stderr)
            full_text = "\n".join(full_output)

            # Filter only failed hooks
            if not full_text:
                return "No pre-commit issues found."

            # Split output into sections by hook results
            lines = full_text.splitlines()
            filtered_lines = []
            current_failed_hook = False

            for line in lines:
                # Check for passed hooks (ends with "Passed")
                if line.strip().endswith("Passed"):
                    current_failed_hook = False
                    continue  # Skip passed hooks
                # Check for failed hooks (ends with "Failed")
                elif line.strip().endswith("Failed"):
                    current_failed_hook = True
                    filtered_lines.append(line)
                # Keep lines for failed hooks
                elif current_failed_hook:
                    filtered_lines.append(line)

            if filtered_lines:
                return "\n".join(filtered_lines)
            else:
                return "No pre-commit issues found."
        except FileNotFoundError:
            return (
                "pre-commit command not found. Please ensure pre-commit is installed."
            )
        except Exception as e:
            return f"Error running pre-commit dry-run: {str(e)}"

    def _find_large_python_files(
        self, project_root: Path, paths: list[str] | None = None
    ) -> list[tuple[Path, int]]:
        search_paths = self._build_search_paths(project_root, paths)
        results: list[tuple[Path, int]] = []
        for sp in search_paths:
            for py_file in self._iter_python_files(sp):
                count = self._count_lines(py_file)
                if count is not None and count > 200:
                    results.append((py_file, count))
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _build_search_paths(
        self, project_root: Path, paths: list[str] | None
    ) -> list[Path]:
        if paths:
            resolved: list[Path] = []
            for p in paths:
                path = Path(p)
                if not path.is_absolute():
                    path = project_root / path
                if path.exists():
                    resolved.append(path)
            return resolved
        base = [project_root / "src"]
        t = project_root / "tools"
        e = project_root / "examples"
        if t.exists():
            base.append(t)
        if e.exists():
            base.append(e)
        return base

    def _iter_python_files(self, path: Path):
        if not path.exists():
            return []
        if path.is_file() and path.suffix == ".py":
            return [path]
        if path.is_dir():
            return [p for p in path.rglob("*.py") if "__pycache__" not in str(p)]
        return []

    def _count_lines(self, file_path: Path) -> int | None:
        try:
            with open(file_path, encoding="utf-8") as f:
                return sum(1 for _ in f)
        except Exception:
            return None

    def _build_header(
        self, quiet: bool, fix: bool, paths: list[str] | None
    ) -> list[str]:
        lines: list[str] = []
        lines.append("# Lint Report\n")
        lines.append("## Configuration\n\n")
        lines.append(f"- Quiet mode: {quiet}\n")
        lines.append(f"- Fix enabled: {fix}\n")
        lines.append(f"- Paths: {', '.join(paths) if paths else '.'}\n\n")
        return lines

    def _resolve_sections(
        self, project_root: Path, paths: list[str] | None
    ) -> list[tuple[str, Path]]:
        if paths:
            items: list[tuple[str, Path]] = []
            for p in paths:
                path = Path(p)
                if not path.is_absolute():
                    path = project_root / path
                items.append((p, path))
            return items
        return [
            ("src/", project_root / "src"),
            ("tools/", project_root / "tools"),
            ("examples/", project_root / "examples"),
        ]

    def _generate_lint_report(
        self,
        result: SubprocessResult,
        project_root: Path,
        paths: list[str] | None,
        fix: bool,
        quiet: bool,
    ) -> list[str]:
        """Generate the main lint report content."""
        lines = self._build_header(quiet, fix, paths)

        sections = self._resolve_sections(project_root, paths)

        outputs = []
        for title, path in sections:
            if path.exists():
                res = SubprocessExecutor().run(
                    ["ruff", "check", str(path)], cwd=project_root, quiet=True
                )
                outputs.append((title, res))

        issues_found = any(o[1].stdout.strip() for o in outputs)

        for title, exec_res in outputs:
            if exec_res.stdout.strip():
                lines.append(f"## Issues in {title}\n\n")
                lines.append("```\n")
                lines.append(exec_res.stdout)
                lines.append("```\n")
            if exec_res.stderr.strip():
                lines.append(f"## Errors in {title}\n\n")
                lines.append("```\n")
                lines.append(exec_res.stderr)
                lines.append("```\n")

        # Run pre-commit dry-run and add results to report
        lines.append("\n## Pre-commit Dry Run Results\n\n")
        precommit_result = self._run_precommit_dry_run(project_root, quiet)
        lines.append("```\n")
        lines.append(precommit_result)
        lines.append("```\n")

        # Run mypy and add results to report
        mypy_cmd = ["mypy"]
        # Use .wl/mypy.ini if it exists
        wl_mypy_config = project_root / ".wl/mypy.ini"
        if wl_mypy_config.exists():
            mypy_cmd.extend(["--config-file", str(wl_mypy_config)])
        mypy_cmd.extend(["src/", "tests/"])
        mypy_result = SubprocessExecutor().run(mypy_cmd, cwd=project_root, quiet=True)
        lines.append("\n## MyPy Results\n\n")
        if mypy_result.stdout:
            lines.append("```\n")
            lines.append(mypy_result.stdout)
            lines.append("```\n")
        else:
            lines.append("No MyPy issues found.\n")
        if mypy_result.stderr:
            lines.append("\n## MyPy Errors\n\n")
            lines.append("```\n")
            lines.append(mypy_result.stderr)
            lines.append("```\n")

        large_files = self._find_large_python_files(project_root, paths)

        if (
            not issues_found
            and not result.stdout
            and not large_files
            and not mypy_result.stdout
        ):
            lines.append("No lint issues found.\n")
        if result.stderr and not result.stdout:
            lines.append("\n## Errors\n\n")
            lines.append("```\n")
            lines.append(result.stderr)
            lines.append("```\n")

        return lines

    def _generate_error_report(self, project_root: Path) -> list[str]:
        """Generate the mypy error report content for src/ and tests/ directories."""
        error_lines = ["# MyPy Error Report\n\n"]

        # Run mypy on src/ and tests/ separately for detailed error reporting
        mypy_base_cmd = ["mypy"]
        # Use .wl/mypy.ini if it exists
        wl_mypy_config = project_root / ".wl/mypy.ini"
        if wl_mypy_config.exists():
            mypy_base_cmd.extend(["--config-file", str(wl_mypy_config)])

        src_mypy = SubprocessExecutor().run(
            mypy_base_cmd + ["src/"], cwd=project_root, quiet=True
        )
        tests_mypy = SubprocessExecutor().run(
            mypy_base_cmd + ["tests/"], cwd=project_root, quiet=True
        )

        # Add src/ results
        if src_mypy.stdout or src_mypy.stderr:
            error_lines.append("## MyPy Results for src/\n\n")
            error_lines.append("```\n")
            if src_mypy.stdout:
                error_lines.append(src_mypy.stdout)
            if src_mypy.stderr:
                error_lines.append(src_mypy.stderr)
            error_lines.append("```\n\n")

        # Add tests/ results
        if tests_mypy.stdout or tests_mypy.stderr:
            error_lines.append("## MyPy Results for tests/\n\n")
            error_lines.append("```\n")
            if tests_mypy.stdout:
                error_lines.append(tests_mypy.stdout)
            if tests_mypy.stderr:
                error_lines.append(tests_mypy.stderr)
            error_lines.append("```\n")

        return error_lines

    def _write_report_file(self, file_path: Path, content: list[str]) -> None:
        """Write report content to the specified file."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(content)

    def _generate_packaging_todo(
        self, large_files: list[tuple[Path, int]], project_root: Path, quiet: bool
    ) -> None:
        """
        生成用于打包模块化的待办事项报告
        """
        # Create todos directory in current working directory
        todos_dir = Path("todos")
        todos_dir.mkdir(exist_ok=True)

        packaging_report_file = todos_dir / "to_packaging_modularization.md"

        lines: list[str] = []
        lines.append("# To Packaging Modularization\n\n")
        lines.append("## Large Python Files (>200 lines)\n\n")
        lines.append(
            "These files are candidates for modularization due to their size.\n\n"
        )
        lines.append("| File Path | Line Count |\n")
        lines.append("|-----------|------------|\n")
        for file_path, line_count in large_files:
            # 将路径转换为相对于项目根目录的路径
            relative_path = file_path.relative_to(project_root)
            lines.append(f"| {relative_path} | {line_count} |\n")
        lines.append("\n")

        with open(packaging_report_file, "w", encoding="utf-8") as f:
            f.writelines(lines)

        if not quiet:
            log_info(
                f"Packaging todo list generated at {packaging_report_file}",
                f"打包模块化待办列表已生成到 {packaging_report_file}",
            )
