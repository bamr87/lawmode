"""CLI interface for LawMode."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from lawmode.core import LawModeAgent
from lawmode.config import LawModeConfig
from lawmode.models import Severity


console = Console()


@click.command()
@click.argument("target", type=click.Path(exists=True), required=False)
@click.option(
    "--diff",
    type=str,
    help="Git commit range to analyze (e.g., HEAD~1 or commit1..commit2)",
)
@click.option(
    "--jurisdiction",
    "-j",
    multiple=True,
    help="Jurisdictions to check (e.g., US-CA, EU, UK)",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to policy.yaml config file",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output directory for artifacts (default: .lawmode)",
)
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--json", is_flag=True, help="Output results as JSON")
def main(
    target: Optional[str],
    diff: Optional[str],
    jurisdiction: tuple,
    config: Optional[str],
    output: Optional[str],
    verbose: bool,
    json: bool,
):
    """LawMode.ai - Always-on AI lawyer for developers.
    
    Scan code for legal compliance issues.
    
    Examples:
    
        lawmode scan ./src
    
        lawmode scan --diff HEAD~1
    
        lawmode scan --jurisdiction US-CA EU
    """
    try:
        # Load configuration
        config_path = Path(config) if config else None
        lawmode_config = LawModeConfig.from_file(config_path)
        
        # Override jurisdictions if provided
        if jurisdiction:
            lawmode_config.policy.jurisdictions = list(jurisdiction)
        
        # Override output directory if provided
        if output:
            lawmode_config.artifact_dir = Path(output)
        
        # Initialize agent
        agent = LawModeAgent(lawmode_config)
        
        # Get code to analyze
        code_to_analyze = ""
        file_path = None
        
        if diff:
            # Analyze git diff
            code_to_analyze = _get_git_diff(diff)
            if not code_to_analyze:
                console.print(f"[red]Error:[/red] No changes found in diff {diff}")
                sys.exit(1)
        elif target:
            # Analyze file or directory
            target_path = Path(target)
            if target_path.is_file():
                code_to_analyze = target_path.read_text()
                file_path = str(target_path)
            elif target_path.is_dir():
                # Collect all code files
                code_files = _collect_code_files(target_path)
                code_to_analyze = "\n\n".join(
                    f"// {path}\n{path.read_text()}" for path in code_files
                )
            else:
                console.print(f"[red]Error:[/red] Invalid target: {target}")
                sys.exit(1)
        else:
            # Try to analyze current directory
            code_to_analyze = _get_git_diff("HEAD")
            if not code_to_analyze:
                console.print("[yellow]Warning:[/yellow] No git changes found. Analyzing current directory...")
                code_to_analyze = _collect_code_from_dir(Path("."))
        
        if not code_to_analyze:
            console.print("[red]Error:[/red] No code found to analyze")
            sys.exit(1)
        
        # Run review
        if verbose:
            console.print("[cyan]Running legal review...[/cyan]")
        
        review = agent.review_code(code_to_analyze, file_path=file_path)
        
        # Generate artifacts
        artifacts = agent.generate_artifacts(review)
        
        # Display results
        if json:
            import json
            console.print(json.dumps(review.model_dump(mode="json"), indent=2, default=str))
        else:
            _display_results(review, artifacts, verbose)
        
        # Exit with error code if critical risks found
        if review.has_critical_risks():
            sys.exit(1)
        elif review.has_blocking_risks(lawmode_config.policy.severity_gating):
            sys.exit(1)
    
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


def _get_git_diff(diff_spec: str) -> str:
    """Get git diff for a commit range."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "diff", diff_spec],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout
    except Exception:
        return ""


def _collect_code_files(directory: Path) -> list[Path]:
    """Collect code files from directory."""
    code_extensions = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs", ".cpp", ".c",
        ".h", ".hpp", ".cs", ".php", ".rb", ".swift", ".kt", ".scala", ".html",
        ".css", ".vue", ".svelte", ".sql", ".sh", ".yaml", ".yml", ".json",
    }
    
    files = []
    for ext in code_extensions:
        files.extend(directory.rglob(f"*{ext}"))
    
    # Filter out common ignore patterns
    ignore_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", ".lawmode"}
    files = [f for f in files if not any(ignore in f.parts for ignore in ignore_dirs)]
    
    return files[:100]  # Limit to 100 files for performance


def _collect_code_from_dir(directory: Path) -> str:
    """Collect code from directory."""
    files = _collect_code_files(directory)
    return "\n\n".join(f"// {path}\n{path.read_text()}" for path in files)


def _display_results(review, artifacts, verbose: bool):
    """Display review results in a formatted way."""
    console.print("\n")
    console.print(Panel.fit("[bold cyan]LawMode.ai Legal Review[/bold cyan]", border_style="cyan"))
    console.print("\n")
    
    # Summary
    summary_table = Table(title="Review Summary", show_header=True, header_style="bold magenta")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green")
    
    summary_table.add_row("Review ID", str(review.review_id))
    summary_table.add_row("Timestamp", review.timestamp.isoformat())
    summary_table.add_row("Jurisdictions", ", ".join(review.jurisdictions) if review.jurisdictions else "None")
    summary_table.add_row("Domain", review.domain or "Not detected")
    summary_table.add_row("Total Risks", str(len(review.risks)))
    summary_table.add_row("Critical", str(sum(1 for r in review.risks if r.severity == Severity.CRITICAL)))
    summary_table.add_row("High", str(sum(1 for r in review.risks if r.severity == Severity.HIGH)))
    summary_table.add_row("Medium", str(sum(1 for r in review.risks if r.severity == Severity.MEDIUM)))
    summary_table.add_row("Low", str(sum(1 for r in review.risks if r.severity == Severity.LOW)))
    
    console.print(summary_table)
    console.print("\n")
    
    # Risks table
    if review.risks:
        risks_table = Table(title="Identified Risks", show_header=True, header_style="bold red")
        risks_table.add_column("ID", style="cyan")
        risks_table.add_column("Severity", style="bold")
        risks_table.add_column("Title", style="yellow")
        risks_table.add_column("Law", style="blue")
        risks_table.add_column("File", style="dim")
        
        for risk in review.risks:
            severity_color = {
                Severity.CRITICAL: "red",
                Severity.HIGH: "yellow",
                Severity.MEDIUM: "blue",
                Severity.LOW: "green",
            }.get(risk.severity, "white")
            
            risks_table.add_row(
                risk.id,
                f"[{severity_color}]{risk.severity.value}[/{severity_color}]",
                risk.title,
                risk.law,
                risk.file_path or "",
            )
        
        console.print(risks_table)
        console.print("\n")
        
        # Show detailed risk information
        if verbose:
            for risk in review.risks:
                console.print(Panel(
                    f"[bold]{risk.title}[/bold]\n\n"
                    f"[cyan]Severity:[/cyan] {risk.severity.value}\n"
                    f"[cyan]Law:[/cyan] {risk.law}\n"
                    f"[cyan]Description:[/cyan] {risk.description}\n"
                    f"[cyan]Mitigation:[/cyan] {risk.mitigation}\n"
                    + (f"[cyan]Citation:[/cyan] {risk.citation}\n" if risk.citation else ""),
                    title=f"Risk {risk.id}",
                    border_style="yellow" if risk.severity == Severity.CRITICAL else "blue",
                ))
                console.print("\n")
    else:
        console.print("[green]✓[/green] No legal risks identified.\n")
    
    # Artifacts
    console.print(Panel(
        "[bold]Generated Artifacts:[/bold]\n\n" + "\n".join(f"  • {path}" for path in artifacts.values()),
        title="Artifacts",
        border_style="green",
    ))
    console.print("\n")
    
    # Disclaimer
    console.print(Panel(
        "[yellow]⚠️  NOT LEGAL ADVICE[/yellow]\n\n"
        "LawMode.ai provides automated legal compliance analysis for informational purposes only. "
        "This does not constitute legal advice. Consult qualified legal counsel for legal matters.",
        border_style="yellow",
    ))

