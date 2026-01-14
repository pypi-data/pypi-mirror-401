import warnings
import sys

# Suppress all warnings before importing anything else
warnings.filterwarnings("ignore")

# Also suppress urllib3 warning specifically
import urllib3
urllib3.disable_warnings()

"""CLI interface for AgentAuth using Typer and Rich."""

import logging
logging.disable(logging.INFO)

import json
import shutil
from datetime import datetime, timedelta
from getpass import getpass
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print as rprint

from agent_auth.client import (
    AgentAuthClient,
    AgentAuthClientError,
    SessionExpiredError,
    SessionNotFoundError,
)
from agent_auth.identity import Agent, AgentError, AgentNotFoundError, AgentScopeError
from agent_auth.vault import (
    Vault,
    VaultAuthenticationError,
    VaultError,
    VaultNotInitializedError,
)
from agent_auth.chrome_cookies import grab_chrome_cookies

logger = logging.getLogger(__name__)

# Create Typer app and Rich console
app = typer.Typer(
    name="agent-auth",
    help="AgentAuth - AI Agent session management SDK",
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
        console.print("[bold red]Vault is not initialized. Run 'agent-auth init' first.[/bold red]")
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
    """Initialize the vault with a master password."""
    console.print("[bold blue]Initializing AgentAuth vault...[/bold blue]")
    
    vault = Vault()
    
    # Check if vault already exists
    if vault.is_initialized():
        console.print("[yellow]Vault already initialized[/yellow]")
        console.print(f"[dim]Vault location: {vault.db_path}[/dim]")
        raise typer.Exit(0)
    
    # Vault doesn't exist - create it with auto-generated password
    try:
        vault.initialize()  # Generates random password and stores in Keychain
        console.print("[bold green]✓[/bold green] Vault initialized successfully!")
        console.print("[dim]Password stored securely in macOS Keychain[/dim]")
        console.print(f"[dim]Vault location: {vault.db_path}[/dim]")
    except VaultError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def add(domain: str):
    """Add a session for a domain."""
    console.print(f"[bold blue]Adding session for domain: {domain}[/bold blue]")
    
    vault = Vault()
    
    if not vault.is_initialized():
        console.print("[bold red]Vault is not initialized. Run 'agent-auth init' first.[/bold red]")
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
        console.print("Run: agent-auth grab <domain>")
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
            console.print(f"[red]Error:[/red] No session found for {domain}")
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
        console.print("[bold red]Vault is not initialized. Run 'agent-auth init' first.[/bold red]")
        raise typer.Exit(1)
    
    # Unlock vault automatically (password retrieved from Keychain)
    try:
        vault.unlock()  # Automatically retrieves password from Keychain
    except VaultAuthenticationError as e:
        console.print(f"[bold red]Error unlocking vault:[/bold red] {e}")
        raise typer.Exit(1)
    
    try:
        client = AgentAuthClient(agent, vault=vault)
        session = client.get_session(domain)
        
        console.print(f"[bold green]✓[/bold green] Session retrieved successfully!")
        console.print("\n[bold]Cookies:[/bold]")
        console.print(Panel(json.dumps(session, indent=2), title="Session Cookies"))
    except SessionNotFoundError as e:
        console.print(f"[bold red]Session not found:[/bold red] {e}")
        raise typer.Exit(1)
    except SessionExpiredError as e:
        console.print(f"[bold red]Session expired:[/bold red] {e}")
        raise typer.Exit(1)
    except AgentScopeError as e:
        console.print(f"[bold red]Scope error:[/bold red] {e}")
        raise typer.Exit(1)
    except AgentAuthClientError as e:
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
        keyring_password = keyring.get_password("AgentAuth", "vault")
    except Exception:
        pass  # Keyring might not have password, that's okay
    
    # If vault doesn't exist OR keyring password doesn't exist, set up everything
    if not vault.is_initialized() or keyring_password is None:
        # Generate a random password using token_hex(32) - 64 hex characters
        password = secrets.token_hex(32)
        
        # Store it in keyring
        try:
            keyring.set_password("AgentAuth", "vault", password)
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
            console.print(f"[yellow]No cookies found for domain: {domain}[/yellow]")
            console.print("[dim]Make sure you're logged into the site in Chrome.[/dim]")
            raise typer.Exit(0)
        
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
        
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
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
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    
    if not cookies:
        console.print(f"[red]Error:[/red] No cookies found for {domain}")
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
def version():
    """Show AgentAuth version."""
    console.print("AgentAuth v0.2.2")


@app.command()
def status():
    """Check vault status and stats."""
    import os
    
    vault_path = os.path.expanduser("~/.agent-auth/vault.db")
    
    if not os.path.exists(vault_path):
        console.print("[yellow]No vault found.[/yellow]")
        console.print("Run: agent-auth grab <domain> to get started")
        return
    
    vault_size = os.path.getsize(vault_path)
    vault_size_kb = vault_size / 1024
    
    vault = get_vault()
    
    try:
        sessions = vault.list_sessions()
    except VaultError as e:
        console.print(f"[bold red]Error listing sessions:[/bold red] {e}")
        raise typer.Exit(1)
    
    console.print("\n[bold]AgentAuth Status[/bold]\n")
    console.print(f"  Vault: ~/.agent-auth/vault.db ({vault_size_kb:.1f} KB)")
    console.print(f"  Sessions: {len(sessions)}")
    console.print(f"  Status: [green]Healthy[/green]")
    console.print()


@app.command()
def export():
    """Export the vault to a portable encrypted file."""
    vault = Vault()
    
    if not vault.is_initialized():
        console.print("[bold red]Vault is not initialized. Run 'agent-auth init' first.[/bold red]")
        raise typer.Exit(1)
    
    # Ensure vault directory exists
    vault.vault_dir.mkdir(parents=True, exist_ok=True)
    
    # Export path
    export_path = vault.vault_dir / "vault-export.enc"
    
    try:
        # Copy vault.db to vault-export.enc
        shutil.copy2(vault.db_path, export_path)
        # Show path with ~ for home directory
        export_path_str = str(export_path).replace(str(Path.home()), "~")
        console.print(f"Exported vault to {export_path_str}")
        console.print("Copy this file to your server and run: agent-auth import")
    except Exception as e:
        console.print(f"[bold red]Error exporting vault:[/bold red] {e}")
        raise typer.Exit(1)


@app.command(name="import")
def import_vault(file: str):
    """Import a vault file."""
    vault = Vault()
    
    # Ensure vault directory exists
    vault.vault_dir.mkdir(parents=True, exist_ok=True)
    
    # Source file path
    source_path = Path(file)
    if not source_path.exists():
        console.print(f"[bold red]File not found: {file}[/bold red]")
        raise typer.Exit(1)
    
    # Destination path
    dest_path = vault.db_path
    
    try:
        # Copy the file to vault.db
        shutil.copy2(source_path, dest_path)
        console.print("Imported vault successfully")
        console.print("Run 'agent-auth list' to see stored sessions")
    except Exception as e:
        console.print(f"[bold red]Error importing vault:[/bold red] {e}")
        raise typer.Exit(1)


def main():
    """Main entry point for CLI."""
    app()


# Typer app can also be called directly
if __name__ == "__main__":
    main()

