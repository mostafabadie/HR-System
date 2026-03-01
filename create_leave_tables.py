import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect('hr.db')
cursor = conn.cursor()

# إنشاء جدول أنواع الإجازات
cursor.execute('''
CREATE TABLE IF NOT EXISTS leave_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    max_days INTEGER NOT NULL,
    description TEXT
)
''')

# إنشاء جدول طلبات الإجازات
cursor.execute('''
CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    leave_type_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    days_requested INTEGER NOT NULL,
    reason TEXT,
    status TEXT DEFAULT 'pending',
    request_date TEXT NOT NULL,
    approved_by INTEGER,
    approved_date TEXT,
    comments TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (leave_type_id) REFERENCES leave_types(id),
    FOREIGN KEY (approved_by) REFERENCES employees(id)
)
''')

# إنشاء جدول رصيد الإجازات للموظفين
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee_leave_balance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    leave_type_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    allocated_days INTEGER NOT NULL,
    used_days INTEGER DEFAULT 0,
    remaining_days INTEGER NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (leave_type_id) REFERENCES leave_types(id),
    UNIQUE(employee_id, leave_type_id, year)
)
''')

# إدراج أنواع الإجازات الافتراضية
default_leave_types = [
    ('إجازة سنوية', 21, 'الإجازة السنوية العادية'),
    ('إجازة مرضية', 15, 'إجازة للحالات المرضية'),
    ('إجازة طارئة', 5, 'إجازة للحالات الطارئة'),
    ('إجازة أمومة', 90, 'إجازة الأمومة للموظفات'),
    ('إجازة أبوة', 7, 'إجازة الأبوة للموظفين')
]

cursor.executemany('''
INSERT OR IGNORE INTO leave_types (name, max_days, description)
VALUES (?, ?, ?)
''', default_leave_types)

conn.commit()
conn.close()

print("تم إنشاء جداول الإجازات بنجاح.")

