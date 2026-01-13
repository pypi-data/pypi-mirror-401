"""
XSource Security CLI - Main Entry Point

AI Agent Security Scanner & Benchmark Tool
"""

import typer
from typing import Optional
from rich.panel import Panel
from rich import box

from . import __version__
from .auth import app as auth_app
from .scan import app as scan_app, report_app
from .bench import app as bench_app
from .config import get_config, Config, CONFIG_FILE
from .utils import (
    console,
    print_banner,
    print_success,
    print_error,
    print_info,
    BRAND_GREEN,
    BRAND_PURPLE,
)

# Create main app
app = typer.Typer(
    name="xsource",
    help="XSource Security CLI - AI Agent Security Scanner & Benchmark Tool",
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_show_locals=False,
)

# Add subcommands
app.add_typer(auth_app, name="auth", help="Authentication commands")
app.add_typer(scan_app, name="scan", help="Security scanning (AgentAudit)")
app.add_typer(report_app, name="report", help="View and export scan reports")
app.add_typer(bench_app, name="bench", help="Benchmarking (AgentBench)")


# =========================================================================
# Top-level commands
# =========================================================================

@app.command("login")
def login_shortcut(
    email: Optional[str] = typer.Option(None, "--email", "-e", help="Email address"),
    password: Optional[str] = typer.Option(None, "--password", "-p", help="Password"),
):
    """
    Login to XSource Security (shortcut for 'xsource auth login').
    """
    from .auth import login
    login(email=email, password=password)


@app.command("config")
def config_cmd(
    show: bool = typer.Option(False, "--show", "-s", help="Show current configuration"),
    api_url: Optional[str] = typer.Option(None, "--api-url", help="Set API URL"),
    timeout: Optional[int] = typer.Option(None, "--timeout", help="Set request timeout (seconds)"),
    reset: bool = typer.Option(False, "--reset", help="Reset to default configuration"),
):
    """
    Manage CLI configuration.

    Examples:
        xsource config --show
        xsource config --api-url https://api.xsourcesec.com
        xsource config --timeout 120
        xsource config --reset
    """
    config = get_config()

    if reset:
        config = Config()
        config.save()
        print_success("Configuration reset to defaults")
        show = True

    if api_url:
        config.api_url = api_url
        config.save()
        print_success(f"API URL set to: {api_url}")

    if timeout is not None:
        config.timeout = timeout
        config.save()
        print_success(f"Timeout set to: {timeout}s")

    if show or (not api_url and timeout is None and not reset):
        content = []
        content.append(f"[bold]API URL:[/bold] {config.api_url}")
        content.append(f"[bold]Timeout:[/bold] {config.timeout}s")
        content.append(f"[bold]Output Format:[/bold] {config.output_format}")
        content.append(f"[bold]Colors:[/bold] {'enabled' if config.color else 'disabled'}")
        content.append("")
        content.append(f"[dim]Config file: {CONFIG_FILE}[/dim]")

        panel = Panel(
            "\n".join(content),
            title="[bold]Configuration[/bold]",
            border_style="dim",
            box=box.ROUNDED,
        )
        console.print(panel)


@app.command("version")
def version():
    """
    Show version information.
    """
    console.print(f"[bold {BRAND_GREEN}]XSource CLI[/bold {BRAND_GREEN}] version [bold]{__version__}[/bold]")
    console.print(f"[dim]https://xsourcesec.com[/dim]")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version_flag: bool = typer.Option(False, "--version", "-v", help="Show version and exit"),
):
    """
    [bold green]XSource Security CLI[/bold green]

    AI Agent Security Scanner & Benchmark Tool

    [bold]Quick Start:[/bold]
        xsource login                         # Authenticate
        xsource scan https://api.example.com  # Run security scan
        xsource bench list                    # List benchmark scenarios

    [bold]Documentation:[/bold]
        https://docs.xsourcesec.com/cli

    [bold]Support:[/bold]
        support@xsourcesec.com
    """
    if version_flag:
        version()
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        print_banner()
        console.print(ctx.get_help())


# =========================================================================
# Quick command aliases
# =========================================================================

@app.command("status", hidden=True)
def status_alias():
    """Check authentication status (alias for 'xsource auth status')."""
    from .auth import status
    status()


@app.command("whoami", hidden=True)
def whoami_alias():
    """Show current user (alias for 'xsource auth whoami')."""
    from .auth import whoami
    whoami()


# =========================================================================
# Entry point
# =========================================================================

def main_entry():
    """Main entry point for the CLI."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted[/dim]")
        raise typer.Exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    main_entry()
