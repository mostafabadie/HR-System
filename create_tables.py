import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect('hr.db')
cursor = conn.cursor()

# إنشاء جدول الرواتب
cursor.execute('''
CREATE TABLE IF NOT EXISTS payrolls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    salary REAL NOT NULL,
    bonus REAL DEFAULT 0,
    deductions REAL DEFAULT 0,
    net_salary REAL NOT NULL,
    payment_date TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
)
''')

conn.commit()
conn.close()

print("تم إنشاء جدول الرواتب بنجاح.")
