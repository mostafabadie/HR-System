import sqlite3

conn = sqlite3.connect("hr.db")
c = conn.cursor()

# جدول لتخزين ملخص الحضور اليومي (لتحليلات أسهل)
c.execute("""
CREATE TABLE IF NOT EXISTS daily_attendance_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    total_hours_worked REAL DEFAULT 0,
    is_absent INTEGER DEFAULT 0, -- 0 for present, 1 for absent
    is_late INTEGER DEFAULT 0,    -- 0 for on time, 1 for late
    is_early_departure INTEGER DEFAULT 0, -- 0 for on time, 1 for early
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    UNIQUE(employee_id, date)
);
""")

# جدول لتخزين ملخص الرواتب الشهرية (لتحليلات أسهل)
c.execute("""
CREATE TABLE IF NOT EXISTS monthly_payroll_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    month TEXT NOT NULL, -- YYYY-MM format
    total_salary REAL NOT NULL,
    total_bonus REAL DEFAULT 0,
    total_deductions REAL DEFAULT 0,
    net_salary REAL NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    UNIQUE(employee_id, month)
);
""")

# جدول لتخزين ملخص استخدام الإجازات السنوي (لتحليلات أسهل)
c.execute("""
CREATE TABLE IF NOT EXISTS annual_leave_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    leave_type_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    days_allocated INTEGER NOT NULL,
    days_used INTEGER NOT NULL,
    days_remaining INTEGER NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (leave_type_id) REFERENCES leave_types(id),
    UNIQUE(employee_id, leave_type_id, year)
);
""")

conn.commit()
conn.close()

print("تم إنشاء جداول التقارير بنجاح.")

