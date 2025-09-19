import sqlite3

DB_FILE = "id_map.db"
MAX_IDS = 256  # Only 1-byte values: 0-255

def init_db():
    """Create the database and table if they don't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS id_map (
                long_id BLOB PRIMARY KEY,
                short_id INTEGER UNIQUE
            )
        ''')
        conn.commit()

def assign_id(long_id: bytes) -> int:
    """
    Retrieves the short ID for a given 12-byte long ID.
    If it doesn't exist, assigns the next available 1-byte ID.
    """
    if not isinstance(long_id, bytes) or len(long_id) != 12:
        raise ValueError("long_id must be 12 bytes")

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()

        # Check if the long ID is already assigned
        c.execute('SELECT short_id FROM id_map WHERE long_id = ?', (long_id,))
        row = c.fetchone()
        if row:
            return row[0]

        # Find used short IDs
        c.execute('SELECT short_id FROM id_map ORDER BY short_id')
        used_ids = {r[0] for r in c.fetchall()}

        # Find the next available short ID
        for candidate_id in range(MAX_IDS):
            if candidate_id not in used_ids:
                short_id = candidate_id
                break
        else:
            raise RuntimeError("No available short IDs (0–255 range exhausted)")

        # Assign and insert the new mapping
        c.execute(
            'INSERT INTO id_map (long_id, short_id) VALUES (?, ?)',
            (long_id, short_id)
        )
        conn.commit()
        return short_id

def get_short_id(long_id: bytes):
    """
    Returns the short ID for a given 12-byte long ID, or None if not assigned yet.
    """
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('SELECT short_id FROM id_map WHERE long_id = ?', (long_id,))
        row = c.fetchone()
        return row[0] if row else None

def reset_mapping():
    """
    Wipes all mappings (use with caution).
    """
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM id_map')
        conn.commit()
