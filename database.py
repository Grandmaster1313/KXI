import sqlite3
import json

DB_PATH = r"C:\Users\herna\AppData\Local\com.fincept.terminal\data\cache.db"


def get_market_data(symbol_key):
    """
    Reads one market symbol from Fincept cache.db
    """

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT value
        FROM unified_cache
        WHERE key = ?
        """,
        (symbol_key,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return json.loads(row[0])