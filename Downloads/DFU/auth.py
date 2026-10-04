import sqlite3
import hashlib
import os

DB_PATH = "users.db"


def init_db():
    """Creates the users table if it doesn't exist yet. Safe to call every run."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def _hash_password(password, salt=None):
    """Simple salted SHA-256 hash. Good enough for a student project —
    not meant for production-grade security."""
    if salt is None:
        salt = os.urandom(16).hex()
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${h}"


def _verify_password(password, stored_hash):
    salt, _ = stored_hash.split("$")
    return _hash_password(password, salt) == stored_hash


def create_user(username, password):
    """Returns (success: bool, message: str)."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        return False, "Username already exists. Try logging in instead."

    password_hash = _hash_password(password)
    c.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    conn.commit()
    conn.close()
    return True, "Account created successfully."


def verify_user(username, password):
    """Returns (success: bool, message: str)."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()

    if not row:
        return False, "No account found with that username."

    if _verify_password(password, row[0]):
        return True, "Login successful."
    else:
        return False, "Incorrect password."