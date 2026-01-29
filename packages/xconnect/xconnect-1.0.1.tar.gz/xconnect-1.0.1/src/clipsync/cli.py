import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import pyfiglet

console = Console()

def print_banner():
    banner_text = pyfiglet.figlet_format("XDT Labs", font="slant")
    console.print(banner_text, style="bold yellow")
    console.print("-" * 50, style="yellow")

@click.group()
def cli():
    """clipSync CLI - Professional Cross-Platform Clipboard Synchronization"""
    print_banner()

@cli.command()
def login():
    """Login and authenticate with Firebase"""
    from .auth import login_flow
    login_flow()

@cli.command()
def logout():
    """Logout and clear authentication"""
    from .auth import logout_user
    logout_user()
    click.echo("Logged out successfully.")

@cli.command()
def serve():
    """Start the clipboard synchronization service"""
    from .auth import get_auth
    from .monitor import start_service
    
    if not get_auth():
        click.echo("Not logged in. Please run 'csync login' first.")
        return
    
    start_service()

@cli.command()
def stop():
    """Stop the clipboard synchronization service"""
    from .monitor import stop_service
    stop_service()

@cli.command()
def rename():
    """Rename this device"""
    from .auth import get_auth, rename_device
    
    if not get_auth():
        click.echo("Not logged in. Please run 'csync login' first.")
        return
    
    new_name = click.prompt("Enter new device name")
    if rename_device(new_name):
        click.echo(f"Device renamed to: {new_name}")
    else:
        click.echo("Failed to rename device. Please try again.")

def main():
    cli()

if __name__ == "__main__":
    main()
