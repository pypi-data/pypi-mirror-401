"""
Kurral Security CLI - Security scanning via Kurral Cloud API

Usage:
    kurral security scan --agent-url <url>
    kurral security status <scan_id>
    kurral security list
"""

import os
import sys
import time
import click
import httpx
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

console = Console()

# API Configuration
DEFAULT_API_URL = "https://kurral-api.onrender.com"
API_URL = os.environ.get("KURRAL_API_URL", DEFAULT_API_URL)


def get_api_key() -> str | None:
    """Get API key from environment."""
    return os.environ.get("KURRAL_API_KEY")


def api_request(method: str, endpoint: str, **kwargs) -> httpx.Response:
    """Make authenticated API request."""
    api_key = get_api_key()
    if not api_key:
        console.print("[red]Error:[/red] KURRAL_API_KEY environment variable not set")
        console.print("\nGet your API key from: https://app.kurral.com/dashboard")
        console.print("Then run: export KURRAL_API_KEY=kr_live_xxx")
        sys.exit(1)

    headers = kwargs.pop("headers", {})
    headers["X-API-Key"] = api_key
    headers["Content-Type"] = "application/json"

    url = f"{API_URL}{endpoint}"

    try:
        response = httpx.request(method, url, headers=headers, timeout=60.0, **kwargs)
        return response
    except httpx.ConnectError:
        console.print(f"[red]Error:[/red] Could not connect to Kurral API at {API_URL}")
        sys.exit(1)
    except httpx.TimeoutException:
        console.print("[red]Error:[/red] Request timed out")
        sys.exit(1)


@click.group(name="security")
def security_group():
    """Security scanning for MCP agents.

    Run security assessments against your AI agents to find vulnerabilities
    before production.

    Examples:
        kurral security scan --agent-url http://localhost:3000
        kurral security status scan_abc123
        kurral security list
    """
    pass


@security_group.command()
@click.option("--agent-url", required=True, help="URL of the MCP agent to scan")
@click.option("--duration", default="5m", help="Scan duration (e.g., 5m, 10m, 30m)")
@click.option("--categories", default="all", help="Vulnerability categories to test (comma-separated)")
@click.option("--wait/--no-wait", default=True, help="Wait for scan to complete")
@click.option("--output", type=click.Choice(["table", "json"]), default="table", help="Output format")
def scan(agent_url: str, duration: str, categories: str, wait: bool, output: str):
    """Start a security scan against an MCP agent.

    Examples:
        kurral security scan --agent-url http://localhost:3000
        kurral security scan --agent-url http://localhost:3000 --duration 10m
        kurral security scan --agent-url http://localhost:3000 --no-wait
    """
    console.print(Panel.fit(
        "[bold cyan]Kurral Security Scanner[/bold cyan]\n"
        f"Target: {agent_url}",
        border_style="cyan"
    ))

    # Parse duration
    duration_minutes = 5
    if duration.endswith("m"):
        duration_minutes = int(duration[:-1])
    elif duration.endswith("h"):
        duration_minutes = int(duration[:-1]) * 60

    # Start scan
    console.print("\n[dim]Starting security assessment...[/dim]")

    response = api_request("POST", "/api/scans", json={
        "agent_url": agent_url,
        "duration_minutes": duration_minutes,
        "categories": categories.split(",") if categories != "all" else None,
    })

    if response.status_code == 401:
        console.print("[red]Error:[/red] Invalid API key")
        sys.exit(1)
    elif response.status_code == 422:
        console.print(f"[red]Error:[/red] Invalid request: {response.json()}")
        sys.exit(1)
    elif response.status_code != 200 and response.status_code != 201:
        console.print(f"[red]Error:[/red] API error: {response.status_code}")
        sys.exit(1)

    scan_data = response.json()
    scan_id = scan_data.get("id") or scan_data.get("scan_id")

    console.print(f"[green]✓[/green] Scan started: [cyan]{scan_id}[/cyan]")

    if not wait:
        console.print(f"\nCheck status: [dim]kurral security status {scan_id}[/dim]")
        console.print(f"View results: [dim]https://app.kurral.com/dashboard/scans/{scan_id}[/dim]")
        return

    # Poll for completion
    console.print("\n[dim]Running security tests...[/dim]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing agent...", total=None)

        max_wait = duration_minutes * 60 + 120  # Duration + 2 min buffer
        start_time = time.time()

        while time.time() - start_time < max_wait:
            status_response = api_request("GET", f"/api/scans/{scan_id}")

            if status_response.status_code != 200:
                progress.stop()
                console.print(f"[red]Error:[/red] Failed to get scan status")
                sys.exit(1)

            status_data = status_response.json()
            status = status_data.get("status", "unknown")

            if status == "completed":
                progress.stop()
                break
            elif status == "failed":
                progress.stop()
                console.print(f"[red]Scan failed:[/red] {status_data.get('error', 'Unknown error')}")
                sys.exit(1)

            progress.update(task, description=f"Analyzing agent... [{status}]")
            time.sleep(3)
        else:
            progress.stop()
            console.print("[yellow]Warning:[/yellow] Scan still running. Check status later.")
            console.print(f"  kurral security status {scan_id}")
            return

    # Display results
    display_scan_results(status_data, output)


@security_group.command()
@click.argument("scan_id")
@click.option("--output", type=click.Choice(["table", "json"]), default="table", help="Output format")
def status(scan_id: str, output: str):
    """Get the status of a security scan.

    Example:
        kurral security status scan_abc123
    """
    response = api_request("GET", f"/api/scans/{scan_id}")

    if response.status_code == 404:
        console.print(f"[red]Error:[/red] Scan not found: {scan_id}")
        sys.exit(1)
    elif response.status_code != 200:
        console.print(f"[red]Error:[/red] API error: {response.status_code}")
        sys.exit(1)

    scan_data = response.json()
    display_scan_results(scan_data, output)


@security_group.command("list")
@click.option("--limit", "-n", default=10, help="Number of scans to show")
@click.option("--output", type=click.Choice(["table", "json"]), default="table", help="Output format")
def list_scans(limit: int, output: str):
    """List recent security scans.

    Example:
        kurral security list
        kurral security list -n 20
    """
    response = api_request("GET", f"/api/scans?limit={limit}")

    if response.status_code != 200:
        console.print(f"[red]Error:[/red] API error: {response.status_code}")
        sys.exit(1)

    data = response.json()
    scans = data.get("scans", [])

    if not scans:
        console.print("[yellow]No scans found.[/yellow]")
        console.print("\nStart a scan: [dim]kurral security scan --agent-url <url>[/dim]")
        return

    if output == "json":
        import json
        console.print(json.dumps(scans, indent=2))
        return

    table = Table(title="Recent Security Scans")
    table.add_column("ID", style="cyan")
    table.add_column("Agent", style="white")
    table.add_column("Status", style="white")
    table.add_column("Findings", style="white")
    table.add_column("Score", style="white")
    table.add_column("Created", style="dim")

    for scan in scans:
        scan_id = scan.get("id", "")[:12]
        agent = scan.get("agent_url", "unknown")
        if len(agent) > 30:
            agent = agent[:27] + "..."

        status = scan.get("status", "unknown")
        status_color = {
            "completed": "green",
            "running": "yellow",
            "pending": "dim",
            "failed": "red",
        }.get(status, "white")

        findings = scan.get("finding_count", 0)
        findings_color = "red" if findings > 0 else "green"

        score = scan.get("security_score")
        score_str = f"{score}" if score is not None else "-"
        score_color = "green" if score and score >= 80 else "yellow" if score and score >= 50 else "red"

        created = scan.get("created_at", "")[:10]

        table.add_row(
            scan_id,
            agent,
            f"[{status_color}]{status}[/{status_color}]",
            f"[{findings_color}]{findings}[/{findings_color}]",
            f"[{score_color}]{score_str}[/{score_color}]",
            created,
        )

    console.print(table)


def display_scan_results(scan_data: dict, output: str):
    """Display scan results in the specified format."""
    if output == "json":
        import json
        console.print(json.dumps(scan_data, indent=2))
        return

    scan_id = scan_data.get("id", "unknown")
    status = scan_data.get("status", "unknown")
    agent_url = scan_data.get("agent_url", "unknown")
    score = scan_data.get("security_score")
    findings = scan_data.get("findings", [])

    # Status color
    status_color = {
        "completed": "green",
        "running": "yellow",
        "pending": "dim",
        "failed": "red",
    }.get(status, "white")

    # Score color
    if score is not None:
        if score >= 80:
            score_color = "green"
            score_label = "Good"
        elif score >= 50:
            score_color = "yellow"
            score_label = "Fair"
        else:
            score_color = "red"
            score_label = "Poor"
        score_display = f"[{score_color}]{score}/100 ({score_label})[/{score_color}]"
    else:
        score_display = "[dim]-[/dim]"

    # Header
    console.print(Panel(
        f"[bold]Scan ID:[/bold] {scan_id}\n"
        f"[bold]Agent:[/bold] {agent_url}\n"
        f"[bold]Status:[/bold] [{status_color}]{status}[/{status_color}]\n"
        f"[bold]Security Score:[/bold] {score_display}",
        title="Scan Results",
        border_style="cyan"
    ))

    if not findings:
        if status == "completed":
            console.print("\n[green]✓ No vulnerabilities found![/green]")
        return

    # Findings table
    console.print(f"\n[bold]Findings ({len(findings)})[/bold]\n")

    table = Table()
    table.add_column("Severity", style="white", width=10)
    table.add_column("Category", style="cyan", width=20)
    table.add_column("Tool", style="white", width=20)
    table.add_column("Description", style="white")

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    sorted_findings = sorted(findings, key=lambda f: severity_order.get(f.get("severity", "INFO"), 5))

    for finding in sorted_findings:
        severity = finding.get("severity", "INFO")
        severity_color = {
            "CRITICAL": "red bold",
            "HIGH": "red",
            "MEDIUM": "yellow",
            "LOW": "blue",
            "INFO": "dim",
        }.get(severity, "white")

        table.add_row(
            f"[{severity_color}]{severity}[/{severity_color}]",
            finding.get("category", "unknown"),
            finding.get("tool_name", "unknown"),
            finding.get("description", "")[:60] + "..." if len(finding.get("description", "")) > 60 else finding.get("description", ""),
        )

    console.print(table)

    # Dashboard link
    console.print(f"\n[dim]View full report: https://app.kurral.com/dashboard/scans/{scan_id}[/dim]")
