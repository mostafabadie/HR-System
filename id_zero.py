import sqlite3

conn = sqlite3.connect("hr.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM employees")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='employees'")

conn.commit()
conn.close()