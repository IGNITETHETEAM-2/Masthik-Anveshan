"""
Masthik Anveshan - User Authentication & Credential Management Database
Provides SQLite database integration, password hashing via werkzeug.security,
user registration, authentication, session retrieval, and seed demo accounts.
"""

import os
import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')


def get_db_connection() -> sqlite3.Connection:
    """Creates a connection to SQLite database with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db():
    """Initializes users table and seeds pre-configured demo clinical accounts."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Neuroradiologist',
            institution TEXT NOT NULL DEFAULT 'Academic Medical Center',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    conn.commit()

    # Check if default demo accounts exist
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        demo_users = [
            (
                "Dr. Radhika Muvva, MD",
                "radhika@neuro.ai",
                generate_password_hash("password123"),
                "Chief Neuroradiologist",
                "Comprehensive Brain Tumor Institute"
            ),
            (
                "Dr. Akshay Kumar, PhD",
                "akshay@masthik.ai",
                generate_password_hash("password123"),
                "Senior Neuro-AI Researcher",
                "Neuro-Oncology Intelligence Lab"
            ),
            (
                "Dr. Jordan Patel, MD",
                "resident@hospital.org",
                generate_password_hash("password123"),
                "Neurosurgery Resident",
                "University Teaching Hospital"
            )
        ]

        cursor.executemany('''
            INSERT INTO users (name, email, password_hash, role, institution, created_at, last_login)
            VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        ''', demo_users)
        conn.commit()
        print(f"[Auth DB] Initialized database and seeded {len(demo_users)} verified clinical demo accounts.")

    conn.close()


def create_user(name: str, email: str, password: str, role: str = 'Neuroradiologist',
                institution: str = 'Academic Medical Center') -> Dict[str, Any]:
    """
    Registers a new clinical user. Hashes password using PBKDF2:SHA256.
    Returns dictionary with status and created user dict or error message.
    """
    email_clean = email.strip().lower()
    name_clean = name.strip()

    if not email_clean or not name_clean or not password:
        return {"status": "error", "message": "All required fields must be provided."}

    if len(password) < 6:
        return {"status": "error", "message": "Password must be at least 6 characters in length."}

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        pw_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (name, email, password_hash, role, institution, created_at, last_login)
            VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        ''', (name_clean, email_clean, pw_hash, role.strip(), institution.strip()))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        return {
            "status": "success",
            "user": {
                "id": user_id,
                "name": name_clean,
                "email": email_clean,
                "role": role.strip(),
                "institution": institution.strip()
            }
        }
    except sqlite3.IntegrityError:
        conn.close()
        return {"status": "error", "message": f"An account with email '{email_clean}' is already registered."}
    except Exception as e:
        conn.close()
        return {"status": "error", "message": f"Database registration error: {str(e)}"}


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Verifies user credentials. Returns user dictionary if valid, None otherwise.
    Updates last_login timestamp upon success.
    """
    email_clean = email.strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email_clean,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None

    if check_password_hash(row['password_hash'], password):
        # Update last_login
        cursor.execute("UPDATE users SET last_login = datetime('now') WHERE id = ?", (row['id'],))
        conn.commit()
        user_dict = {
            "id": row['id'],
            "name": row['name'],
            "email": row['email'],
            "role": row['role'],
            "institution": row['institution'],
            "created_at": row['created_at']
        }
        conn.close()
        return user_dict

    conn.close()
    return None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves user profile by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role, institution, created_at, last_login FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


if __name__ == '__main__':
    init_auth_db()
    print("Testing auth with demo user:")
    user = authenticate_user("radhika@neuro.ai", "password123")
    print("Authenticated:", user)
