import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
import questionary
from rich.table import Table 
import sys

from . import database, storage
from .models import LogEntry

console = Console(highlight=False)

def init():
    """Initialize the Devtrace storage system."""
    # Check if the DB file already exists
    if database.DB_PATH.exists():
        console.print("[yellow]Devtrace is already initialized.[/yellow]")
        console.print(f"📂 Storage location: {database.DB_DIR}")
        return

    try:
        database.init_db()
        console.print("[bold green]✅ Devtrace initialized successfully![/bold green]")
        console.print(f"📂 Storage location: {database.DB_DIR}")
    except Exception as e:
        console.print(f"[bold red]❌ Initialization failed:[/bold red] {e}")

def log(content: str):
    """Log a new entry with formatting support (\\n for newline, \\b for bullet)."""
    
    # We use r"\n" to look for the literal characters slash+n
    formatted_content = (
        content
        .replace(r"\n", "\n")       # Literal \n -> Actual Newline
        .replace(r"\b", "\n  • ")   # Literal \b -> Newline + Indent + Bullet
    )

    entry = LogEntry(content=formatted_content)
    
    database.insert_log(entry)
    storage.save_to_markdown(entry)
    
    # Show a preview of what was logged
    console.print(f"[green]✔[/green] Logged at [dim]{entry.timestamp.strftime('%H:%M')}[/dim]")

def see(date: str = typer.Argument("today", help="Date (YYYY-MM-DD), 'today', or 'yesterday'")):
    """View logs for a specific date."""
    
    # Parse the date argument
    target_dt = datetime.now()
    
    if date.lower() == "today":
        target_dt = datetime.now()
    elif date.lower() == "yesterday":
        target_dt = datetime.now() - timedelta(days=1)
    else:
        try:
            target_dt = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            console.print(f"[bold red]❌ Invalid date format: {date}[/bold red]")
            console.print("Please use YYYY-MM-DD, 'today', or 'yesterday'.")
            return

    target_date_str = target_dt.strftime("%Y-%m-%d")
    
    # Fetch logs from DB
    logs = database.get_logs_by_date(target_date_str)
    
    # Handle Empty State
    if not logs:
        console.print(f"[yellow]No logs found for {target_date_str}[/yellow]")
        return

    # Print Logs
    console.print(f"\n[bold white]{target_date_str}[/bold white]")

    for log in logs:
        dt = datetime.fromisoformat(log["timestamp"])
        time_str = dt.strftime("%H:%M")
        content = log["content"]

        prefix = f"> [{time_str}] "
        lines = content.splitlines()
        
        console.print(f"{prefix}{lines[0]}")
        
        padding = " " * len(prefix)
        
        for line in lines[1:]:
            console.print(f"{padding}{line}")
    
    console.print()

def view(month: str = typer.Argument(None, help="Month in YYYY-MM format. Defaults to current month.")):
    """Interactive month view."""
    
    # Default to current month if not provided
    target_month = month if month else datetime.now().strftime("%Y-%m")
    
    # Get dates from DB
    dates = database.get_active_dates_in_month(target_month)
    
    if not dates:
        console.print(f"[yellow]No logs found in {target_month}[/yellow]")
        return

    # Show the Interactive Menu
    # qmark="" removes the default '?' icon
    # pointer=">>" gives you the double arrow you wanted
    selected_date = questionary.select(
        f"Logs for {target_month}",
        choices=dates,
        qmark="",
        pointer=">>",
        use_indicator=True
    ).ask()

    # If user selected something (didn't press Ctrl+C), show the logs
    if selected_date:
        sys.stdout.write("\033[F\033[K")
        sys.stdout.flush()
        see(selected_date)

def help():
    """Show the Devtrace usage guide."""
    
    # 1. Create a table for commands
    table = Table(title="Devtrace Manual", show_header=True, header_style="bold cyan", border_style="dim")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description")
    table.add_column("Example", style="dim")

    # 2. Add rows
    table.add_row("init", "Setup the database folder (Run once)", "devtrace init")
    table.add_row("log", "Save a new work entry", 'devtrace log "Fixed bug"')
    table.add_row("see", "View logs for a date", "devtrace see yesterday")
    table.add_row("view", "Browse logs by month interactively", "devtrace view")
    table.add_row("help", "Show this message", "devtrace help")
    
    console.print(table)
    console.print() # Spacer

    # 3. Add a "Formatting Tips" section
    console.print("[bold cyan]Formatting Tips:[/bold cyan]")
    console.print("Use these markers inside your log message to structure your notes:\n")
    
    # We construct a little manual example
    console.print(r"  [white]\n[/white]   Creates a new line aligned with text.")
    console.print(r"  [white]\b[/white]   Creates a indented bullet point.")
    
    console.print("\n[dim]Example:[/dim]")
    console.print(r'  devtrace log "Refactored API \n Added validation \b Checked error 404"')
    console.print()