import click
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .core import get_wifi_credentials, generate_qr_code_ascii, WiFiError

@click.command()
@click.option('--timeout', type=int, default=None, help='Clear screen and exit after N seconds.')
@click.option('--no-color', is_flag=True, help='Disable colored output.')
def cli(timeout, no_color):
    """Retrieves current Wi-Fi credentials and generates a QR code."""
    console = Console(no_color=no_color)

    try:
        with console.status("[bold green]Retrieving Wi-Fi credentials...", spinner="dots"):
            ssid, password, auth_type = get_wifi_credentials()
        
        qr_ascii, wifi_str = generate_qr_code_ascii(ssid, password, auth_type)
        
        # Create a nice layout
        message = Text()
        message.append(f"\nSSID: ", style="bold cyan")
        message.append(f"{ssid}\n")
        
        if password:
            message.append(f"Password: ", style="bold red")
            message.append(f"{password}\n")
        else:
            message.append("Network is Open (No Password)\n", style="bold yellow")
            
        message.append(f"\nScan this QR code to connect:", style="italic grey50")

        grid = Panel(
            Text.from_ansi(qr_ascii),
            title="[bold]Wi-Fi QR Code[/bold]",
            subtitle="wifi-qr-terminal",
            expand=False,
            border_style="green"
        )

        console.print(message)
        console.print(grid)
        
        if timeout:
            with console.status(f"[bold yellow]Clearing in {timeout} seconds...", spinner="clock"):
                time.sleep(timeout)
            console.clear()
            console.print("[bold red]Screen cleared for security.[/bold red]")

    except WiFiError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {e}")
        # Debug info could go here
        sys.exit(1)

if __name__ == '__main__':
    cli()
