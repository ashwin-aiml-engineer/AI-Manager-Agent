import sqlite3
import json
from datetime import datetime

DB_NAME = "history.db"

def init_db():
    """Creates the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create table for Sessions (Conversations)
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create table for Messages (The actual chat)
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_session(first_message):
    """Starts a new chat session."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Use the first 30 chars of the message as the Title
    title = first_message[:30] + "..."
    
    c.execute('INSERT INTO sessions (title) VALUES (?)', (title,))
    session_id = c.lastrowid
    
    conn.commit()
    conn.close()
    return session_id

def save_message(session_id, role, content):
    """Saves a single message to the DB."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # If content is a dict (like a chart image), convert to string
    if isinstance(content, dict):
        content = json.dumps(content)
        
    c.execute('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)', 
              (session_id, role, content))
    conn.commit()
    conn.close()

def load_messages(session_id):
    """Retrieves full history for a specific session."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC', (session_id,))
    rows = c.fetchall()
    
    messages = []
    for role, content in rows:
        # Check if it's a JSON string (for charts)
        try:
            if content.strip().startswith("{"):
                content = json.loads(content)
        except:
            pass
        messages.append({"role": role, "content": content})
        
    conn.close()
    return messages

def get_all_sessions():
    """Returns a list of all past conversations."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, title, created_at FROM sessions ORDER BY id DESC')
    sessions = c.fetchall()
    conn.close()
    return sessions

def delete_session(session_id):
    """Permanently deletes a session and its messages."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Delete messages first (Foreign Key cleanup)
    c.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
    # Delete the session itself
    c.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
    
    conn.commit()
    conn.close()
    
# Initialize immediately when imported
init_db()