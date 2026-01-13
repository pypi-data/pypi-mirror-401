import sqlite3
from pathlib import Path
from .models import LogEntry

# Define where the DB lives
DB_DIR = Path.home() / ".devtrace"
DB_PATH = DB_DIR / "devtrace.db"

def init_db():
    """Creates the hidden directory and the database table."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            content TEXT,
            tags TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_log(entry: LogEntry):
    """Saves a log entry to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO logs (id, timestamp, content, tags) VALUES (?, ?, ?, ?)",
        (entry.id, entry.timestamp.isoformat(), entry.content, ",".join(entry.tags))
    )
    conn.commit()
    conn.close()

def get_logs_by_date(date_str: str):
    """Retrieve logs for a specific date string (YYYY-MM-DD)."""
    # Note: We use string matching on the timestamp for simplicity in v1
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    cursor = conn.cursor()
    
    query = "SELECT * FROM logs WHERE timestamp LIKE ? ORDER BY timestamp ASC"
    cursor.execute(query, (f"{date_str}%",))
    
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_active_dates_in_month(month_str: str) -> list[str]:
    """
    Returns a list of unique dates (YYYY-MM-DD) that have logs in the given month.
    month_str should be 'YYYY-MM' (e.g., '2026-01').
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # We grab the first 10 chars of timestamp (YYYY-MM-DD) and get unique ones
    query = """
        SELECT DISTINCT substr(timestamp, 1, 10) 
        FROM logs 
        WHERE timestamp LIKE ? 
        ORDER BY timestamp ASC
    """
    cursor.execute(query, (f"{month_str}%",))
    
    # Create a clean list of strings
    dates = [row[0] for row in cursor.fetchall()]
    conn.close()
    return dates