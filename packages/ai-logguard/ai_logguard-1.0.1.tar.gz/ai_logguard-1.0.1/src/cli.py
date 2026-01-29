"""
AI-LogGuard CLI - Modern CLI interface for CI/CD log analysis
Using GRU Deep Learning model (F1: 97.63%) + Multi-stage Pipeline Analyzer
"""
import sys
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
import json

from .parsers import parse_log
from .models import ParsedLog, BuildStatus, Platform
from .utils.display import display_parsed_log, display_summary
from .ml.log_analyzer import analyze_pipeline_log, ErrorLayer
from .ml.analysis_formatter import format_analysis
from .ml.ai_log_analyzer import AIProvider

# Create Typer app
app = typer.Typer(
    name="ai-logguard",
    help="🤖 AI-powered CLI for CI/CD log analysis using GRU Deep Learning (F1: 97.63%)",
    add_completion=False,
)

# Rich console for beautiful output
console = Console()


# ============================================================================
# Core Commands
# ============================================================================

@app.command()
def analyze(
    log_file: Optional[Path] = typer.Argument(
        None,
        help="Path to the CI/CD log file (if not provided, paste mode will start)",
    ),
    output_format: str = typer.Option(
        "rich",
        "--format",
        "-f",
        help="Output format: rich, json, markdown",
    ),
    show_full: bool = typer.Option(
        False,
        "--full",
        help="Show full analysis including all errors and warnings",
    ),
):
    """
    🔍 Analyze a CI/CD log file
    
    Parse and analyze logs from Jenkins, GitHub Actions, GitLab CI, etc.
    Uses GRU deep learning model for error classification.
    
    Examples:
        ai-logguard analyze build.log    # Analyze from file
        ai-logguard analyze              # Paste log directly
    """
    # Determine input source
    log_content = None
    job_name = "pasted_log"
    
    # Case 1: File provided
    if log_file is not None:
        if not log_file.exists():
            console.print(f"[red]❌ File not found: {log_file}[/red]")
            raise typer.Exit(code=1)
        console.print(f"\n[bold blue]🔍 Analyzing log file:[/bold blue] {log_file}\n")
        try:
            log_content = log_file.read_text(encoding='utf-8')
            job_name = log_file.stem
        except Exception as e:
            console.print(f"[red]❌ Error reading file: {e}[/red]")
            raise typer.Exit(code=1)
    
    # Case 2: No file - go directly to paste mode
    else:
        log_content, job_name = _interactive_log_input("analyze")
        if not log_content:
            raise typer.Exit(code=1)
    
    # Now analyze the log content
    _analyze_log_content(log_content, job_name, output_format, show_full)


def _get_pasted_log() -> Optional[str]:
    """Get log content from user paste input"""
    console.print("\n[bold blue]📋 AI-LogGuard - Paste Mode[/bold blue]")
    console.print("[dim]Paste your CI/CD log content below.[/dim]")
    console.print("[dim]Press Enter twice (empty line) to finish, or Ctrl+D.[/dim]")
    console.print("[yellow]" + "─" * 60 + "[/yellow]\n")
    
    lines = []
    empty_line_count = 0
    
    try:
        while True:
            try:
                line = input()
                if line == "":
                    empty_line_count += 1
                    if empty_line_count >= 2:
                        break
                    lines.append(line)
                else:
                    empty_line_count = 0
                    lines.append(line)
            except EOFError:
                break
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Input cancelled.[/yellow]\n")
        return None
    
    log_content = "\n".join(lines).strip()
    
    if not log_content:
        console.print("\n[yellow]⚠️ No log content provided.[/yellow]\n")
        return None
    
    console.print("\n[yellow]" + "─" * 60 + "[/yellow]")
    console.print(f"[green]✓ Received {len(lines)} lines of log content[/green]\n")
    
    return log_content


def _interactive_log_input(command: str) -> tuple:
    """Interactive mode - directly goes to paste mode"""
    console.print(f"\n[bold blue]🔍 AI-LogGuard - {command.title()} Mode[/bold blue]\n")
    
    # Go directly to paste mode
    log_content = _get_pasted_log()
    return log_content, "pasted_log"


def _analyze_log_content(log_content: str, job_name: str, output_format: str, show_full: bool):
    """Core analyze logic - separated from input handling"""
    
    # Parse log
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Parsing log...", total=None)
        
        try:
            parsed = parse_log(
                log_content,
                job_name=job_name,
            )
            progress.update(task, description="✅ Log parsed successfully")
        except Exception as e:
            console.print(f"[red]❌ Error parsing log: {e}[/red]")
            raise typer.Exit(code=1)
    
    console.print()
    
    # Display based on format
    if output_format == "json":
        console.print(json.dumps(parsed.model_dump(), indent=2, default=str))
    elif output_format == "markdown":
        _display_markdown(parsed)
    else:
        display_parsed_log(parsed, console=console, show_full=show_full)
    
    # Add Hybrid classification (Rule-based + GRU for better accuracy)
    try:
        from .ml.hybrid_classifier import HybridLogClassifier
        classifier = HybridLogClassifier()
        result = classifier.predict(log_content)
        
        if result.get('is_success', False):
            console.print(f"\n[bold green]✅ Classification: SUCCESS[/bold green]")
        else:
            confidence_color = "green" if result['confidence'] > 0.8 else "yellow" if result['confidence'] > 0.6 else "red"
            method_info = f" [{result.get('method', 'hybrid')}]" if result.get('method') else ""
            console.print(f"\n[bold]🧠 Classification:[/bold] [{confidence_color}]{result['category'].upper()}[/{confidence_color}] ({result['confidence']:.1%}){method_info}")
            
            # Show evidence if available
            if result.get('evidence'):
                console.print(f"[dim]Evidence: {result['evidence'][0][:100]}...[/dim]")
    except Exception as e:
        # Fallback to basic GRU if hybrid fails
        try:
            from .ml.gru_classifier import GRULogClassifier
            classifier = GRULogClassifier()
            result = classifier.predict(log_content)
            if not result.get('is_success', False):
                console.print(f"\n[bold]🧠 GRU Classification:[/bold] {result['category'].upper()} ({result['confidence']:.1%})")
        except:
            pass
    
    # Root Cause Analysis (integrated from diagnose command)
    console.print("\n" + "─" * 60)
    console.print("[bold]🎯 Root Cause Analysis[/bold]\n")
    
    try:
        analysis = analyze_pipeline_log(log_content)
        
        if analysis.root_causes:
            console.print(f"[dim]Found {len(analysis.root_causes)} root cause(s):[/dim]\n")
            
            for i, error in enumerate(analysis.root_causes, 1):
                layer_emoji = {
                    ErrorLayer.CI: "🏃",
                    ErrorLayer.BUILD: "📦",
                    ErrorLayer.CODE: "💻",
                    ErrorLayer.ENV: "🔧",
                    ErrorLayer.APP: "🧪",
                    ErrorLayer.INFRA: "☸️",
                    ErrorLayer.PLATFORM: "🏢",
                    ErrorLayer.DATA: "🗄️",
                    ErrorLayer.SECURITY: "🔒",
                }.get(error.layer, "❓")
                
                console.print(f"  {layer_emoji} [bold cyan]#{i}[/bold cyan] [{error.layer.value}] {error.error_type}")
                console.print(f"     [dim]{error.message[:100]}{'...' if len(error.message) > 100 else ''}[/dim]")
                if error.stage:
                    console.print(f"     [dim]Stage: {error.stage}[/dim]")
                console.print()
        else:
            # If no root causes from analyzer, extract from parsed errors
            if parsed.errors:
                console.print(f"[dim]Detected {len(parsed.errors)} error(s). Key issues:[/dim]\n")
                
                # Show top 3 most important errors
                for i, err in enumerate(parsed.errors[:3], 1):
                    console.print(f"  📦 [bold cyan]#{i}[/bold cyan] Line {err.line_number}")
                    console.print(f"     [dim]{err.message[:100]}{'...' if len(err.message) > 100 else ''}[/dim]")
                    console.print()
            else:
                console.print("[dim]No specific root causes identified.[/dim]")
                
    except Exception as e:
        # Fallback: show parsed errors as root causes
        if parsed.errors:
            console.print(f"[dim]Key errors detected:[/dim]\n")
            for i, err in enumerate(parsed.errors[:3], 1):
                console.print(f"  📦 [bold cyan]#{i}[/bold cyan] Line {err.line_number}: {err.message[:80]}...")
        else:
            console.print(f"[dim]Could not perform root cause analysis: {e}[/dim]")
    
    console.print()


@app.command()
def summarize(
    log_file: Optional[Path] = typer.Argument(
        None,
        help="Path to the CI/CD log file (if not provided, paste mode will start)",
    ),
):
    """
    📊 Generate a quick summary of a log file
    
    Show high-level statistics and key information.
    
    Examples:
        ai-logguard summarize build.log    # Summarize from file
        ai-logguard summarize              # Paste log directly
    """
    # Determine input source
    log_content = None
    job_name = "pasted_log"
    
    # Case 1: File provided
    if log_file is not None:
        if not log_file.exists():
            console.print(f"[red]❌ File not found: {log_file}[/red]")
            raise typer.Exit(code=1)
        console.print(f"\n[bold blue]📊 Summarizing log file:[/bold blue] {log_file}\n")
        try:
            log_content = log_file.read_text(encoding='utf-8')
            job_name = log_file.stem
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
            raise typer.Exit(code=1)
    
    # Case 2: No file - go directly to paste mode
    else:
        log_content, job_name = _interactive_log_input("summarize")
        if not log_content:
            raise typer.Exit(code=1)
    
    # Parse and display summary
    try:
        parsed = parse_log(log_content, job_name=job_name)
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        raise typer.Exit(code=1)
    
    display_summary(parsed, console=console)
    console.print()


@app.command()
def guide(
    command: Optional[str] = typer.Argument(
        None,
        help="Command name to get detailed usage (analyze, summarize, version)",
    ),
):
    """
    📖 AI-LogGuard CLI Usage Guide
    
    Show detailed usage for each command with examples.
    
    Examples:
        ai-logguard guide              # Overview of all commands
        ai-logguard guide analyze      # Detailed guide for analyze command
        ai-logguard guide summarize    # Detailed guide for summarize command
    """
    
    # Command details
    commands_info = {
        'analyze': {
            'title': '🔍 ANALYZE - CI/CD Log Analysis',
            'description': 'Detailed log analysis with root cause detection and error classification.',
            'usage': [
                'ai-logguard analyze <file>',
                'ai-logguard analyze',
            ],
            'examples': [
                ('Analyze from file', 'ai-logguard analyze build.log'),
                ('Paste log directly', 'ai-logguard analyze'),
            ],
            'options': [
                ('--json, -j', 'Output results as JSON'),
                ('--full, -f', 'Show all errors and warnings'),
            ],
            'output': [
                '📊 Statistics (lines, errors, warnings)',
                '❌ Error list with line numbers',
                '⚠️ Warning list',
                '🧠 ML Classification (GRU model)',
                '🎯 Root Cause Analysis',
            ],
            'paste_guide': [
                '1. Run: ai-logguard analyze',
                '2. Copy your CI/CD log content',
                '3. Paste into terminal (Cmd+V on macOS, Ctrl+Shift+V on Linux)',
                '4. Press Enter twice (empty line) to finish input',
                '5. Or press Ctrl+D to submit immediately',
            ],
        },
        'summarize': {
            'title': '📊 SUMMARIZE - Quick Log Summary',
            'description': 'Display high-level statistics of a log file.',
            'usage': [
                'ai-logguard summarize <file>',
                'ai-logguard summarize',
            ],
            'examples': [
                ('Summarize from file', 'ai-logguard summarize jenkins.log'),
                ('Paste log directly', 'ai-logguard summarize'),
            ],
            'options': [],
            'output': [
                '📈 Platform detection (Jenkins/GitLab/GitHub)',
                '📊 Line counts and statistics',
                '🔢 Error and warning counts',
            ],
            'paste_guide': [
                '1. Run: ai-logguard summarize',
                '2. Copy your CI/CD log content',
                '3. Paste into terminal',
                '4. Press Enter twice or Ctrl+D to finish',
            ],
        },
        'version': {
            'title': '📦 VERSION - Version Information',
            'description': 'Display version and information about AI-LogGuard.',
            'usage': [
                'ai-logguard version',
                'ai-logguard version --verbose',
            ],
            'examples': [
                ('Show version', 'ai-logguard version'),
                ('Show details', 'ai-logguard version --verbose'),
            ],
            'options': [
                ('--verbose, -v', 'Show detailed features and model status'),
            ],
            'output': [
                '📦 Version number',
                '✅ Feature list (with --verbose)',
                '🧠 Model status (with --verbose)',
            ],
            'paste_guide': [],
        },
        'guide': {
            'title': '📖 GUIDE - Usage Guide',
            'description': 'Display detailed usage guide for each command.',
            'usage': [
                'ai-logguard guide',
                'ai-logguard guide <command>',
            ],
            'examples': [
                ('Show overview', 'ai-logguard guide'),
                ('Analyze details', 'ai-logguard guide analyze'),
            ],
            'options': [],
            'output': [
                '📖 Usage examples',
                '⚙️ Available options',
            ],
            'paste_guide': [],
        },
    }
    
    if command:
        # Show specific command details
        cmd_lower = command.lower()
        if cmd_lower not in commands_info:
            console.print(f"[red]❌ Command '{command}' does not exist.[/red]")
            console.print(f"[dim]Available: {', '.join(commands_info.keys())}[/dim]")
            raise typer.Exit(1)
        
        info = commands_info[cmd_lower]
        
        console.print(f"\n[bold blue]{info['title']}[/bold blue]")
        console.print(f"[dim]{info['description']}[/dim]\n")
        
        # Usage
        console.print("[bold]📝 Usage:[/bold]")
        for usage in info['usage']:
            console.print(f"  [cyan]{usage}[/cyan]")
        
        # Examples
        console.print("\n[bold]💡 Examples:[/bold]")
        for desc, example in info['examples']:
            console.print(f"  [dim]{desc}:[/dim]")
            console.print(f"    [green]$ {example}[/green]")
        
        # Paste Guide (if available)
        if info.get('paste_guide'):
            console.print("\n[bold]📋 How to Paste Log:[/bold]")
            for step in info['paste_guide']:
                console.print(f"  {step}")
        
        # Options
        if info['options']:
            console.print("\n[bold]⚙️ Options:[/bold]")
            table = Table(show_header=True, header_style="bold")
            table.add_column("Option", style="cyan")
            table.add_column("Description")
            for opt, desc in info['options']:
                table.add_row(opt, desc)
            console.print(table)
        
        # Output
        console.print("\n[bold]📤 Output:[/bold]")
        for item in info['output']:
            console.print(f"  • {item}")
        
        console.print()
    else:
        # Show overview of all commands
        console.print("\n[bold blue]📖 AI-LogGuard CLI - Usage Guide[/bold blue]")
        console.print("[dim]AI-powered CI/CD log analysis tool[/dim]\n")
        
        console.print("[bold]🚀 Quick Start:[/bold]")
        console.print("  [green]$ ai-logguard analyze build.log[/green]  # Analyze from file")
        console.print("  [green]$ ai-logguard analyze[/green]            # Paste log directly\n")
        
        console.print("[bold]📋 All Commands:[/bold]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Command", style="green", width=12)
        table.add_column("Description")
        table.add_column("Example", style="dim")
        
        table.add_row(
            "analyze",
            "Detailed log analysis with root cause detection",
            "ai-logguard analyze build.log"
        )
        table.add_row(
            "summarize",
            "Quick statistics summary of log",
            "ai-logguard summarize jenkins.log"
        )
        table.add_row(
            "version",
            "Show version and information",
            "ai-logguard version -v"
        )
        table.add_row(
            "guide",
            "CLI usage guide",
            "ai-logguard guide analyze"
        )
        
        console.print(table)
        
        console.print("\n[bold]📋 How to Paste Log:[/bold]")
        console.print("  1. Run [cyan]ai-logguard analyze[/cyan] (no arguments)")
        console.print("  2. Copy your CI/CD log content from browser/terminal")
        console.print("  3. Paste into terminal ([cyan]Cmd+V[/cyan] on macOS, [cyan]Ctrl+Shift+V[/cyan] on Linux)")
        console.print("  4. Press [cyan]Enter twice[/cyan] (empty line) to submit")
        console.print("  5. Or press [cyan]Ctrl+D[/cyan] to submit immediately")
        
        console.print("\n[bold]💡 Tips:[/bold]")
        console.print("  • Use [cyan]--help[/cyan] after any command to see options")
        console.print("  • Use [cyan]ai-logguard guide <command>[/cyan] for detailed usage")
        console.print("  • Supports GitLab CI, Jenkins, GitHub Actions logs")
        
        console.print("\n[bold]📚 Detailed Command Guides:[/bold]")
        console.print("  [green]$ ai-logguard guide analyze[/green]")
        console.print("  [green]$ ai-logguard guide summarize[/green]")
        console.print()


@app.command()
def version(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed version information",
    )
):
    """📦 Show version information"""
    console.print("\n[bold blue]AI-LogGuard[/bold blue] v1.0.0")
    console.print("AI-powered CI/CD log analysis tool\n")
    
    if verbose:
        console.print("[bold]Features:[/bold]")
        console.print("  [green]✅[/green] Jenkins & GitHub Actions parsing")
        console.print("  [green]✅[/green] Error detection and categorization")
        console.print("  [green]✅[/green] GRU Deep Learning classification (F1: 97.63%)")
        console.print("  [green]✅[/green] Intelligent fix suggestions")
        console.print("  [green]✅[/green] 9 error categories supported")
        console.print()
        
        # Check model availability
        try:
            from .ml.gru_classifier import GRULogClassifier
            classifier = GRULogClassifier()
            console.print("[bold]Model Status:[/bold]")
            console.print("  [green]✅[/green] GRU model loaded successfully")
            console.print("  [dim]Path: models/deep_learning/gru.pt[/dim]")
        except:
            console.print("[bold]Model Status:[/bold]")
            console.print("  [red]❌[/red] Model not found")
            console.print("  [yellow]Run training notebooks first[/yellow]")
        
        console.print()


def _display_markdown(parsed: ParsedLog):
    """Display parsed log as Markdown"""
    md_lines = [
        f"# Log Analysis Report",
        f"",
        f"**Platform:** {parsed.platform}",
        f"**Job:** {parsed.job_name or 'Unknown'}",
        f"**Status:** {parsed.status}",
        f"**Build Number:** {parsed.build_number or 'N/A'}",
        f"",
        f"## Statistics",
        f"- Total Lines: {parsed.total_lines}",
        f"- Errors: {parsed.error_count}",
        f"- Warnings: {parsed.warning_count}",
        f"",
    ]
    
    if parsed.stages:
        md_lines.append("## Stages")
        for stage in parsed.stages:
            md_lines.append(f"- **{stage.name}**: {stage.status}")
    
    if parsed.errors:
        md_lines.append("\n## Top Errors")
        for error in parsed.errors[:5]:
            md_lines.append(f"- Line {error.line_number}: {error.message}")
    
    md_text = "\n".join(md_lines)
    console.print(Markdown(md_text))


def main():
    """Entry point for the CLI"""
    app()


if __name__ == "__main__":
    main()
