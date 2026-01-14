"""Nova Agent CLI."""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
import webbrowser

import structlog
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from nova_agent import __version__
from nova_agent.config import get_config_manager
from nova_agent.settings import get_settings, set_verbose

logger = structlog.get_logger(__name__)
console = Console()


def _is_pipx_installed() -> bool:
    """Check if nova-agent was installed via pipx."""
    from pathlib import Path

    # pipx uses different paths on different systems
    pipx_paths = [
        Path.home() / ".local" / "share" / "pipx" / "venvs" / "nova-agent",  # Linux/macOS standard
        Path.home() / ".local" / "pipx" / "venvs" / "nova-agent",  # Alternative location
    ]
    return any(p.exists() for p in pipx_paths)


def _do_update() -> bool:
    """Perform the actual update.

    Returns:
        True if update succeeded, False otherwise
    """
    if _is_pipx_installed():
        cmd = ["pipx", "upgrade", "nova-agent"]
    else:
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "nova-agent"]

    console.print(f"[dim]Running: {' '.join(cmd)}[/dim]")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def _parse_version(version: str) -> tuple[int, ...]:
    """Convert version string to comparable tuple."""
    return tuple(int(x) for x in version.split("."))


def _check_for_updates() -> None:
    """Check PyPI for latest version and prompt for update."""
    try:
        import urllib.request

        url = "https://pypi.org/pypi/nova-agent/json"
        with urllib.request.urlopen(url, timeout=3) as response:
            import json

            data = json.loads(response.read().decode())
            latest_version = data["info"]["version"]

            # Only notify if latest version is higher than current
            if _parse_version(latest_version) > _parse_version(__version__):
                console.print(
                    f"[yellow]New version available: {__version__} → {latest_version}[/yellow]"
                )
                if typer.confirm("Update now?", default=True):
                    _do_update()
                    console.print(
                        "[green]Update complete! Please restart.[/green]"
                    )
                    raise typer.Exit(0)
                console.print()
    except typer.Exit:
        raise
    except Exception:
        # Ignore network errors (update check failure should not block execution)
        pass


def _ensure_browser_installed() -> bool:
    """Ensure Playwright browser (Chromium) is installed.

    Skips quickly if already installed.

    Returns:
        True if browser is ready, False if installation failed
    """
    try:
        console.print(
            "[dim]Checking browser... "
            "(first run may take 1-3 minutes to download)[/dim]"
        )
        # Force IPv4 to avoid IPv6 timeout issues on servers
        # Set in os.environ so all child processes inherit it
        os.environ["NODE_OPTIONS"] = "--dns-result-order=ipv4first"
        os.environ["NODE_NO_WARNINGS"] = "1"

        # Show stdout/stderr in real-time for download progress
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
        )
        if result.returncode != 0:
            console.print("[red]Browser installation failed[/red]")
            return False

        # Install system dependencies on Linux (only once)
        if sys.platform == "linux":
            from pathlib import Path
            deps_marker = Path.home() / ".nova-agent" / ".deps-installed"
            if not deps_marker.exists():
                console.print("[dim]Installing system dependencies...[/dim]")
                result = subprocess.run(
                    [sys.executable, "-m", "playwright", "install-deps", "chromium"],
                )
                if result.returncode == 0:
                    deps_marker.parent.mkdir(parents=True, exist_ok=True)
                    deps_marker.touch()

        return True
    except Exception as e:
        console.print(f"[red]Browser check failed: {e}[/red]")
        return False


app = typer.Typer(
    name="nova-agent",
    help="Nova Agent - Browser automation agent for Nova QA platform",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        console.print(f"Nova Agent v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Nova Agent - Browser automation agent for Nova QA platform."""
    pass


@app.command()
def login(
    frontend_url: str | None = typer.Option(
        None,
        "--url",
        "-u",
        help="Frontend URL for agent registration",
    ),
) -> None:
    """Register agent and get token.

    Login to Nova platform in browser, register agent, and enter the token.
    """
    config = get_config_manager()

    # Check if token already exists
    if config.has_token():
        overwrite = typer.confirm(
            "Token already exists. Register a new one?",
            default=False,
        )
        if not overwrite:
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Exit()

    # Load settings
    settings = get_settings()
    url = frontend_url or settings.frontend_url

    # Open browser
    register_url = f"{url.rstrip('/')}{settings.agent_register_path}"
    console.print(
        Panel(
            f"[bold]Opening agent registration page.[/bold]\n\n"
            f"1. Login to Nova platform in your browser\n"
            f"2. Enter agent name and register\n"
            f"3. Copy the issued token\n\n"
            f"URL: {register_url}",
            title="Nova Agent Registration",
            border_style="blue",
        )
    )

    try:
        webbrowser.open(register_url)
        console.print("[green]Browser opened.[/green]\n")
    except Exception as e:
        console.print(f"[yellow]Could not open browser: {e}[/yellow]")
        console.print(f"Please visit: {register_url}\n")

    # Get token input
    token = Prompt.ask(
        "[bold]Paste your token[/bold]",
        password=True,
    )

    if not token.strip():
        console.print("[red]No token entered.[/red]")
        raise typer.Exit(1)

    # Save token
    config.save_token(token)
    console.print(
        Panel(
            "[bold green]Agent registered![/bold green]\n\n"
            f"Token saved to: {config.token_file}\n\n"
            "[dim]Run 'nova-agent start' to start the agent.[/dim]",
            border_style="green",
        )
    )


@app.command()
def start(
    headless: bool | None = typer.Option(
        None,
        "--headless/--no-headless",
        help="Browser headless mode",
    ),
    gateway_url: str | None = typer.Option(
        None,
        "--gateway-url",
        "-g",
        help="Gateway WebSocket URL",
    ),
    pool_size: int | None = typer.Option(
        None,
        "--pool-size",
        "-p",
        help="Max concurrent browsers (default: 1)",
        min=1,
        max=10,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose logging",
    ),
) -> None:
    """Start the agent.

    Connect to Gateway and wait for jobs.
    """
    # Check for updates
    _check_for_updates()

    config = get_config_manager()

    # Check token
    token = config.load_token()
    if not token:
        console.print(
            "[red]No token found.[/red]\n"
            "[dim]Run 'nova-agent login' to register first.[/dim]"
        )
        raise typer.Exit(1)

    # Load settings
    settings = get_settings()
    actual_gateway_url = gateway_url or settings.gateway_url
    actual_headless = headless if headless is not None else settings.headless
    actual_pool_size = pool_size or settings.pool_size

    # Set log level and verbose mode
    set_verbose(verbose)
    if verbose:
        structlog.configure(
            wrapper_class=structlog.make_filtering_bound_logger(10),  # DEBUG
        )

    # Check browser installation
    if not _ensure_browser_installed():
        raise typer.Exit(1)

    console.print(
        Panel(
            f"[bold]Nova Agent Starting[/bold]\n\n"
            f"Gateway: {actual_gateway_url}\n"
            f"Headless: {actual_headless}\n"
            f"Pool Size: {actual_pool_size}\n"
            f"Verbose: {verbose}",
            border_style="blue",
        )
    )

    # Run agent
    try:
        asyncio.run(_run_agent(token, actual_gateway_url, actual_headless, actual_pool_size))
    except KeyboardInterrupt:
        console.print("\n[yellow]Agent stopped.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


async def _run_agent(
    token: str,
    gateway_url: str,
    headless: bool,
    pool_size: int,
) -> None:
    """Run the agent main loop.

    Args:
        token: JWT token
        gateway_url: Gateway WebSocket URL
        headless: Headless mode flag
        pool_size: Browser pool size
    """
    from nova_agent.browser.pool import BrowserPool
    from nova_agent.executor.job_manager import JobManager
    from nova_agent.websocket.client import AgentWebSocketClient

    settings = get_settings()

    # Initialize browser pool (browsers start on job assignment)
    browser_pool = BrowserPool(
        max_size=pool_size,
        headless=headless,
        viewport_width=settings.viewport_width,
        viewport_height=settings.viewport_height,
    )
    console.print(f"[green]Browser pool initialized (max {pool_size})[/green]")

    # Initialize job manager
    job_manager = JobManager(browser_pool=browser_pool)

    # Initialize WebSocket client
    ws_client = AgentWebSocketClient(
        gateway_url=gateway_url,
        token=token,
        job_manager=job_manager,
    )

    # Set client reference in JobManager
    job_manager.set_client(ws_client)

    try:
        # WebSocket connection and main loop
        await ws_client.connect_and_run()

    finally:
        # Cleanup
        await job_manager.shutdown()
        console.print("[yellow]Browser pool shut down.[/yellow]")


@app.command()
def status() -> None:
    """Check agent status.

    Shows token and connection status.
    """
    config = get_config_manager()

    if config.has_token():
        console.print(
            Panel(
                f"[bold green]Agent Registered[/bold green]\n\n"
                f"Token file: {config.token_file}\n\n"
                "[dim]Run 'nova-agent start' to start the agent.[/dim]",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                "[bold yellow]Agent Not Registered[/bold yellow]\n\n"
                "[dim]Run 'nova-agent login' to register.[/dim]",
                border_style="yellow",
            )
        )


@app.command()
def logout() -> None:
    """Delete token and logout.

    Removes the saved token.
    """
    config = get_config_manager()

    if not config.has_token():
        console.print("[yellow]No token found.[/yellow]")
        raise typer.Exit()

    confirm = typer.confirm("Delete token?", default=False)
    if not confirm:
        console.print("[yellow]Cancelled.[/yellow]")
        raise typer.Exit()

    config.delete_token()
    console.print("[green]Token deleted.[/green]")


@app.command()
def update() -> None:
    """Update Nova Agent.

    Install latest version from PyPI.
    """
    console.print("[dim]Checking for updates...[/dim]")

    if _do_update():
        console.print("[green]Update complete![/green]")
    else:
        console.print("[red]Update failed[/red]")
        raise typer.Exit(1)


@app.command(name="install-deps")
def install_deps() -> None:
    """Install browser system dependencies.

    Required on Linux servers without GUI. Run with sudo.
    """
    from pathlib import Path

    console.print("[dim]Installing browser dependencies...[/dim]")
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install-deps", "chromium"],
    )
    if result.returncode == 0:
        # Mark as installed
        deps_marker = Path.home() / ".nova-agent" / ".deps-installed"
        deps_marker.parent.mkdir(parents=True, exist_ok=True)
        deps_marker.touch()
        console.print("[green]Dependencies installed![/green]")
    else:
        console.print("[red]Installation failed. Try running with sudo.[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
