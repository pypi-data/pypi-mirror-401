import warnings
import sys

# Suppress all warnings before importing anything else
warnings.filterwarnings("ignore")

# Also suppress urllib3 warning specifically
import urllib3
urllib3.disable_warnings()

"""CLI interface for Romek using Typer and Rich."""

import logging
logging.disable(logging.INFO)

import json
import os
import shutil
from datetime import datetime, timedelta
from getpass import getpass
from pathlib import Path
from typing import List, Optional

try:
    import yaml
except ImportError:
    yaml = None

import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print as rprint

from romek.client import (
    RomekClient,
    RomekClientError,
    SessionExpiredError,
    SessionNotFoundError,
)
from romek.identity import Agent, AgentError, AgentNotFoundError, AgentScopeError
from romek.vault import (
    Vault,
    VaultAuthenticationError,
    VaultError,
    VaultNotInitializedError,
)
from romek.chrome_cookies import grab_chrome_cookies

logger = logging.getLogger(__name__)

# Create Typer app and Rich console
app = typer.Typer(
    name="romek",
    help="Romek - AI Agent session management SDK",
    add_completion=False,
)
console = Console()


def get_vault_password() -> str:
    """Prompt for vault password securely.
    
    Returns:
        The vault password
    """
    return getpass("Vault password: ")


def get_vault() -> Vault:
    """Get an unlocked vault instance.
    
    Returns:
        Unlocked Vault instance
        
    Raises:
        SystemExit: If vault is not initialized or unlock fails
    """
    vault = Vault()
    
    if not vault.is_initialized():
        console.print("[bold red]Vault is not initialized. Run 'romek init' first.[/bold red]")
        raise typer.Exit(1)
    
    try:
        vault.unlock()  # Automatically retrieves password from Keychain
    except VaultAuthenticationError as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    
    return vault


@app.command()
def init():
    """Initialize Romek config file (romek.yaml) in current directory."""
    if yaml is None:
        console.print("[bold red]PyYAML is required for config file support.[/bold red]")
        console.print("[dim]Install it with: pip install pyyaml[/dim]")
        raise typer.Exit(1)
    
    config_path = Path("romek.yaml")
    
    if config_path.exists():
        console.print("[yellow]romek.yaml already exists[/yellow]")
        if not Confirm.ask("Overwrite existing config file?"):
            raise typer.Exit(0)
    
    console.print("[bold blue]Creating romek.yaml...[/bold blue]")
    
    # Prompt for domains
    console.print("\n[bold]Enter domains to sync (comma or space separated, empty line to finish):[/bold]")
    console.print("[dim]Example: linkedin.com, github.com, gmail.com[/dim]")
    console.print("[dim]Or: linkedin.com github.com gmail.com[/dim]")
    
    domains = []
    while True:
        domain_input = Prompt.ask("Domain(s) (or press Enter to finish)", default="")
        if not domain_input.strip():
            break
        
        # Split by comma first, then by space
        # Handle both "domain1, domain2, domain3" and "domain1 domain2 domain3"
        potential_domains = []
        
        # First split by comma
        comma_split = [d.strip() for d in domain_input.split(',')]
        
        # Then split each by space (in case user mixes comma and space)
        for item in comma_split:
            if item:
                # Split by space and add each non-empty item
                space_split = [d.strip() for d in item.split() if d.strip()]
                potential_domains.extend(space_split)
        
        # Process each domain
        for domain_raw in potential_domains:
            if not domain_raw:
                continue
            domain = domain_raw.strip().lower()
            # Remove protocol if present
            domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
            if domain and domain not in domains:
                domains.append(domain)
    
    # Create config structure
    config = {
        "sessions": domains
    }
    
    # Write YAML file
    try:
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        console.print(f"[bold green]✓[/bold green] Created romek.yaml with {len(domains)} domain{'s' if len(domains) != 1 else ''}")
        if domains:
            console.print(f"[dim]Domains: {', '.join(domains)}[/dim]")
        else:
            console.print("[dim]No domains added. Edit romek.yaml to add domains.[/dim]")
    except Exception as e:
        console.print(f"[bold red]Error creating config file:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def add(domain: str):
    """Add a session for a domain."""
    console.print(f"[bold blue]Adding session for domain: {domain}[/bold blue]")
    
    vault = Vault()
    
    if not vault.is_initialized():
        console.print("[bold red]Vault is not initialized. Run 'romek init' first.[/bold red]")
        raise typer.Exit(1)
    
    try:
        vault.unlock()  # Automatically retrieves password from Keychain
    except VaultAuthenticationError as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    
    # Prompt for cookies JSON
    console.print("\n[bold]Enter cookies as JSON:[/bold]")
    console.print("[dim]Example: {\"session_id\": \"abc123\", \"auth_token\": \"xyz789\"}[/dim]")
    
    cookies_json = Prompt.ask("Cookies JSON")
    
    try:
        cookies = json.loads(cookies_json)
        if not isinstance(cookies, dict):
            raise ValueError("Cookies must be a JSON object (dictionary)")
    except json.JSONDecodeError as e:
        console.print(f"[bold red]Invalid JSON:[/bold red] {e}")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    
    # Prompt for expiration
    days = Prompt.ask("Expiration (days from now)", default="30")
    try:
        days_int = int(days)
        expires_at = datetime.utcnow() + timedelta(days=days_int)
    except ValueError:
        console.print("[bold red]Invalid number of days![/bold red]")
        raise typer.Exit(1)
    
    try:
        session = vault.store_session(
            domain=domain,
            cookies=cookies,
            expires_at=expires_at,
        )
        console.print(f"[bold green]✓[/bold green] Session stored successfully!")
        console.print(f"[dim]Expires: {expires_at.isoformat()}[/dim]")
    except VaultError as e:
        console.print(f"[bold red]Error storing session:[/bold red] {e}")
        raise typer.Exit(1)


@app.command(name="list")
def list_sessions():
    """List all stored sessions with details."""
    vault = get_vault()
    
    try:
        sessions = vault.list_sessions()
    except VaultError as e:
        console.print(f"[bold red]Error listing sessions:[/bold red] {e}")
        raise typer.Exit(1)
    
    if not sessions:
        console.print("No sessions stored yet.")
        console.print("Run: romek grab <domain>")
        return
    
    console.print("\n[bold]Stored sessions:[/bold]\n")
    now = datetime.utcnow()
    for session in sessions:
        domain = session.domain
        cookie_count = len(session.cookies)
        # Format expires date
        if session.expires_at < now:
            expires = f"{session.expires_at.strftime('%Y-%m-%d')} (expired)"
        else:
            expires = session.expires_at.strftime('%Y-%m-%d')
        console.print(f"  {domain}  ({cookie_count} cookies, expires {expires})")
    console.print()


@app.command()
def delete(domain: str):
    """Delete a stored session."""
    vault = get_vault()
    
    try:
        deleted = vault.delete_session(domain)
        if deleted:
            console.print(f"✓ Deleted session for {domain}")
        else:
            console.print(f"[bold red]No stored session for {domain}.[/bold red]")
            console.print(f"[dim]Run 'romek grab {domain}' first.[/dim]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def create_agent(
    name: str,
    scopes: Optional[str] = typer.Option(None, "--scopes", "-s", help="Comma-separated list of scopes"),
):
    """Create a new agent identity."""
    console.print(f"[bold blue]Creating agent: {name}[/bold blue]")
    
    # Parse scopes
    scope_list = []
    if scopes:
        scope_list = [s.strip() for s in scopes.split(",") if s.strip()]
    
    if not scope_list:
        # Prompt for scopes interactively
        console.print("\n[bold]Enter scopes (domains this agent can access):[/bold]")
        console.print("[dim]Example: linkedin.com,gmail.com[/dim]")
        scopes_input = Prompt.ask("Scopes (comma-separated)", default="")
        if scopes_input:
            scope_list = [s.strip() for s in scopes_input.split(",") if s.strip()]
    
    if not scope_list:
        console.print("[yellow]No scopes provided. Agent will be created without scopes.[/yellow]")
        if not Confirm.ask("Continue?"):
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Exit()
    
    try:
        agent = Agent.create(name, scope_list)
        console.print(f"[bold green]✓[/bold green] Agent created successfully!")
        console.print(f"[dim]Agent ID: {agent.identity.id}[/dim]")
        console.print(f"[dim]Scopes: {', '.join(agent.identity.scopes) if agent.identity.scopes else '(none)'}[/dim]")
    except AgentError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command(name="agents")
def list_agents():
    """List all registered agents."""
    console.print("[bold blue]Registered Agents[/bold blue]")
    
    try:
        agent_names = Agent.list_agents()
    except Exception as e:
        console.print(f"[bold red]Error listing agents:[/bold red] {e}")
        raise typer.Exit(1)
    
    if not agent_names:
        console.print("[yellow]No agents registered.[/yellow]")
        return
    
    # Load and display agent details
    table = Table(title="Registered Agents")
    table.add_column("Name", style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Scopes", style="yellow")
    table.add_column("Created", style="dim")
    
    for name in agent_names:
        try:
            agent = Agent.load(name)
            scopes_str = ", ".join(agent.identity.scopes) if agent.identity.scopes else "(none)"
            table.add_row(
                agent.identity.name,
                str(agent.identity.id)[:8] + "...",
                scopes_str,
                agent.identity.created_at.isoformat(),
            )
        except Exception as e:
            table.add_row(name, "[red]Error[/red]", str(e), "")
    
    console.print(table)


@app.command()
def test_session(
    agent_name: str,
    domain: str,
):
    """Test retrieving a session with an agent."""
    console.print(f"[bold blue]Testing session retrieval[/bold blue]")
    console.print(f"Agent: {agent_name}")
    console.print(f"Domain: {domain}\n")
    
    try:
        agent = Agent.load(agent_name)
    except AgentNotFoundError:
        console.print(f"[bold red]Agent '{agent_name}' not found![/bold red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error loading agent:[/bold red] {e}")
        raise typer.Exit(1)
    
    vault = Vault()
    
    if not vault.is_initialized():
        console.print("[bold red]Vault is not initialized. Run 'romek init' first.[/bold red]")
        raise typer.Exit(1)
    
    # Unlock vault automatically (password retrieved from Keychain)
    try:
        vault.unlock()  # Automatically retrieves password from Keychain
    except VaultAuthenticationError as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    
    try:
        client = RomekClient(agent, vault=vault)
        session = client.get_session(domain)
        
        console.print(f"[bold green]✓[/bold green] Session retrieved successfully!")
        console.print("\n[bold]Cookies:[/bold]")
        console.print(Panel(json.dumps(session, indent=2), title="Session Cookies"))
    except SessionNotFoundError as e:
        console.print(f"[bold red]No stored session for {domain}.[/bold red]")
        console.print(f"[dim]Run 'romek grab {domain}' first.[/dim]")
        raise typer.Exit(1)
    except SessionExpiredError as e:
        console.print(f"[bold red]Session expired:[/bold red] {e}")
        raise typer.Exit(1)
    except AgentScopeError as e:
        console.print(f"[bold red]Scope error:[/bold red] {e}")
        raise typer.Exit(1)
    except RomekClientError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def grab(
    domain: str,
    profile: str = typer.Option("Default", "--profile", "-p", help="Chrome profile name to use")
):
    """Grab cookies from Chrome and store them in the vault."""
    import keyring
    import secrets
    
    vault = Vault()
    
    # Check if we need to set up password in keyring
    keyring_password = None
    try:
        keyring_password = keyring.get_password("Romek", "vault")
    except Exception:
        pass  # Keyring might not have password, that's okay
    
    # If vault doesn't exist OR keyring password doesn't exist, set up everything
    if not vault.is_initialized() or keyring_password is None:
        # Generate a random password using token_hex(32) - 64 hex characters
        password = secrets.token_hex(32)
        
        # Store it in keyring
        try:
            keyring.set_password("Romek", "vault", password)
        except Exception as e:
            console.print(f"[bold red]Error storing password in Keychain:[/bold red] {e}")
            raise typer.Exit(1)
        
        # Initialize vault if it doesn't exist
        if not vault.is_initialized():
            try:
                vault.initialize(password)  # Use the generated password
            except VaultError as e:
                console.print(f"[bold red]Error initializing vault:[/bold red] {e}")
                raise typer.Exit(1)
    
    # Unlock vault automatically (password retrieved from Keychain)
    try:
        vault.unlock()  # Automatically retrieves password from Keychain
    except VaultAuthenticationError as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    
    # Grab cookies from Chrome
    try:
        console.print(f"==> Grabbing session for {domain}...")
        cookies = grab_chrome_cookies(domain, profile=profile)
        
        if not cookies:
            console.print(f"[bold red]No session found for {domain}. Are you logged in on Chrome?[/bold red]")
            raise typer.Exit(1)
        
        console.print(f"==> Found {len(cookies)} cookies")
        
        # Store in vault (default expiration: 30 days)
        expires_at = datetime.utcnow() + timedelta(days=30)
        session = vault.store_session(
            domain=domain,
            cookies=cookies,
            expires_at=expires_at,
        )
        
        console.print("==> Stored in vault")
        console.print()
        console.print(f"[green]{domain} session ready.[/green] Use [cyan]vault.get_session(\"{domain}\")[/cyan] in your agent.")
        console.print()
        console.print("⭐ If Romek saved you time, star us on GitHub: https://github.com/jacobgadek/romek")
        
    except RuntimeError as e:
        error_msg = str(e)
        # Handle specific error cases with helpful messages
        if "Chrome not detected" in error_msg:
            console.print("[bold red]Chrome not detected. Is Chrome installed?[/bold red]")
        elif "Chrome is open" in error_msg:
            console.print("[bold red]Chrome is open. Close Chrome and try again.[/bold red]")
        elif "No session found" in error_msg:
            console.print(f"[bold red]No session found for {domain}. Are you logged in on Chrome?[/bold red]")
        else:
            console.print(f"[bold red]Error:[/bold red] {error_msg}")
        raise typer.Exit(1)
    except Exception as e:
        # Check for database lock errors
        error_str = str(e).lower()
        if "locked" in error_str or "database is locked" in error_str:
            console.print("[bold red]Chrome is open. Close Chrome and try again.[/bold red]")
        else:
            console.print(f"[bold red]Unexpected error:[/bold red] {e}")
            import traceback
            traceback.print_exc()
        raise typer.Exit(1)


@app.command()
def refresh(
    domain: str,
    profile: str = typer.Option("Default", "--profile", "-p", help="Chrome profile name to use")
):
    """Re-grab cookies for a domain (updates existing session)."""
    console.print(f"==> Refreshing session for {domain}...")
    
    try:
        cookies = grab_chrome_cookies(domain, profile=profile)
    except RuntimeError as e:
        error_msg = str(e)
        # Handle specific error cases with helpful messages
        if "Chrome not detected" in error_msg:
            console.print("[bold red]Chrome not detected. Is Chrome installed?[/bold red]")
        elif "Chrome is open" in error_msg:
            console.print("[bold red]Chrome is open. Close Chrome and try again.[/bold red]")
        elif "No session found" in error_msg:
            console.print(f"[bold red]No session found for {domain}. Are you logged in on Chrome?[/bold red]")
        else:
            console.print(f"[bold red]Error:[/bold red] {error_msg}")
        raise typer.Exit(1)
    except Exception as e:
        # Check for database lock errors
        error_str = str(e).lower()
        if "locked" in error_str or "database is locked" in error_str:
            console.print("[bold red]Chrome is open. Close Chrome and try again.[/bold red]")
        else:
            console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        raise typer.Exit(1)
    
    if not cookies:
        console.print(f"[bold red]No session found for {domain}. Are you logged in on Chrome?[/bold red]")
        raise typer.Exit(1)
    
    vault = get_vault()
    
    # Store session with 30-day expiration (same as grab command)
    expires_at = datetime.utcnow() + timedelta(days=30)
    try:
        vault.store_session(domain, cookies, expires_at)
    except VaultError as e:
        console.print(f"[bold red]Error storing session:[/bold red] {e}")
        raise typer.Exit(1)
    
    console.print(f"==> Found {len(cookies)} cookies")
    console.print(f"==> Updated in vault")
    console.print()
    console.print(f"[green]{domain} session refreshed.[/green]")


@app.command()
def sync(
    profile: str = typer.Option("Default", "--profile", "-p", help="Chrome profile name to use")
):
    """Sync sessions from romek.yaml file."""
    if yaml is None:
        console.print("[bold red]PyYAML is required for config file support.[/bold red]")
        console.print("[dim]Install it with: pip install pyyaml[/dim]")
        raise typer.Exit(1)
    
    config_path = Path("romek.yaml")
    
    if not config_path.exists():
        console.print("[bold red]No romek.yaml found.[/bold red]")
        console.print("[dim]Run 'romek init' first.[/dim]")
        raise typer.Exit(1)
    
    # Read config file
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[bold red]Error reading romek.yaml:[/bold red] {e}")
        raise typer.Exit(1)
    
    if not config or "sessions" not in config:
        console.print("[bold red]Invalid romek.yaml format.[/bold red]")
        console.print("[dim]Expected 'sessions' key with list of domains.[/dim]")
        raise typer.Exit(1)
    
    domains = config.get("sessions", [])
    if not domains:
        console.print("[yellow]No domains found in romek.yaml[/yellow]")
        raise typer.Exit(0)
    
    console.print("Syncing sessions from romek.yaml...")
    console.print()
    
    # Initialize vault if needed
    import keyring
    import secrets
    
    vault = Vault()
    
    # Check if we need to set up password in keyring
    keyring_password = None
    try:
        keyring_password = keyring.get_password("Romek", "vault")
    except Exception:
        pass
    
    # If vault doesn't exist OR keyring password doesn't exist, set up everything
    if not vault.is_initialized() or keyring_password is None:
        password = secrets.token_hex(32)
        
        try:
            keyring.set_password("Romek", "vault", password)
        except Exception as e:
            console.print(f"[bold red]Error storing password in Keychain:[/bold red] {e}")
            raise typer.Exit(1)
        
        if not vault.is_initialized():
            try:
                vault.initialize(password)
            except VaultError as e:
                console.print(f"[bold red]Error initializing vault:[/bold red] {e}")
                raise typer.Exit(1)
    
    # Unlock vault
    try:
        vault.unlock()
    except VaultAuthenticationError as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    
    # Sync each domain
    success_count = 0
    failed_count = 0
    
    for domain in domains:
        try:
            cookies = grab_chrome_cookies(domain, profile=profile)
            
            if not cookies:
                console.print(f"❌ {domain} (not logged in)")
                failed_count += 1
                continue
            
            # Store in vault (default expiration: 30 days)
            expires_at = datetime.utcnow() + timedelta(days=30)
            vault.store_session(
                domain=domain,
                cookies=cookies,
                expires_at=expires_at,
            )
            
            console.print(f"✅ {domain} ({len(cookies)} cookies)")
            success_count += 1
            
        except RuntimeError as e:
            error_msg = str(e)
            if "Chrome not detected" in error_msg:
                console.print(f"❌ {domain} (Chrome not detected)")
            elif "Chrome is open" in error_msg:
                console.print(f"❌ {domain} (Chrome is open)")
            elif "No session found" in error_msg:
                console.print(f"❌ {domain} (not logged in)")
            else:
                console.print(f"❌ {domain} ({error_msg})")
            failed_count += 1
        except Exception as e:
            console.print(f"❌ {domain} (error: {e})")
            failed_count += 1
    
    console.print()
    console.print(f"Synced {success_count}/{len(domains)} sessions")


@app.command()
def doctor():
    """Check health of all sessions in romek.yaml."""
    if yaml is None:
        console.print("[bold red]PyYAML is required for config file support.[/bold red]")
        console.print("[dim]Install it with: pip install pyyaml[/dim]")
        raise typer.Exit(1)
    
    config_path = Path("romek.yaml")
    
    if not config_path.exists():
        console.print("[bold red]No romek.yaml found.[/bold red]")
        console.print("[dim]Run 'romek init' first.[/dim]")
        raise typer.Exit(1)
    
    # Read config file
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[bold red]Error reading romek.yaml:[/bold red] {e}")
        raise typer.Exit(1)
    
    if not config or "sessions" not in config:
        console.print("[bold red]Invalid romek.yaml format.[/bold red]")
        console.print("[dim]Expected 'sessions' key with list of domains.[/dim]")
        raise typer.Exit(1)
    
    domains = config.get("sessions", [])
    if not domains:
        console.print("[yellow]No domains found in romek.yaml[/yellow]")
        raise typer.Exit(0)
    
    console.print("Checking session health...")
    console.print()
    
    # Get vault (initialize if needed)
    vault = Vault()
    
    if not vault.is_initialized():
        # Vault not initialized - all sessions will be "Not found"
        ready_count = 0
        for domain in domains:
            console.print(f"[bold]{domain}[/bold]")
            console.print(f"├── Status: [red]❌ Not found[/red]")
            console.print(f"└── Run 'romek grab {domain}'")
            console.print()
        
        console.print(f"Health: {ready_count}/{len(domains)} sessions ready")
        raise typer.Exit(0)
    
    # Unlock vault
    try:
        vault.unlock()
    except VaultAuthenticationError as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    
    # Check each domain
    ready_count = 0
    
    for domain in domains:
        console.print(f"[bold]{domain}[/bold]")
        
        try:
            session = vault.get_session(domain)
            
            if session is None:
                console.print(f"├── Status: [red]❌ Not found[/red]")
                console.print(f"└── Run 'romek grab {domain}'")
                console.print()
                continue
            
            # Calculate status
            now = datetime.utcnow()
            time_until_expiry = session.expires_at - now
            hours_until_expiry = time_until_expiry.total_seconds() / 3600
            is_expired = hours_until_expiry < 0
            
            # Format expiry time
            if is_expired:
                time_since_expiry = abs(time_until_expiry)
                expires_formatted = _format_expiry_time(time_since_expiry, is_past=True)
                expires_str = f"Expired {expires_formatted}"
                status_icon = "❌"
                status_text = "[red]Expired[/red]"
            else:
                expires_formatted = _format_expiry_time(time_until_expiry, is_past=False)
                expires_str = f"in {expires_formatted}"
                if hours_until_expiry < 24:
                    status_icon = "⚠️"
                    status_text = "[yellow]Expiring Soon[/yellow]"
                    ready_count += 1  # Expiring soon is still ready
                else:
                    status_icon = "✅"
                    status_text = "[green]Fresh[/green]"
                    ready_count += 1
            
            console.print(f"├── Status: {status_icon} {status_text}")
            console.print(f"├── Cookies: {len(session.cookies)} stored")
            console.print(f"└── Expires: {expires_str}")
            console.print()
            
        except VaultError as e:
            console.print(f"├── Status: [red]❌ Error[/red]")
            console.print(f"└── {e}")
            console.print()
    
    console.print(f"Health: {ready_count}/{len(domains)} sessions ready")


@app.command()
def version():
    """Show Romek version."""
    console.print("Romek v0.3.0")


@app.command()
def status(domain: str):
    """Check status of a stored session for a domain."""
    vault = get_vault()
    
    try:
        session = vault.get_session(domain)
        if session is None:
            console.print(f"[bold red]No session found for {domain}.[/bold red]")
            console.print(f"[dim]Run 'romek grab {domain}' first.[/dim]")
            raise typer.Exit(1)
    except VaultError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    
    # Calculate relative times
    now = datetime.utcnow()
    time_since_grabbed = now - session.created_at
    time_until_expiry = session.expires_at - now
    
    # Format "grabbed" time
    grabbed_str = _format_relative_time(time_since_grabbed)
    
    # Determine status first (based on time until expiry)
    hours_until_expiry = time_until_expiry.total_seconds() / 3600
    is_expired = hours_until_expiry < 0
    
    if is_expired:
        status_icon = "❌"
        status_text = "[red]Expired[/red]"
        # Format as "Expired ~X ago"
        time_since_expiry = abs(time_until_expiry)
        expires_formatted = _format_expiry_time(time_since_expiry, is_past=True)
        expires_str = f"Expired {expires_formatted}"
    else:
        # Format as "in ~X" for future expiry
        expires_formatted = _format_expiry_time(time_until_expiry, is_past=False)
        expires_str = f"in {expires_formatted}"
        
        # Determine status for non-expired sessions
        if hours_until_expiry < 24:
            status_icon = "⚠️"
            status_text = "[yellow]Expiring Soon[/yellow]"
        else:
            status_icon = "✅"
            status_text = "[green]Fresh[/green]"
    
    # Display status
    console.print(f"\n[bold]{session.domain}[/bold]")
    console.print(f"├── Cookies: {len(session.cookies)} stored")
    console.print(f"├── Grabbed: {grabbed_str}")
    console.print(f"├── Expires: {expires_str}")
    console.print(f"└── Status: {status_icon} {status_text}")
    console.print()


def _format_expiry_time(timedelta_obj: timedelta, is_past: bool) -> str:
    """Format a timedelta for expiry display with ~ prefix.
    
    Args:
        timedelta_obj: The time difference (should be positive/abs value)
        is_past: True if this is a past time (expired), False if future
    
    Returns:
        Formatted string like "~4 weeks ago" or "~4 weeks"
    """
    total_seconds = abs(timedelta_obj.total_seconds())
    
    if total_seconds < 60:
        seconds = int(total_seconds)
        unit = "second" if seconds == 1 else "seconds"
        return f"~{seconds} {unit}{' ago' if is_past else ''}"
    elif total_seconds < 3600:
        minutes = int(total_seconds / 60)
        unit = "minute" if minutes == 1 else "minutes"
        return f"~{minutes} {unit}{' ago' if is_past else ''}"
    elif total_seconds < 86400:
        hours = int(total_seconds / 3600)
        unit = "hour" if hours == 1 else "hours"
        return f"~{hours} {unit}{' ago' if is_past else ''}"
    elif total_seconds < 604800:
        days = int(total_seconds / 86400)
        unit = "day" if days == 1 else "days"
        return f"~{days} {unit}{' ago' if is_past else ''}"
    else:
        weeks = int(total_seconds / 604800)
        unit = "week" if weeks == 1 else "weeks"
        return f"~{weeks} {unit}{' ago' if is_past else ''}"


def _format_relative_time(timedelta_obj: timedelta) -> str:
    """Format a timedelta as a human-readable relative time string.
    
    Examples:
        "2 hours ago" (for past times)
        "in 3 days" (for future times)
    """
    total_seconds = abs(timedelta_obj.total_seconds())
    is_past = timedelta_obj.total_seconds() > 0
    
    if total_seconds < 60:
        seconds = int(total_seconds)
        unit = "second" if seconds == 1 else "seconds"
        return f"{seconds} {unit} ago" if is_past else f"in {seconds} {unit}"
    elif total_seconds < 3600:
        minutes = int(total_seconds / 60)
        unit = "minute" if minutes == 1 else "minutes"
        return f"{minutes} {unit} ago" if is_past else f"in {minutes} {unit}"
    elif total_seconds < 86400:
        hours = int(total_seconds / 3600)
        unit = "hour" if hours == 1 else "hours"
        return f"{hours} {unit} ago" if is_past else f"in {hours} {unit}"
    elif total_seconds < 604800:
        days = int(total_seconds / 86400)
        unit = "day" if days == 1 else "days"
        return f"{days} {unit} ago" if is_past else f"in {days} {unit}"
    else:
        weeks = int(total_seconds / 604800)
        unit = "week" if weeks == 1 else "weeks"
        return f"{weeks} {unit} ago" if is_past else f"in {weeks} {unit}"


@app.command()
def export(
    domain: str,
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path (default: stdout)")
):
    """Export cookies for a domain as JSON (Playwright/Selenium compatible format)."""
    vault = get_vault()
    
    try:
        session = vault.get_session(domain)
        if session is None:
            console.print(f"[bold red]No stored session for {domain}.[/bold red]")
            console.print(f"[dim]Run 'romek grab {domain}' first.[/dim]")
            raise typer.Exit(1)
        
        # Convert simple dict format to Playwright/Selenium format
        # Playwright expects: [{name, value, domain, path, expires?, httpOnly?, secure?, sameSite?}]
        playwright_cookies = []
        for name, value in session.cookies.items():
            # Clean value (remove quotes if present)
            clean_value = str(value)
            if clean_value.startswith('"') and clean_value.endswith('"'):
                clean_value = clean_value[1:-1]
            if clean_value.startswith('\\"') and clean_value.endswith('\\"'):
                clean_value = clean_value[2:-2]
            
            cookie = {
                "name": str(name),
                "value": clean_value,
                "domain": f".{session.domain}" if not session.domain.startswith(".") else session.domain,
                "path": "/",
            }
            playwright_cookies.append(cookie)
        
        # Output JSON
        cookies_json = json.dumps(playwright_cookies, indent=2)
        
        if output:
            # Write to file
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(cookies_json)
            console.print(f"[green]✓[/green] Exported {len(playwright_cookies)} cookies to {output}")
        else:
            # Write to stdout
            print(cookies_json)
            
    except VaultError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error exporting cookies:[/bold red] {e}")
        raise typer.Exit(1)


@app.command(name="import")
def import_cookies(
    file: str,
    domain: Optional[str] = typer.Option(None, "--domain", "-d", help="Domain to associate with imported cookies")
):
    """Import cookies from a JSON file into the vault.
    
    Supports both Playwright/Selenium format (array of cookie objects) and simple dict format.
    """
    vault = get_vault()
    
    # Read JSON file
    file_path = Path(file)
    if not file_path.exists():
        console.print(f"[bold red]File not found: {file}[/bold red]")
        raise typer.Exit(1)
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        console.print("[bold red]Invalid JSON file. Expected array of cookies.[/bold red]")
        console.print(f"[dim]Error: {e}[/dim]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error reading file:[/bold red] {e}")
        raise typer.Exit(1)
    
    # Convert to simple dict format
    cookies = {}
    
    if isinstance(data, list):
        # Playwright/Selenium format: array of cookie objects
        if not data:
            console.print("[bold red]Invalid JSON file. Expected array of cookies.[/bold red]")
            console.print("[dim]The file contains an empty array.[/dim]")
            raise typer.Exit(1)
        
        # Try to extract domain from first cookie if not provided
        if not domain and data:
            cookie_domain = data[0].get("domain", "")
            if cookie_domain:
                # Remove leading dot if present
                if cookie_domain.startswith("."):
                    cookie_domain = cookie_domain[1:]
                domain = cookie_domain
        
        for cookie_obj in data:
            if not isinstance(cookie_obj, dict):
                console.print("[bold red]Invalid JSON file. Expected array of cookies.[/bold red]")
                console.print("[dim]Each cookie should be an object with 'name' and 'value' fields.[/dim]")
                raise typer.Exit(1)
            
            name = cookie_obj.get("name")
            value = cookie_obj.get("value")
            
            if name is None or value is None:
                console.print("[yellow]Warning: Skipping cookie with missing name or value[/yellow]")
                continue
            
            cookies[name] = value
            
    elif isinstance(data, dict):
        # Simple dict format: {name: value, ...}
        cookies = data
    else:
        console.print("[bold red]Invalid JSON file. Expected array of cookies.[/bold red]")
        console.print("[dim]The file should contain an array of cookie objects or a simple object.[/dim]")
        raise typer.Exit(1)
    
    if not cookies:
        console.print("[bold red]No cookies found in file[/bold red]")
        raise typer.Exit(1)
    
    if not domain:
        console.print("[bold red]Domain is required. Use --domain flag.[/bold red]")
        raise typer.Exit(1)
    
    # Normalize domain
    domain = domain.strip().lower().replace('https://', '').replace('http://', '').split('/')[0]
    
    # Store in vault (default expiration: 30 days)
    expires_at = datetime.utcnow() + timedelta(days=30)
    try:
        session = vault.store_session(
            domain=domain,
            cookies=cookies,
            expires_at=expires_at,
        )
        console.print(f"[green]✓[/green] Imported {len(cookies)} cookies for {domain}")
        console.print(f"[dim]Expires: {expires_at.strftime('%Y-%m-%d')}[/dim]")
    except VaultError as e:
        console.print(f"[bold red]Error storing session:[/bold red] {e}")
        raise typer.Exit(1)


def main():
    """Main entry point for CLI."""
    app()


# Typer app can also be called directly
if __name__ == "__main__":
    main()

