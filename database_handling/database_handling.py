import sqlite3
import uuid
from datetime import datetime


def init_db(database_file):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS renamed_files (
            id TEXT PRIMARY KEY,
            original_filename TEXT NOT NULL,
            new_filename TEXT NOT NULL,
            original_path TEXT NOT NULL,
            new_path TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            user TEXT
        )
    ''')
    connection.commit()
    connection.close()
    
    
def file_already_processed(database_file, original_path):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM renamed_files WHERE original_path = ?', (original_path,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def log_renamed_file(database_file, original_filename, new_filename, original_path, new_path, status, user):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO renamed_files (id, original_filename, new_filename, original_path, new_path, timestamp, status, user)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id, original_filename, new_filename, original_path, new_path, timestamp, status, user))
    conn.commit()
    conn.close()