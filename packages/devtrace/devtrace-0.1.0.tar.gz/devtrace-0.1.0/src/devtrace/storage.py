from pathlib import Path
import textwrap
from .models import LogEntry

ROOT_DIR = Path.home() / ".devtrace"

def save_to_markdown(entry: LogEntry):
    """Appends the log to a Markdown file: ~/.devtrace/YYYY/Month/DD.md"""
    
    # Determine the file path
    year = entry.timestamp.strftime("%Y")
    month = entry.timestamp.strftime("%B") # e.g., "January"
    day = entry.timestamp.strftime("%d")   # e.g., "10"
    
    folder_path = ROOT_DIR / year / month
    folder_path.mkdir(parents=True, exist_ok=True)
    
    file_path = folder_path / f"{day}.md"
    
    # Create a nice header if the file is new
    if not file_path.exists():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# Work Log: {entry.timestamp.strftime('%Y-%m-%d')}\n\n")
    time_str = entry.timestamp.strftime("%H:%M")

    lines = entry.content.splitlines()
    first_line = f"- [{time_str}] {lines[0]}"
    remaining_lines = []
    
    for line in lines[1:]:
        remaining_lines.append(f"    {line}")
    
    full_block = [first_line] + remaining_lines
    
    # Join them and add the hidden ID at the very end
    final_text = "\n".join(full_block) + f" \n"
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(final_text)