import sqlite3


def ejecutar_query(query: str, params=()):
    with sqlite3.connect("basededatos.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)

            if query.strip().lower().startswith("select"):
                return cursor.fetchall()

            conn.commit()

            return None

        except Exception as e:
            print(e)
