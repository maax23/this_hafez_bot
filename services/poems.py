import sqlite3

# Database file path
database_file = 'database.db'

def get_poem(name:str) -> tuple:
    """
    Fetch a poem from the SQLite database by its identifier.

    Args:
        name (str): Poem file identifier (e.g. 'sh001').

    Returns:
        tuple | None: 
            A tuple of (file, text, interpretation, voice_id),
            or None if the poem does not exist.
    """
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()
        res = cursor.execute(
            "SELECT file, text, tabir, voice FROM poems WHERE file=?",
            (name,)
        )
        return res.fetchone()