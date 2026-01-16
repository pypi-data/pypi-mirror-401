#!/usr/bin/env python3
"""
Aribot CLI - AI-Powered Threat Modeling

Usage:
    aribot login                    # Authenticate with API key
    aribot analyze <diagram>        # Analyze a diagram file
    aribot threats <diagram-id>     # List threats for a diagram
    aribot export <diagram-id>      # Export report
    aribot diagrams                 # List all diagrams
"""

import os
import sys
import time
import hashlib
import hmac
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import click
import httpx
import keyring
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
API_BASE = "https://api.aribot.ayurak.com/aribot-api"
SERVICE_NAME = "aribot-cli"
VERSION = "1.0.10"


# =============================================================================
# SECURE CREDENTIAL MANAGEMENT
# =============================================================================

def get_api_key() -> Optional[str]:
    """Get API key from secure keyring storage."""
    try:
        return keyring.get_password(SERVICE_NAME, "api_key")
    except Exception:
        # Fallback to environment variable
        return os.environ.get("ARIBOT_API_KEY")


def set_api_key(api_key: str) -> None:
    """Store API key in secure keyring storage."""
    try:
        keyring.set_password(SERVICE_NAME, "api_key", api_key)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not store in keyring: {e}[/yellow]")
        console.print("[dim]Set ARIBOT_API_KEY environment variable as fallback[/dim]")


def delete_api_key() -> None:
    """Remove API key from keyring."""
    try:
        keyring.delete_password(SERVICE_NAME, "api_key")
    except keyring.errors.PasswordDeleteError:
        pass
    except Exception:
        pass


def get_stored_user_info() -> dict:
    """Get cached user info from keyring."""
    try:
        email = keyring.get_password(SERVICE_NAME, "user_email")
        company = keyring.get_password(SERVICE_NAME, "company")
        return {"email": email, "company": company}
    except Exception:
        return {}


def set_stored_user_info(email: str, company: str) -> None:
    """Cache user info in keyring."""
    try:
        keyring.set_password(SERVICE_NAME, "user_email", email or "")
        keyring.set_password(SERVICE_NAME, "company", company or "")
    except Exception:
        pass


# =============================================================================
# SECURE API CLIENT
# =============================================================================

def get_headers() -> dict:
    """Get auth headers for API requests."""
    api_key = get_api_key()
    if not api_key:
        console.print("[red]Not authenticated. Run: aribot login[/red]")
        sys.exit(1)

    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
        "User-Agent": f"aribot-cli/{VERSION} (Python)",
    }


def get_auth_header_only() -> dict:
    """Get only Authorization header (for file uploads)."""
    api_key = get_api_key()
    if not api_key:
        console.print("[red]Not authenticated. Run: aribot login[/red]")
        sys.exit(1)

    return {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": f"aribot-cli/{VERSION} (Python)",
    }


def create_request_signature(method: str, path: str, timestamp: str, body: str = "") -> str:
    """Create HMAC signature for request integrity verification."""
    api_key = get_api_key()
    if not api_key:
        return ""

    # Create signature payload
    payload = f"{method.upper()}\n{path}\n{timestamp}\n{body}"

    # Sign with API key
    signature = hmac.new(
        api_key.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature


def api_request(
    endpoint: str,
    method: str = "GET",
    json_data: dict = None,
    files: dict = None,
    data: dict = None,
    timeout: float = 60.0
) -> dict:
    """Make secure API request with proper error handling."""
    headers = get_headers() if not files else get_auth_header_only()

    # Add request timestamp for replay attack prevention
    timestamp = datetime.now(timezone.utc).isoformat()
    headers["X-Request-Timestamp"] = timestamp
    headers["X-Request-ID"] = secrets.token_urlsafe(16)

    try:
        with httpx.Client(timeout=timeout) as client:
            if method == "GET":
                response = client.get(f"{API_BASE}{endpoint}", headers=headers)
            elif method == "POST":
                if files:
                    response = client.post(
                        f"{API_BASE}{endpoint}",
                        headers=headers,
                        files=files,
                        data=data
                    )
                else:
                    response = client.post(
                        f"{API_BASE}{endpoint}",
                        headers=headers,
                        json=json_data
                    )
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            console.print("[red]Authentication failed. Run: aribot login[/red]")
        elif e.response.status_code == 403:
            console.print("[red]Access denied. Check your API key permissions.[/red]")
        elif e.response.status_code == 429:
            console.print("[yellow]Rate limit exceeded. Please wait and try again.[/yellow]")
        else:
            try:
                error = e.response.json()
                console.print(f"[red]API Error: {error.get('detail', str(e))}[/red]")
            except Exception:
                console.print(f"[red]API Error: {e.response.status_code}[/red]")
        sys.exit(1)
    except httpx.RequestError as e:
        console.print(f"[red]Network error: {e}[/red]")
        sys.exit(1)


def resolve_diagram_id(short_id: str) -> str:
    """Resolve short UUID to full UUID by fetching diagrams."""
    # If it already looks like a full UUID, return it
    if '-' in short_id or len(short_id) >= 32:
        return short_id

    # Fetch diagrams and find by prefix match
    data = api_request("/v2/threat-modeling/diagrams/?limit=100")
    results = data.get("results", [])

    for diagram in results:
        if diagram.get("id", "").startswith(short_id):
            return diagram["id"]

    raise click.ClickException(f"No diagram found matching ID: {short_id}")


# =============================================================================
# CLI COMMANDS
# =============================================================================

@click.group()
@click.version_option(version=VERSION)
def main():
    """Aribot CLI - AI-powered threat modeling by Ayurak."""
    pass


@main.command()
def login():
    """Authenticate with your Aribot API key."""
    api_key = click.prompt("Enter your Aribot API key", hide_input=True)

    # Validate API key format (should be URL-safe base64)
    if len(api_key) < 20:
        console.print("[red]Invalid API key format[/red]")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Exchanging API key for token...", total=None)

        try:
            with httpx.Client(timeout=30.0) as client:
                # Exchange API key for token
                response = client.post(
                    f"{API_BASE}/v1/developer/token/",
                    headers={"Content-Type": "application/json"},
                    json={"api_key": api_key}
                )

                if response.status_code == 200:
                    data = response.json()
                    set_api_key(api_key)

                    # Store user info
                    user = data.get("user", {})
                    set_stored_user_info(
                        user.get("email", ""),
                        user.get("company", "")
                    )

                    progress.remove_task(task)
                    console.print("[green]Authenticated successfully![/green]")
                    if user.get("email"):
                        console.print(f"[dim]Logged in as {user.get('email')}[/dim]")
                else:
                    progress.remove_task(task)
                    try:
                        error = response.json()
                        console.print(f"[red]{error.get('message', 'Invalid API key')}[/red]")
                    except Exception:
                        console.print("[red]Invalid API key[/red]")

        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Authentication failed: {e}[/red]")


@main.command()
def logout():
    """Remove stored credentials."""
    delete_api_key()
    try:
        keyring.delete_password(SERVICE_NAME, "user_email")
        keyring.delete_password(SERVICE_NAME, "company")
    except Exception:
        pass
    console.print("[green]Logged out successfully.[/green]")


@main.command()
def whoami():
    """Show current authentication status."""
    api_key = get_api_key()

    if not api_key:
        console.print("[yellow]Not authenticated[/yellow]")
        console.print("[dim]Run: aribot login[/dim]")
        return

    try:
        # Fetch user info and API key info in parallel
        user_data = api_request("/v1/users/me/")
        keys_data = api_request("/v1/developer/api-keys/")

        # Get company from API keys endpoint
        company = "N/A"
        plan = "N/A"
        if keys_data and isinstance(keys_data, list) and len(keys_data) > 0:
            company = keys_data[0].get("company_name", "N/A")
            plan = keys_data[0].get("plan_name", "N/A")
        elif user_data.get("company"):
            company = user_data.get("company")

        console.print("[green]Authenticated as:[/green]")
        console.print(f"  Email:   {user_data.get('email', 'N/A')}")
        console.print(f"  Company: {company}")
        console.print(f"  Plan:    {plan}")

        # Show API key info (masked)
        console.print(f"  API Key: {api_key[:8]}...{api_key[-4:]}")

    except Exception:
        # Try cached info
        cached = get_stored_user_info()
        if cached.get("email"):
            console.print("[yellow]API key stored (validation pending)[/yellow]")
            console.print(f"  Email:   {cached.get('email', 'N/A')}")
            console.print(f"  Company: {cached.get('company', 'N/A')}")
        else:
            console.print("[yellow]API key stored but validation failed[/yellow]")


@main.command()
@click.option("-l", "--limit", default=10, help="Number of diagrams to show")
def diagrams(limit: int):
    """List all your diagrams."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Fetching diagrams...", total=None)

        try:
            data = api_request(f"/v2/threat-modeling/diagrams/?limit={limit}")
            progress.remove_task(task)

            if not data.get("results"):
                console.print("[dim]No diagrams found.[/dim]")
                console.print("[dim]Create one at https://portal.aribot.ayurak.com[/dim]")
                return

            table = Table(title="Your Diagrams")
            table.add_column("ID", style="cyan")
            table.add_column("Name")
            table.add_column("Status")
            table.add_column("Threats", justify="right")
            table.add_column("Created")

            for d in data["results"]:
                # Use 'stage' field (not 'status')
                stage = d.get("stage", "pending")
                status_icon = "[green]✓[/green]" if stage == "completed" else "[yellow]⋯[/yellow]"

                # Use filename as fallback for name
                name = d.get("name") or d.get("filename") or "Unnamed"

                table.add_row(
                    d["id"][:8],
                    name[:40],
                    status_icon,
                    str(d.get("threats_count", 0)),
                    d.get("created_at", "")[:10]
                )

            console.print(table)
            console.print(f"[dim]Showing {len(data['results'])} of {data.get('count', 0)} diagrams[/dim]")

        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Failed to fetch diagrams: {e}[/red]")


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("-n", "--name", help="Diagram name")
@click.option("--auto-threats/--no-auto-threats", default=True, help="Auto-generate AI threats")
def analyze(file: str, name: Optional[str], auto_threats: bool):
    """Upload and analyze a diagram file."""
    file_path = Path(file)
    diagram_name = name or file_path.stem

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Uploading diagram...", total=None)

        try:
            with open(file_path, "rb") as f:
                files = {"file": (file_path.name, f)}
                data = {
                    "name": diagram_name,
                    "auto_generate_threats": str(auto_threats).lower()
                }

                headers = get_auth_header_only()
                with httpx.Client(timeout=120.0) as client:
                    response = client.post(
                        f"{API_BASE}/v2/threat-modeling/diagrams/upload-analyze/",
                        headers=headers,
                        files=files,
                        data=data
                    )
                    response.raise_for_status()
                    result = response.json()

            progress.update(task, description="Diagram uploaded!")
            progress.remove_task(task)

            console.print("\n[bold]Diagram Created:[/bold]")
            console.print(f"  ID:     [cyan]{result['id']}[/cyan]")
            console.print(f"  Name:   {result.get('name') or result.get('filename', 'Untitled')}")
            console.print(f"  Status: {result.get('stage', result.get('status', 'pending'))}")

            if auto_threats:
                task2 = progress.add_task("Generating AI threats...", total=None)

                # Poll for completion
                for _ in range(30):
                    time.sleep(2)
                    status = api_request(f"/v2/threat-modeling/diagrams/{result['id']}/")

                    if status.get("stage") == "completed":
                        progress.remove_task(task2)
                        console.print(f"[green]Generated {status.get('threats_count', 0)} threats[/green]")
                        break
                else:
                    progress.remove_task(task2)
                    console.print("[yellow]Threat generation in progress...[/yellow]")

            console.print(f"\n[dim]View at: https://portal.aribot.ayurak.com/diagrams/{result['id']}[/dim]")

        except httpx.HTTPStatusError as e:
            progress.remove_task(task)
            console.print(f"[red]Upload failed: {e.response.status_code}[/red]")
        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Analysis failed: {e}[/red]")


@main.command()
@click.argument("diagram_id")
@click.option("-s", "--severity", help="Filter by severity (critical, high, medium, low)")
def threats(diagram_id: str, severity: Optional[str]):
    """List threats for a diagram."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Fetching threats...", total=None)

        try:
            url = f"/v2/threat-modeling/diagrams/{diagram_id}/threats/"
            if severity:
                url += f"?severity={severity}"

            data = api_request(url)
            progress.remove_task(task)

            # Handle both response formats
            threats_list = data.get("threats") or data.get("results") or []

            if not threats_list:
                console.print("[dim]No threats found.[/dim]")
                return

            table = Table(title="Threats")
            table.add_column("Severity", style="bold")
            table.add_column("Title")
            table.add_column("Category")
            table.add_column("ID", style="dim")

            severity_styles = {
                "critical": "red",
                "high": "yellow",
                "medium": "blue",
                "low": "dim"
            }

            for t in threats_list:
                sev = t.get("severity", "medium") or "medium"
                style = severity_styles.get(sev.lower(), "white")

                # Handle both title and name fields
                title = t.get("title") or t.get("name") or "Untitled"
                category = t.get("category") or t.get("stride_category") or "N/A"

                table.add_row(
                    f"[{style}]{sev.upper()}[/{style}]",
                    title[:60],
                    category,
                    str(t.get("id", ""))[:8]
                )

            console.print(table)
            total = data.get("count") or len(threats_list)
            console.print(f"\n[dim]Total: {total} threats[/dim]")

        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Failed to fetch threats: {e}[/red]")


@main.command()
@click.argument("diagram_id")
@click.option("-f", "--format", "fmt", default="json", help="Export format (pdf, json, csv)")
@click.option("-o", "--output", help="Output file path")
def export(diagram_id: str, fmt: str, output: Optional[str]):
    """Export diagram report."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Exporting {fmt.upper()} report...", total=None)

        try:
            headers = get_auth_header_only()

            with httpx.Client(timeout=120.0) as client:
                response = client.get(
                    f"{API_BASE}/v2/threat-modeling/diagrams/{diagram_id}/export/?format={fmt}",
                    headers=headers
                )
                response.raise_for_status()

                output_path = output or f"aribot-report-{diagram_id[:8]}.{fmt}"

                with open(output_path, "wb") as f:
                    f.write(response.content)

            progress.remove_task(task)
            console.print(f"[green]Report saved to [cyan]{output_path}[/cyan][/green]")

        except httpx.HTTPStatusError as e:
            progress.remove_task(task)
            console.print(f"[red]Export failed: {e.response.status_code}[/red]")
        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Export failed: {e}[/red]")


@main.command("generate-threats")
@click.argument("diagram_id")
def generate_threats(diagram_id: str):
    """Generate AI threats for an existing diagram."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Generating AI threats...", total=None)

        try:
            api_request(
                f"/v2/threat-modeling/diagrams/{diagram_id}/generate-threats/",
                method="POST"
            )

            progress.update(task, description="Processing...")

            # Poll for completion
            for _ in range(30):
                time.sleep(2)
                status = api_request(f"/v2/threat-modeling/diagrams/{diagram_id}/")

                if status.get("ai_threats_generated"):
                    progress.remove_task(task)
                    console.print(f"[green]Generated {status.get('threats_count', 0)} threats[/green]")
                    return

            progress.remove_task(task)
            console.print("[green]Threat generation initiated[/green]")

        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Failed to generate threats: {e}[/red]")


@main.command()
def status():
    """Check API status and rate limits."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Checking API status...", total=None)

        try:
            # Check health endpoint (no auth required)
            with httpx.Client(timeout=10.0) as client:
                health_response = client.get(f"{API_BASE}/health/")
                health = health_response.json() if health_response.status_code == 200 else {}

            progress.remove_task(task)

            console.print("[bold]API Status[/bold]\n")
            status_icon = "[green]✓ Healthy[/green]" if health.get("status") == "healthy" else "[red]✗ Unhealthy[/red]"
            console.print(f"  Status:   {status_icon}")
            console.print(f"  Version:  [cyan]{health.get('version', 'N/A')}[/cyan]")
            console.print(f"  Features: {'[green]Enabled[/green]' if health.get('features_enabled') else '[yellow]Disabled[/yellow]'}")

            # Check rate limits if authenticated
            api_key = get_api_key()
            if api_key:
                try:
                    limits = api_request("/v2/developer-portal/rate-limits/usage/")
                    console.print("\n[bold]Rate Limits[/bold]")
                    console.print(f"  Requests/min:  {limits.get('requests_per_minute', {}).get('used', 0)}/{limits.get('requests_per_minute', {}).get('limit', 'unlimited')}")
                    console.print(f"  Requests/hour: {limits.get('requests_per_hour', {}).get('used', 0)}/{limits.get('requests_per_hour', {}).get('limit', 'unlimited')}")
                    console.print(f"  Requests/day:  {limits.get('requests_per_day', {}).get('used', 0)}/{limits.get('requests_per_day', {}).get('limit', 'unlimited')}")
                except Exception:
                    console.print("\n[dim]Rate limit info requires authentication[/dim]")

        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Failed to check status: {e}[/red]")


# Compliance Standards
COMPLIANCE_STANDARDS = [
    'SOC2', 'ISO27001', 'ISO27017', 'ISO27018', 'ISO22301',
    'NIST-CSF', 'NIST-800-53', 'NIST-800-171',
    'PCI-DSS', 'PCI-DSS-4.0',
    'GDPR', 'CCPA', 'LGPD', 'PIPEDA',
    'HIPAA', 'HITRUST',
    'FedRAMP-Low', 'FedRAMP-Moderate', 'FedRAMP-High',
    'CIS-AWS', 'CIS-Azure', 'CIS-GCP', 'CIS-Kubernetes',
    'SOX', 'GLBA', 'FISMA',
    'CSA-CCM', 'MITRE-ATT&CK', 'OWASP-TOP-10',
]


@main.command()
@click.argument("diagram_id")
@click.option("-s", "--standard", default="SOC2", help="Compliance standard (SOC2, ISO27001, NIST, PCI-DSS, GDPR, HIPAA)")
@click.option("--list-standards", is_flag=True, help="List all available compliance standards")
def compliance(diagram_id: str, standard: str, list_standards: bool):
    """Run compliance assessment on a diagram."""
    if list_standards:
        console.print("[bold]Supported Compliance Standards[/bold]\n")
        for s in COMPLIANCE_STANDARDS:
            console.print(f"  [cyan]•[/cyan] {s}")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Running {standard} compliance assessment...", total=None)

        try:
            data = api_request(
                "/v2/compliances/assess_diagram/",
                method="POST",
                json_data={
                    "diagram_id": diagram_id,
                    "frameworks": [standard]
                }
            )

            progress.remove_task(task)
            console.print(f"[green]Compliance assessment complete![/green]")

            console.print(f"\n[bold]{standard} Compliance Report[/bold]\n")

            score = data.get("score", 0)
            score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
            console.print(f"  Score:           [{score_color}]{score}%[/{score_color}]")
            console.print(f"  Passed Controls: [green]{data.get('passed_controls', 0)}[/green]")
            console.print(f"  Failed Controls: [red]{data.get('failed_controls', 0)}[/red]")

            status = data.get("status", "unknown")
            status_color = "green" if status == "compliant" else "yellow"
            console.print(f"  Status:          [{status_color}]{status.title()}[/{status_color}]")

            findings = data.get("findings", [])
            if findings:
                console.print("\n[bold]Top Findings[/bold]")
                for f in findings[:5]:
                    sev = f.get("severity", "medium")
                    sev_color = "red" if sev == "high" else "yellow" if sev == "medium" else "dim"
                    console.print(f"  [{sev_color}][{sev.upper()}][/{sev_color}] {f.get('title', f.get('control_id', 'N/A'))}")

        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Compliance assessment failed: {e}[/red]")


@main.command()
@click.option("--roi", type=float, help="Calculate ROI for security investment (in USD)")
@click.option("--tco", help="Calculate TCO for cloud provider (aws, azure, gcp)")
@click.option("--analyze", "analyze_diagram", help="Analyze costs for a diagram")
@click.option("--cost", "cost_diagram", help="AI-powered cost intelligence for diagram")
@click.option("--dashboard", is_flag=True, help="Show economic intelligence dashboard")
def economics(roi: Optional[float], tco: Optional[str], analyze_diagram: Optional[str], cost_diagram: Optional[str], dashboard: bool):
    """Economic intelligence and cost analysis."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Calculating...", total=None)

        try:
            if roi:
                data = api_request(
                    "/v2/economic/v2/roi/create/",
                    method="POST",
                    json_data={
                        "investment": roi,
                        "risk_reduction": 50,
                        "time_horizon": 3
                    }
                )

                progress.remove_task(task)
                console.print("[green]ROI Analysis Complete![/green]")
                console.print("\n[bold]Security ROI Analysis[/bold]\n")
                console.print(f"  Investment:      [cyan]${roi:,.0f}[/cyan]")
                console.print(f"  Expected ROI:    [green]{data.get('roi_percentage', data.get('roi', 0))}%[/green]")
                console.print(f"  NPV:             [green]${data.get('npv', 0):,.0f}[/green]")
                console.print(f"  Payback Period:  [cyan]{data.get('payback_months', data.get('payback_period', 0))} months[/cyan]")
                console.print(f"  Risk Reduction:  [green]50%[/green]")

            elif tco:
                data = api_request(
                    "/v2/economic/tco/",
                    method="POST",
                    json_data={
                        "provider": tco,
                        "workload_type": "general",
                        "duration_months": 36
                    }
                )

                progress.remove_task(task)
                console.print("[green]TCO Analysis Complete![/green]")
                console.print(f"\n[bold]Total Cost of Ownership ({tco.upper()})[/bold]\n")
                console.print(f"  Monthly Cost:    [cyan]${data.get('monthly_cost', 0):,.0f}[/cyan]")
                console.print(f"  Annual Cost:     [cyan]${data.get('annual_cost', 0):,.0f}[/cyan]")
                console.print(f"  3-Year TCO:      [yellow]${data.get('total_cost', data.get('tco', 0)):,.0f}[/yellow]")

            elif analyze_diagram:
                data = api_request(
                    "/v2/economic/analyze/",
                    method="POST",
                    json_data={"diagram_id": analyze_diagram}
                )

                progress.remove_task(task)
                console.print("[green]Cost Analysis Complete![/green]")
                console.print("\n[bold]Diagram Cost Analysis[/bold]\n")
                console.print(f"  Estimated Monthly: [cyan]${data.get('monthly_estimate', 0):,.0f}[/cyan]")
                console.print(f"  Security Costs:    [yellow]${data.get('security_cost', 0):,.0f}[/yellow]")
                console.print(f"  Breach Risk Cost:  [red]${data.get('breach_risk_cost', 0):,.0f}[/red]")

            elif cost_diagram:
                # Diagram-specific cost analysis
                full_id = resolve_diagram_id(cost_diagram)
                data = api_request(f"/v2/threat-modeling/diagrams/{full_id}/cost-intelligence/")

                progress.remove_task(task)
                console.print("[green]Cost analysis complete![/green]")
                console.print("\n[bold]Diagram Cost Analysis[/bold]\n")

                summary = data.get("cost_summary", data)
                console.print(f"  Monthly Cost:     [cyan]${summary.get('total_monthly', summary.get('monthly', 0)):,.0f}[/cyan]")
                console.print(f"  Annual Cost:      [yellow]${summary.get('total_annual', (summary.get('total_monthly', 0) * 12)):,.0f}[/yellow]")
                console.print(f"  Component Count:  [white]{summary.get('component_count', len(data.get('components', [])))}[/white]")
                console.print(f"  Region:           [white]{summary.get('region', 'us-east-1')}[/white]")

                cost_breakdown = data.get("cost_breakdown", [])
                if cost_breakdown:
                    console.print("\n[bold]Cost Breakdown[/bold]\n")
                    for c in cost_breakdown[:5]:
                        console.print(f"  [cyan]•[/cyan] {c.get('name', c.get('component', 'Unknown'))}: [yellow]${c.get('monthly', c.get('cost', 0)):,.0f}[/yellow]/mo")

                recommendations = data.get("recommendations", [])
                if recommendations:
                    console.print("\n[bold]Optimization Recommendations[/bold]\n")
                    for r in recommendations[:3]:
                        console.print(f"  [green]•[/green] {r.get('title', r.get('description', r))}")

            elif dashboard:
                # Get economic intelligence from threat modeling endpoint
                data = api_request("/v2/threat-modeling/economic-intelligence/")

                progress.remove_task(task)
                console.print("[green]Dashboard loaded![/green]")
                console.print("\n[bold]Economic Intelligence Dashboard[/bold]\n")

                summary = data.get("company_summary", data.get("summary", data))
                console.print(f"  Total Monthly:    [cyan]${summary.get('total_monthly', summary.get('total_security_spend', 0)):,.0f}[/cyan]")
                console.print(f"  Total Annual:     [yellow]${summary.get('total_annual', 0):,.0f}[/yellow]")
                console.print(f"  Total Diagrams:   [white]{summary.get('total_diagrams', 0)}[/white]")
                console.print(f"  Region:           [white]{summary.get('region', 'us-east-1')}[/white]")

                top_cost_drivers = data.get("top_cost_drivers", [])
                if top_cost_drivers:
                    console.print("\n[bold]Top Cost Drivers[/bold]\n")
                    for d in top_cost_drivers[:5]:
                        console.print(f"  [cyan]•[/cyan] {d.get('name', 'Unknown')}: [yellow]${d.get('monthly_cost', 0):,.0f}[/yellow]/mo ({d.get('component_count', 0)} components)")

                ai_recommendations = data.get("intelligence", {}).get("recommendations", [])
                if ai_recommendations:
                    console.print("\n[bold]AI Recommendations[/bold]\n")
                    for r in ai_recommendations[:3]:
                        console.print(f"  [green]•[/green] {r.get('title', r.get('description', r))}")

            else:
                progress.remove_task(task)
                console.print("[yellow]Usage: aribot economics [--roi <amount>] [--tco <provider>] [--analyze <diagram-id>] [--dashboard][/yellow]")

        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Economic analysis failed: {e}[/red]")


@main.command("cloud-security")
@click.option("--scan", "scan_provider", is_flag=False, flag_value="all", default=None, help="Scan cloud security posture (aws, azure, gcp)")
@click.option("--findings", is_flag=True, help="List security findings")
@click.option("--dashboard", is_flag=True, help="Show cloud security dashboard")
@click.option("-s", "--severity", help="Filter findings by severity (critical, high, medium, low)")
def cloud_security(scan_provider: Optional[str], findings: bool, dashboard: bool, severity: Optional[str]):
    """Cloud security posture management (CSPM/CNAPP)."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Scanning cloud security...", total=None)

        try:
            if scan_provider:
                provider_param = scan_provider if scan_provider != "all" else None
                # Use security posture endpoint
                url = "/v2/compliances/dashboard/cloud-stats/"
                if provider_param:
                    url += f"?provider={provider_param}"
                data = api_request(url)

                progress.remove_task(task)
                console.print("[green]Cloud security scan complete![/green]")
                console.print("\n[bold]Cloud Security Posture[/bold]\n")

                stats = data.get("stats", data)
                score = stats.get("security_score", stats.get("score", "N/A"))
                score_color = "green" if isinstance(score, (int, float)) and score >= 80 else "yellow"
                console.print(f"  Security Score:   [{score_color}]{score}%[/{score_color}]")
                console.print(f"  Total Resources:  [cyan]{stats.get('total_resources', stats.get('resource_count', 0))}[/cyan]")
                console.print(f"  Compliant:        [green]{stats.get('compliant_resources', stats.get('compliant', 0))}[/green]")
                console.print(f"  Non-Compliant:    [red]{stats.get('non_compliant_resources', stats.get('non_compliant', 0))}[/red]")
                console.print(f"  Critical Issues:  [red]{stats.get('critical_findings', stats.get('critical', 0))}[/red]")

                if provider_param:
                    console.print(f"\n  Provider:         [cyan]{provider_param.upper()}[/cyan]")

                # Show provider breakdown if available
                by_provider = data.get("by_provider", {})
                if by_provider and not provider_param:
                    console.print("\n[bold]By Provider[/bold]\n")
                    for p, s in by_provider.items():
                        console.print(f"  [cyan]{p.upper():8}[/cyan] Resources: {s.get('count', 0)} | Score: {s.get('score', 'N/A')}%")

            elif findings:
                # Use top non-compliant assets endpoint
                url = "/v2/compliances/dashboard/top-assets/?limit=20"
                if severity:
                    url += f"&severity={severity}"
                data = api_request(url)

                progress.remove_task(task)
                console.print("\n[bold]Cloud Security Findings[/bold]\n")

                findings_list = data.get("results", data.get("findings", []))
                if not findings_list:
                    console.print("  [green]No open findings! Your cloud is secure.[/green]")
                else:
                    table = Table()
                    table.add_column("Severity", style="bold")
                    table.add_column("Title")
                    table.add_column("Resource")

                    severity_styles = {
                        "critical": "red",
                        "high": "yellow",
                        "medium": "blue",
                        "low": "dim"
                    }

                    for f in findings_list[:10]:
                        sev = f.get("severity", "medium")
                        style = severity_styles.get(sev.lower(), "white")
                        table.add_row(
                            f"[{style}]{sev.upper()}[/{style}]",
                            f.get("title", "N/A")[:50],
                            f.get("resource_type", "N/A")
                        )

                    console.print(table)
                    console.print(f"\n[dim]Showing {min(10, len(findings_list))} of {len(findings_list)} findings[/dim]")

            elif dashboard:
                data = api_request("/v2/compliances/dashboard/cloud-stats/")

                progress.remove_task(task)
                console.print("[green]Dashboard loaded![/green]")
                console.print("\n[bold]Cloud Security Dashboard[/bold]\n")

                score = data.get("security_score", 0)
                score_color = "green" if score >= 80 else "yellow"
                console.print(f"  Security Score:  [{score_color}]{score}[/{score_color}]")
                console.print(f"  Total Resources: [cyan]{data.get('total_resources', 0)}[/cyan]")
                console.print(f"  Open Findings:   [yellow]{data.get('open_findings', 0)}[/yellow]")

            else:
                progress.remove_task(task)
                console.print("[yellow]Usage: aribot cloud-security [--scan [provider]] [--findings] [--dashboard][/yellow]")

        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Cloud security operation failed: {e}[/red]")


@main.command()
@click.option("--methodologies", is_flag=True, help="List available threat modeling methodologies")
@click.option("--intelligence", is_flag=True, help="Get threat intelligence summary")
@click.option("--attack-paths", is_flag=True, help="Analyze attack paths (requires --diagram)")
@click.option("-d", "--diagram", help="Diagram ID for analysis")
@click.option("--analyze", help="Comprehensive threat analysis for diagram")
@click.option("--requirements", help="Generate security requirements for diagram")
@click.option("--ai-attack-paths", "ai_attack_paths", help="AI-powered attack path analysis")
@click.option("--ai-predict", "ai_predict", help="AI threat prediction using ML ensemble")
@click.option("--ai-insights", "ai_insights", help="Generate AI architecture insights")
@click.option("--patterns", help="Detect AI patterns in diagram")
def redteam(methodologies: bool, intelligence: bool, attack_paths: bool, diagram: Optional[str], analyze: Optional[str], requirements: Optional[str], ai_attack_paths: Optional[str], ai_predict: Optional[str], ai_insights: Optional[str], patterns: Optional[str]):
    """Red team attack simulation and threat analysis."""
    if methodologies:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching methodologies...", total=None)
            try:
                data = api_request("/v2/threat-engine/threat-models/")
                progress.remove_task(task)

                console.print("\n[bold]Threat Modeling Methodologies[/bold]\n")
                for m in data.get("supported_methodologies", []):
                    console.print(f"  [cyan]{m.get('name', 'N/A'):12}[/cyan] [dim]{m.get('description', '')}[/dim]")

                console.print("\n[bold]Risk Levels[/bold]\n")
                for r in data.get("risk_levels", []):
                    console.print(f"  [yellow]{r.get('name', 'N/A'):12}[/yellow] [dim]{r.get('description', '')}[/dim]")

                console.print("\n[bold]Compliance Frameworks[/bold]\n")
                for f in data.get("compliance_frameworks", []):
                    console.print(f"  [green]{f.get('name', 'N/A'):20}[/green] [dim]{f.get('description', '')}[/dim]")

                console.print("\n[bold]Engine Capabilities[/bold]\n")
                capabilities = data.get("capabilities", {})
                for cap, enabled in capabilities.items():
                    status = "[green]✓[/green]" if enabled else "[red]✗[/red]"
                    console.print(f"  {status} {cap.replace('_', ' ')}")

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]Failed to fetch methodologies: {e}[/red]")
        return

    if intelligence:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching threat intelligence...", total=None)
            try:
                data = api_request("/v2/threat-engine/threat-intelligence/")
                progress.remove_task(task)

                console.print("\n[bold]Threat Intelligence Summary[/bold]\n")
                console.print(f"  [cyan]Integration:[/cyan]     {data.get('integration_status', 'N/A').title()}")
                console.print(f"  [cyan]Cache TTL:[/cyan]       {data.get('cache_ttl', 'N/A')}s")
                console.print(f"  [cyan]Real-time Feeds:[/cyan] {'Enabled' if data.get('real_time_feeds') else 'Disabled'}")
                console.print(f"  [cyan]Correlation:[/cyan]     {'Enabled' if data.get('correlation_enabled') else 'Disabled'}")

                console.print("\n[bold]Supported Indicators[/bold]\n")
                for ind in data.get("supported_indicators", []):
                    console.print(f"  • {ind}")

                console.print("\n[bold]Vision 2040 Features[/bold]\n")
                features = data.get("vision_2040_features", {})
                for feat, enabled in features.items():
                    status = "[green]✓[/green]" if enabled else "[red]✗[/red]"
                    console.print(f"  {status} {feat.replace('_', ' ')}")

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]Failed to fetch threat intelligence: {e}[/red]")
        return

    if attack_paths:
        if not diagram:
            console.print("[red]Error: --attack-paths requires --diagram <diagram-id>[/red]")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing attack paths...", total=None)
            try:
                full_id = resolve_diagram_id(diagram)
                diagram_data = api_request(f"/v2/threat-modeling/diagrams/{full_id}/")

                # Build components and connections from diagram data
                components = []
                connections = []

                for comp in diagram_data.get("components", []):
                    components.append({
                        "id": comp.get("id"),
                        "name": comp.get("name", comp.get("label", "Unknown")),
                        "type": comp.get("type", "generic")
                    })

                for conn in diagram_data.get("connections", []):
                    connections.append({
                        "source": conn.get("source_id", conn.get("source")),
                        "target": conn.get("target_id", conn.get("target")),
                        "type": conn.get("type", "data_flow")
                    })

                # Find entry/exit points
                source_node = None
                target_node = None
                for comp in components:
                    comp_type = comp.get("type", "").lower()
                    if "user" in comp_type or "client" in comp_type or "external" in comp_type:
                        source_node = comp.get("id")
                    elif "database" in comp_type or "storage" in comp_type or "data" in comp_type:
                        target_node = comp.get("id")

                data = api_request(
                    "/v2/threat-engine/attack-paths/",
                    method="POST",
                    json_data={
                        "components": components,
                        "connections": connections,
                        "source_node": source_node,
                        "target_node": target_node
                    }
                )
                progress.remove_task(task)

                console.print(f"\n[bold]Attack Path Analysis[/bold] - {diagram_data.get('name', diagram)}\n")

                overall = data.get("overall_risk", {})
                risk_level = overall.get("level", "unknown")
                risk_color = {
                    "critical": "red",
                    "high": "red",
                    "medium": "yellow",
                    "low": "green"
                }.get(risk_level.lower(), "white")
                console.print(f"  [bold]Overall Risk:[/bold] [{risk_color}]{risk_level.upper()}[/{risk_color}] (Score: {overall.get('score', 'N/A')})")

                paths = data.get("attack_paths", [])
                if paths:
                    console.print(f"\n[bold]Attack Paths Found: {len(paths)}[/bold]\n")
                    for i, p in enumerate(paths[:5], 1):
                        console.print(f"  [yellow]Path {i}:[/yellow] {p.get('description', 'N/A')}")
                        console.print(f"    [dim]Risk: {p.get('risk_score', 'N/A')} | Complexity: {p.get('complexity', 'N/A')}[/dim]")
                        steps = p.get("steps", [])
                        if steps:
                            console.print(f"    [dim]Steps: {' → '.join(steps[:5])}{'...' if len(steps) > 5 else ''}[/dim]")
                else:
                    console.print("  [green]No critical attack paths identified![/green]")

                mitigations = data.get("mitigations", [])
                if mitigations:
                    console.print("\n[bold]Recommended Mitigations[/bold]\n")
                    for m in mitigations[:5]:
                        console.print(f"  • {m}")

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]Failed to analyze attack paths: {e}[/red]")
        return

    if analyze:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Running comprehensive analysis...", total=None)
            try:
                full_id = resolve_diagram_id(analyze)
                diagram_data = api_request(f"/v2/threat-modeling/diagrams/{full_id}/")

                # Use the V2 AI analysis endpoint
                data = api_request(
                    f"/v2/threat-modeling/diagrams/{full_id}/analyze-ai/",
                    method="POST",
                    json_data={
                        "analysis_type": "comprehensive",
                        "include_mitre": True,
                        "include_recommendations": True
                    }
                )
                progress.remove_task(task)

                console.print(f"\n[bold]Comprehensive Threat Analysis[/bold] - {diagram_data.get('name', analyze)}\n")

                analysis = data.get("analysis", data)
                risk_level = analysis.get("risk_level", "N/A")
                risk_color = "red" if risk_level == "critical" else "yellow"
                console.print(f"  [cyan]Risk Level:[/cyan]    [{risk_color}]{risk_level}[/{risk_color}]")
                console.print(f"  [cyan]Risk Score:[/cyan]    [red]{analysis.get('risk_score', analysis.get('overall_score', 'N/A'))}[/red]")
                console.print(f"  [cyan]Threats Found:[/cyan] [yellow]{analysis.get('threat_count', analysis.get('total_threats', 0))}[/yellow]")

                threats = analysis.get("threats", data.get("threats", []))
                if threats:
                    console.print("\n[bold]Top Threats[/bold]\n")
                    for t in threats[:5]:
                        severity = t.get("severity", "unknown")
                        sev_color = {"critical": "red", "high": "red", "medium": "yellow", "low": "green"}.get(severity.lower(), "white")
                        console.print(f"  [{sev_color}]●[/{sev_color}] {t.get('title', t.get('name', 'Unknown'))}")
                        console.print(f"    [dim]Category: {t.get('category', 'N/A')} | MITRE: {t.get('mitre_id', t.get('mitre_mapping', 'N/A'))}[/dim]")

                recommendations = analysis.get("recommendations", data.get("recommendations", []))
                if recommendations:
                    console.print("\n[bold]Top Recommendations[/bold]\n")
                    for r in recommendations[:3]:
                        console.print(f"  [green]→[/green] {r.get('title', r.get('description', r))}")

                console.print(f"\n[dim]Methodologies: {', '.join(analysis.get('methodologies', data.get('methodologies', ['STRIDE', 'PASTA', 'NIST'])))}[/dim]")

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]Failed to run comprehensive analysis: {e}[/red]")
        return

    if requirements:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating security requirements...", total=None)
            try:
                full_id = resolve_diagram_id(requirements)
                diagram_data = api_request(f"/v2/threat-modeling/diagrams/{full_id}/")

                threats = diagram_data.get("threats", [])
                threat_list = [{"name": t.get("name", "Threat"), "severity": t.get("severity", "medium")} for t in threats[:10]]

                data = api_request(
                    "/v2/threat-engine/security-requirements/",
                    method="POST",
                    json_data={
                        "threats": threat_list,
                        "context": f"Diagram: {diagram_data.get('name', 'Unknown')}"
                    }
                )
                progress.remove_task(task)

                console.print(f"\n[bold]Security Requirements[/bold] - {diagram_data.get('name', requirements)}\n")

                console.print(f"  [cyan]Total Requirements:[/cyan] {data.get('total_requirements', 0)}")

                reqs = data.get("requirements", [])
                if reqs:
                    for r in reqs[:10]:
                        priority = r.get("priority", "medium")
                        pri_color = {"critical": "red", "high": "red", "medium": "yellow", "low": "green"}.get(priority.lower(), "white")
                        console.print(f"\n  [{pri_color}][{priority.upper()}][/{pri_color}] {r.get('title', 'Requirement')}")
                        console.print(f"    [dim]{r.get('description', 'N/A')}[/dim]")

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]Failed to generate security requirements: {e}[/red]")
        return

    # AI-powered attack path analysis
    if ai_attack_paths:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Running AI-powered attack path analysis...", total=None)
            try:
                full_id = resolve_diagram_id(ai_attack_paths)
                diagram_data = api_request(f"/v2/threat-modeling/diagrams/{full_id}/")

                data = api_request(
                    "/v2/ai/ai-agents/analyze/",
                    method="POST",
                    json_data={
                        "diagram_data": {
                            "id": full_id,
                            "name": diagram_data.get("name"),
                            "components": diagram_data.get("components", []),
                            "connections": diagram_data.get("links", diagram_data.get("connections", []))
                        },
                        "context": {
                            "analysis_type": "attack_paths",
                            "include_knowledge_graph": True
                        }
                    }
                )
                progress.remove_task(task)

                console.print(f"\n[bold]AI Attack Path Analysis[/bold] - {diagram_data.get('name', ai_attack_paths)}\n")

                analysis = data.get("analysis", data)
                risk_level = analysis.get("risk_level", "N/A")
                console.print(f"  [cyan]Risk Level:[/cyan]     [{'red' if risk_level == 'critical' else 'yellow'}]{risk_level}[/{'red' if risk_level == 'critical' else 'yellow'}]")
                console.print(f"  [cyan]AI Confidence:[/cyan]  [green]{(analysis.get('confidence', 0.85) * 100):.0f}%[/green]")

                attack_paths = analysis.get("attack_paths", data.get("attack_paths", []))
                if attack_paths:
                    console.print(f"\n[bold]Identified Attack Paths ({len(attack_paths)})[/bold]\n")
                    for i, path in enumerate(attack_paths[:5], 1):
                        risk_score = path.get("risk_score", 0.5)
                        risk_color = "red" if risk_score > 0.7 else "yellow" if risk_score > 0.4 else "green"
                        console.print(f"  [bold]Path {i}:[/bold] {path.get('name', path.get('description', 'Attack Vector'))}")
                        console.print(f"    Risk Score:    [{risk_color}]{(risk_score * 100):.0f}%[/{risk_color}]")
                        console.print(f"    Attack Steps:  [cyan]{path.get('steps', path.get('hop_count', 'N/A'))}[/cyan]")
                        console.print(f"    Entry Point:   [yellow]{path.get('entry_point', path.get('source', 'External'))}[/yellow]")
                        console.print(f"    Target:        [red]{path.get('target', path.get('destination', 'Critical Asset'))}[/red]")
                else:
                    console.print("\n  [green]No critical attack paths identified![/green]")

                mitigations = analysis.get("mitigations", data.get("mitigations", []))
                if mitigations:
                    console.print("\n[bold]AI-Recommended Mitigations[/bold]\n")
                    for m in mitigations[:3]:
                        console.print(f"  [green]→[/green] {m.get('title', m.get('description', m))}")

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]AI attack path analysis failed: {e}[/red]")
        return

    # AI threat prediction
    if ai_predict:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Running AI threat prediction...", total=None)
            try:
                full_id = resolve_diagram_id(ai_predict)
                diagram_data = api_request(f"/v2/threat-modeling/diagrams/{full_id}/")

                data = api_request(
                    "/v2/threat-modeling/ml/ensemble-predict/",
                    method="POST",
                    json_data={
                        "diagram_data": {
                            "id": full_id,
                            "components": diagram_data.get("components", []),
                            "connections": diagram_data.get("links", [])
                        },
                        "threat_context": {
                            "industry": "technology",
                            "sensitivity": "high"
                        }
                    }
                )
                progress.remove_task(task)

                console.print(f"\n[bold]AI Threat Prediction[/bold] - {diagram_data.get('name', ai_predict)}\n")
                console.print(f"  [cyan]Model:[/cyan]          [green]ML Ensemble (STRIDE + PASTA + NIST)[/green]")

                predictions = data.get("predictions", data)
                console.print(f"  [cyan]Confidence:[/cyan]     [green]{(predictions.get('confidence', 0.92) * 100):.0f}%[/green]")
                risk_level = predictions.get("risk_level", "medium")
                console.print(f"  [cyan]Predicted Risk:[/cyan] [{'red' if risk_level == 'critical' else 'yellow'}]{risk_level}[/{'red' if risk_level == 'critical' else 'yellow'}]")

                threats = predictions.get("predicted_threats", predictions.get("threats", []))
                if threats:
                    console.print("\n[bold]Predicted Threats[/bold]\n")
                    for t in threats[:5]:
                        prob = t.get("probability", t.get("confidence", 0.8))
                        prob_color = "red" if prob > 0.8 else "yellow" if prob > 0.5 else "green"
                        console.print(f"  [{prob_color}][{(prob * 100):.0f}%][/{prob_color}] {t.get('title', t.get('name', 'Threat'))}")
                        console.print(f"    [dim]Category: {t.get('category', 'N/A')} | Impact: {t.get('impact', 'high')}[/dim]")

                emerging = predictions.get("emerging_threats", [])
                if emerging:
                    console.print("\n[bold]Emerging Threat Patterns[/bold]\n")
                    for t in emerging[:3]:
                        console.print(f"  [yellow]⚠[/yellow] {t.get('name', t.get('description', t))}")

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]AI threat prediction failed: {e}[/red]")
        return

    # AI architecture insights
    if ai_insights:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating AI architecture insights...", total=None)
            try:
                full_id = resolve_diagram_id(ai_insights)

                data = api_request(
                    f"/v2/threat-modeling/diagrams/{full_id}/generate-ai-insights/",
                    method="POST",
                    json_data={"include_recommendations": True}
                )
                progress.remove_task(task)

                console.print("\n[bold]AI Architecture Insights[/bold]\n")

                console.print(f"  [cyan]Diagram:[/cyan]          {data.get('diagram_name', 'N/A')}")
                console.print(f"  [cyan]Components:[/cyan]       [white]{data.get('component_count', 0)}[/white]")
                console.print(f"  [cyan]AI Provider:[/cyan]      [green]{data.get('provider', 'ai_agent')}[/green]")
                console.print(f"  [cyan]Generated:[/cyan]        [dim]{data.get('generated_at', 'now')}[/dim]")

                threats = data.get("threats", [])
                if threats:
                    console.print("\n[bold]Predicted Threats[/bold]\n")
                    for t in threats[:5]:
                        severity = t.get("severity", "medium")
                        severity_color = "red" if severity in ["critical", "high"] else "yellow"
                        console.print(f"  [{severity_color}]![/{severity_color}] {t.get('name', t.get('threat_id', 'Unknown'))}: {t.get('description', '')}")
                        if t.get("probability"):
                            console.print(f"    [dim]Probability: {t.get('probability') * 100:.0f}%[/dim]")
                else:
                    console.print("\n  [green]No critical threats identified.[/green]")

                recommendations = data.get("recommendations", [])
                if recommendations:
                    console.print("\n[bold]AI Recommendations[/bold]\n")
                    for r in recommendations[:5]:
                        rec_text = r if isinstance(r, str) else r.get('title', r.get('description', str(r)))
                        console.print(f"  [cyan]→[/cyan] {rec_text}")

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]AI insights generation failed: {e}[/red]")
        return

    # AI pattern detection
    if patterns:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Detecting AI patterns...", total=None)
            try:
                full_id = resolve_diagram_id(patterns)

                data = api_request(
                    "/v2/threat-modeling/ai-patterns/detect/",
                    method="POST",
                    json_data={
                        "diagram_id": full_id,
                        "sensitivity": "high"
                    }
                )
                progress.remove_task(task)

                console.print("\n[bold]AI Pattern Detection[/bold]\n")

                detection = data.get("detection", data)
                console.print(f"  [cyan]Patterns Found:[/cyan]    {detection.get('total_patterns', 0)}")
                console.print(f"  [cyan]Security Patterns:[/cyan] [yellow]{detection.get('security_patterns', 0)}[/yellow]")
                console.print(f"  [cyan]Risk Patterns:[/cyan]     [red]{detection.get('risk_patterns', 0)}[/red]")

                pattern_list = detection.get("patterns", data.get("patterns", []))
                if pattern_list:
                    console.print("\n[bold]Detected Patterns[/bold]\n")
                    for p in pattern_list[:5]:
                        p_type = p.get("type", "pattern")
                        type_color = "red" if p_type == "risk" else "green" if p_type == "security" else "cyan"
                        console.print(f"  [{type_color}][{p_type.upper()}][/{type_color}] {p.get('name', p.get('title', 'Pattern'))}")
                        console.print(f"    [dim]Confidence: {(p.get('confidence', 0.85) * 100):.0f}% | Impact: {p.get('impact', 'medium')}[/dim]")

                anomalies = detection.get("anomalies", [])
                if anomalies:
                    console.print("\n[bold]Detected Anomalies[/bold]\n")
                    for a in anomalies[:3]:
                        console.print(f"  [yellow]⚠[/yellow] {a.get('description', a.get('name', a))}")

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]AI pattern detection failed: {e}[/red]")
        return

    # Show help if no options provided
    console.print("[bold]Red Team Attack Simulation & Threat Analysis[/bold]\n")
    console.print("Usage:")
    console.print("  [cyan]aribot redteam --methodologies[/cyan]             List threat modeling methodologies")
    console.print("  [cyan]aribot redteam --intelligence[/cyan]              Get threat intelligence summary")
    console.print("  [cyan]aribot redteam --attack-paths -d <id>[/cyan]      Analyze attack paths for diagram")
    console.print("  [cyan]aribot redteam --analyze <id>[/cyan]              Comprehensive threat analysis")
    console.print("  [cyan]aribot redteam --requirements <id>[/cyan]         Generate security requirements")
    console.print("\n[bold]AI-Powered Commands[/bold]\n")
    console.print("  [green]aribot redteam --ai-attack-paths <id>[/green]    AI attack path analysis")
    console.print("  [green]aribot redteam --ai-predict <id>[/green]         AI threat prediction (ML)")
    console.print("  [green]aribot redteam --ai-insights <id>[/green]        Generate AI architecture insights")
    console.print("  [green]aribot redteam --patterns <id>[/green]           Detect AI patterns in diagram")


if __name__ == "__main__":
    main()
