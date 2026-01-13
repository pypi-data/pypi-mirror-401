"""
CLI interface for typo-shield.

Main command: typo-shield scan
"""

from __future__ import annotations

import sys
from pathlib import Path

import typer
from typing_extensions import Annotated

from typo_shield import __version__
from typo_shield.config import load_config, merge_config_with_cli_args
from typo_shield.correlator import (
    analyze_new_deps,
    collect_declared_deps,
    correlate_imports_and_deps,
)
from typo_shield.diff import filter_files_by_extension, filter_files_by_pattern, parse_unified_diff
from typo_shield.git import GitError, get_range_diff, get_repo_root, get_staged_diff
from typo_shield.report import render_json_report, render_result_line, render_text_report
from typo_shield.risk import RiskFinding, get_exit_code
from typo_shield.risk.typosquat import check_multiple_packages
from typo_shield.scanners.deps_pyproject import scan_pyproject
from typo_shield.scanners.deps_requirements import scan_requirements
from typo_shield.scanners.python_imports import scan_python_imports

# Exit codes
EXIT_SUCCESS = 0
EXIT_FINDINGS = 1
EXIT_ERROR = 2


def _run_scan_pipeline(
    staged: bool,
    diff_range: str | None,
    repo_root: Path | None,
    config_path: Path | None,
    output_format: str,
    cli_strict_imports: bool,
    cli_fail_on: str,
    cli_exclude: list[str],
) -> int:
    """
    Run the main scanning pipeline.

    Returns:
        Exit code (0 for success, 1 for findings, 2 for error)
    """
    try:
        # Step 1: Load configuration
        config = load_config(config_path)
        config = merge_config_with_cli_args(
            config,
            cli_fail_on=cli_fail_on,
            cli_strict_imports=cli_strict_imports,
            cli_exclude=cli_exclude,
        )

        # Step 2: Determine repository root
        try:
            if repo_root is None:
                repo_root = get_repo_root()
            else:
                # Validate provided path is a git repo
                repo_root = get_repo_root(repo_root)
        except GitError as e:
            typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
            return EXIT_ERROR

        # Step 3: Get git diff
        try:
            if staged:
                diff_text = get_staged_diff(repo_root)
            else:
                # Parse diff range (e.g., "main...feature" or "main..HEAD")
                if "..." in diff_range:
                    base, head = diff_range.split("...", 1)
                elif ".." in diff_range:
                    base, head = diff_range.split("..", 1)
                else:
                    typer.secho(
                        f"Error: Invalid diff range format: '{diff_range}'",
                        fg=typer.colors.RED,
                        err=True,
                    )
                    return EXIT_ERROR

                diff_text = get_range_diff(repo_root, base, head)
        except GitError as e:
            typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
            return EXIT_ERROR

        # Step 4: Parse diff
        file_changes = parse_unified_diff(diff_text)

        # Apply exclusion patterns
        file_changes = filter_files_by_pattern(file_changes, config.exclude_paths)

        # Step 5: Scan Python files for imports
        python_files = filter_files_by_extension(file_changes, [".py"])
        all_imports: list[RiskFinding] = []

        for file_change in python_files:
            imports = scan_python_imports(file_change, repo_root)
            all_imports.extend(imports)

        # Step 6: Scan dependency files
        new_deps = []

        # Scan requirements.txt files
        req_files = [fc for fc in file_changes if fc.path.endswith("requirements.txt") or "requirements" in fc.path and fc.path.endswith(".txt")]
        for file_change in req_files:
            deps = scan_requirements(file_change)
            new_deps.extend(deps)

        # Scan pyproject.toml files
        toml_files = [fc for fc in file_changes if fc.path.endswith("pyproject.toml")]
        for file_change in toml_files:
            deps = scan_pyproject(file_change, repo_root)
            new_deps.extend(deps)

        # Step 7: Collect all declared dependencies from project
        # (Full scan, not just diff)
        all_declared_deps = _collect_project_dependencies(repo_root)

        # Step 8: Correlate imports with dependencies
        correlation_findings = correlate_imports_and_deps(
            all_imports,
            all_declared_deps,
            repo_root,
        )

        # Step 9: Analyze new dependencies
        new_dep_findings = analyze_new_deps(new_deps)

        # Step 10: Check for typosquatting in new dependencies
        new_dep_names = [dep.name for dep in new_deps]
        # Filter out allowed deps
        new_dep_names = [name for name in new_dep_names if name not in config.allow_deps]
        typosquat_findings = check_multiple_packages(new_dep_names)

        # Step 11: Aggregate all findings
        all_findings = []
        all_findings.extend(correlation_findings)
        all_findings.extend(new_dep_findings)
        all_findings.extend(typosquat_findings)

        # Filter findings based on allow lists
        all_findings = _filter_allowed_findings(all_findings, config)

        # Step 12: Render report
        use_colors = output_format == "text" and sys.stdout.isatty()

        if output_format == "json":
            report = render_json_report(all_findings)
            typer.echo(report)
        else:
            # Text format
            report = render_text_report(all_findings, show_info=True, use_colors=use_colors)
            typer.echo(report)

            # Add result line
            result_line = render_result_line(all_findings, config.fail_on, use_colors=use_colors)
            typer.echo(result_line)

        # Step 13: Determine exit code
        exit_code = get_exit_code(all_findings, config.fail_on)
        return exit_code

    except Exception as e:
        # Catch-all for unexpected errors
        typer.secho(
            f"Error: Unexpected error during scan: {e}",
            fg=typer.colors.RED,
            err=True,
        )
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        return EXIT_ERROR


def _collect_project_dependencies(repo_root: Path) -> set[str]:
    """
    Collect all declared dependencies from the project.

    Scans requirements.txt and pyproject.toml files in the entire project.

    Returns:
        Set of normalized dependency names
    """
    from typo_shield.diff import DiffFileChange

    all_deps = []

    # Find all requirements.txt files
    for req_file in repo_root.rglob("requirements*.txt"):
        if ".venv" in str(req_file) or "venv" in str(req_file):
            continue

        try:
            # Create a fake DiffFileChange with all lines
            lines = req_file.read_text(encoding="utf-8").splitlines()
            added_lines = [(i + 1, line) for i, line in enumerate(lines)]

            file_change = DiffFileChange(
                path=str(req_file.relative_to(repo_root)),
                added_lines=added_lines,
            )

            deps = scan_requirements(file_change)
            all_deps.extend(deps)
        except Exception:
            # Skip files that can't be read
            pass

    # Find all pyproject.toml files
    for toml_file in repo_root.rglob("pyproject.toml"):
        if ".venv" in str(toml_file) or "venv" in str(toml_file):
            continue

        try:
            # Create a fake DiffFileChange with all lines
            lines = toml_file.read_text(encoding="utf-8").splitlines()
            added_lines = [(i + 1, line) for i, line in enumerate(lines)]

            file_change = DiffFileChange(
                path=str(toml_file.relative_to(repo_root)),
                added_lines=added_lines,
            )

            deps = scan_pyproject(file_change, repo_root)
            all_deps.extend(deps)
        except Exception:
            # Skip files that can't be read
            pass

    # Return set of normalized names
    return collect_declared_deps(all_deps)


def _filter_allowed_findings(
    findings: list[RiskFinding],
    config,
) -> list[RiskFinding]:
    """
    Filter findings based on allow lists in configuration.

    Args:
        findings: List of findings
        config: Configuration object

    Returns:
        Filtered list of findings
    """
    filtered = []

    for finding in findings:
        # Skip if in allow_deps list
        if finding.subject == "dep" and finding.name in config.allow_deps:
            continue

        # Skip if in allow_modules list
        if finding.subject == "import" and finding.name in config.allow_modules:
            continue

        filtered.append(finding)

    return filtered


# Create Typer app
app = typer.Typer(
    name="typo-shield",
    help="Security guard against typosquatting in Python dependencies",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        typer.echo(f"typo-shield version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-v",
            help="Show version and exit",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """typo-shield: Security guard against typosquatting in Python dependencies."""
    pass


@app.command()
def scan(
    staged: Annotated[
        bool,
        typer.Option(
            "--staged/--no-staged",
            help="Scan staged changes (default) or use --diff-range",
        ),
    ] = True,
    diff_range: Annotated[
        str | None,
        typer.Option(
            "--diff-range",
            help="Git diff range (e.g., main...feature). Mutually exclusive with --staged",
        ),
    ] = None,
    repo_root: Annotated[
        Path | None,
        typer.Option(
            "--repo-root",
            help="Repository root path (default: auto-detect)",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = None,
    config: Annotated[
        Path | None,
        typer.Option(
            "--config",
            help="Configuration file path",
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
        ),
    ] = None,
    format: Annotated[
        str,
        typer.Option(
            "--format",
            help="Output format",
            case_sensitive=False,
        ),
    ] = "text",
    strict_imports: Annotated[
        bool,
        typer.Option(
            "--strict-imports",
            help="Fail on unknown imports (not in stdlib or dependencies)",
        ),
    ] = False,
    fail_on: Annotated[
        str,
        typer.Option(
            "--fail-on",
            help="Fail threshold: 'warn' or 'fail'",
            case_sensitive=False,
        ),
    ] = "fail",
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            "--exclude",
            help="Exclude file patterns (glob, can be used multiple times)",
        ),
    ] = None,
) -> None:
    """
    Scan git diff for suspicious dependencies and imports.

    By default, scans staged changes (--staged). Use --diff-range for custom ranges.

    Examples:
        typo-shield scan                              # Scan staged changes
        typo-shield scan --diff-range main...feature  # Scan commit range
        typo-shield scan --format json                # JSON output
        typo-shield scan --strict-imports             # Fail on unknown imports
        typo-shield scan --fail-on warn               # Fail on warnings too
    """
    # Validate mutual exclusivity
    if not staged and diff_range is None:
        typer.secho(
            "Error: When using --no-staged, you must specify --diff-range",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_ERROR)

    if staged and diff_range is not None:
        typer.secho(
            "Error: --staged and --diff-range are mutually exclusive",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_ERROR)

    # Validate format
    if format.lower() not in ["text", "json"]:
        typer.secho(
            f"Error: Invalid format '{format}'. Must be 'text' or 'json'",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_ERROR)

    # Validate fail_on
    if fail_on.lower() not in ["warn", "fail"]:
        typer.secho(
            f"Error: Invalid --fail-on value '{fail_on}'. Must be 'warn' or 'fail'",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_ERROR)

    # Run the scan pipeline
    exit_code = _run_scan_pipeline(
        staged=staged,
        diff_range=diff_range,
        repo_root=repo_root,
        config_path=config,
        output_format=format.lower(),
        cli_strict_imports=strict_imports,
        cli_fail_on=fail_on.lower(),
        cli_exclude=exclude or [],
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    app()

