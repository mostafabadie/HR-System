import sqlite3

conn = sqlite3.connect("hr.db")
cur = conn.cursor()
cur.execute("""
        CREATE TABLE IF NOT EXISTS leaves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            start_date TEXT,
            end_date TEXT,
            type TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Pending',
            days INTEGER,
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    """)
conn.commit()
conn.close()
