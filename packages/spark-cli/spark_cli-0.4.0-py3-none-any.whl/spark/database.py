"""Database setup and operations"""
import sqlite3
from pathlib import Path
from typing import Optional


def get_db_path() -> Path:
    """Get the path to the SQLite database"""
    spark_dir = Path.home() / ".spark"
    spark_dir.mkdir(exist_ok=True)
    return spark_dir / "snippets.db"


def init_db() -> sqlite3.Connection:
    """Initialize database and return connection"""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Migration: Add tags column if it doesn't exist
    try:
        conn.execute("ALTER TABLE snippets ADD COLUMN tags TEXT")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    conn.commit()
    
    return conn


def save_snippet(command: str, tags: Optional[str] = None) -> int:
    """Save a new snippet and return its ID"""
    conn = init_db()
    cursor = conn.execute("INSERT INTO snippets (command, tags) VALUES (?, ?)", (command, tags))
    snippet_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return snippet_id


def find_snippets(search_term: str) -> list:
    """Find snippets containing search term in command or tags"""
    conn = init_db()
    cursor = conn.execute(
        "SELECT id, command, tags, created_at FROM snippets WHERE command LIKE ? OR tags LIKE ? ORDER BY created_at DESC",
        (f"%{search_term}%", f"%{search_term}%")
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_all_snippets(tag_filter: Optional[str] = None) -> list:
    """Get all snippets, optionally filtered by tag"""
    conn = init_db()
    if tag_filter:
        cursor = conn.execute(
            "SELECT id, command, tags, created_at FROM snippets WHERE tags LIKE ? ORDER BY created_at DESC",
            (f"%{tag_filter}%",)
        )
    else:
        cursor = conn.execute(
            "SELECT id, command, tags, created_at FROM snippets ORDER BY created_at DESC"
        )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_snippet_by_id(snippet_id: int) -> Optional[dict]:
    """Get a snippet by ID"""
    conn = init_db()
    cursor = conn.execute(
        "SELECT id, command, tags, created_at FROM snippets WHERE id = ?",
        (snippet_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def command_exists(command: str) -> Optional[dict]:
    """Check if a command already exists exactly. Returns snippet dict if found, None otherwise"""
    conn = init_db()
    cursor = conn.execute(
        "SELECT id, command, tags, created_at FROM snippets WHERE command = ?",
        (command,)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_snippet(snippet_id: int) -> bool:
    """Delete a snippet by ID. Returns True if deleted, False if not found"""
    conn = init_db()
    cursor = conn.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def find_snippets_by_text(search_text: str) -> list:
    """Find all snippets containing the search text. Returns list of snippet dicts"""
    conn = init_db()
    cursor = conn.execute(
        "SELECT id, command, tags, created_at FROM snippets WHERE command LIKE ?",
        (f"%{search_text}%",)
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def delete_snippets_by_text(search_text: str) -> int:
    """Delete all snippets containing the search text. Returns number of deleted snippets"""
    conn = init_db()
    cursor = conn.execute("DELETE FROM snippets WHERE command LIKE ?", (f"%{search_text}%",))
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted_count


def clear_all_snippets() -> int:
    """Delete all snippets and reset ID sequence. Returns number of deleted snippets"""
    conn = init_db()
    cursor = conn.execute("SELECT COUNT(*) FROM snippets")
    count = cursor.fetchone()[0]
    conn.execute("DELETE FROM snippets")
    # Reset the AUTOINCREMENT sequence
    conn.execute("DELETE FROM sqlite_sequence WHERE name='snippets'")
    conn.commit()
    conn.close()
    return count

