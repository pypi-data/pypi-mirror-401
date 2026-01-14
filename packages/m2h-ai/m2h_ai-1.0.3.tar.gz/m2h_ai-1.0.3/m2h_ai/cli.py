import json
import sys
import time
from pathlib import Path

# Replace colorama with rich
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich import print as rprint

# Your existing imports
from m2h_ai.core import ask_ai
from m2h_ai.update import check_for_update

# Initialize Rich Console
console = Console()

CONFIG_DIR = Path.home() / ".m2h-ai"
CONFIG_FILE = CONFIG_DIR / "config.json"


def banner():
    # Google style is minimal. No big ASCII art. 
    # Just a clean separator or header.
    console.print()
    console.rule("[bold blue]M2H AI CLI[/bold blue]")
    console.print("[dim italic center]Powered by M2H Web Solution[/dim italic center]")
    console.print()


def first_time_login():
    # Google style uses Panels for important context
    console.print(Panel(
        "OpenRouter API key required to continue.\n"
        "[dim]Your key will be stored locally in ~/.m2h-ai/config.json[/dim]",
        title="[bold yellow]Authentication[/bold yellow]",
        border_style="yellow",
        expand=False
    ))

    # Secure input (masked)
    key = Prompt.ask("Enter API key", password=True)

    if not key.startswith("sk-or-"):
        console.print("[bold red]❌ Error:[/bold red] Invalid OpenRouter key.")
        sys.exit(1)

    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": key}, f)

    console.print("[bold green]✅ Authenticated successfully![/bold green]\n")


def run():
    if not CONFIG_FILE.exists():
        first_time_login()

    # Check update silently or with a minimal status
    with console.status("[dim]Checking system...[/dim]", spinner="dots"):
        check_for_update()
    
    banner()

    console.print("[dim]Type 'exit' to quit.[/dim]\n")

    while True:
        try:
            # Clean prompt style
            q = console.input("[bold blue]m2h-ai[/bold blue] > ").strip()

            if q.lower() in ("exit", "quit"):
                console.print("\n[green]👋 Bye[/green]")
                break

            if not q:
                continue

            console.print() # Spacer

            # The "Google Style" spinner
            with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
                response = ask_ai(q)

            # Render the response as Markdown 
            # (Bold text will be bold, code blocks will be highlighted)
            console.print(Markdown(response))
            console.print() # Spacer
            console.rule(style="dim") # Subtle separator between turns
            console.print() # Spacer

        except KeyboardInterrupt:
            console.print("\n[green]👋 Bye[/green]")
            break

if __name__ == "__main__":
    run()