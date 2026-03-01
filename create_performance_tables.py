import sqlite3

conn = sqlite3.connect("hr.db")
c = conn.cursor()

# جدول معايير التقييم
c.execute("""
CREATE TABLE IF NOT EXISTS evaluation_criteria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    weight REAL DEFAULT 1.0, -- وزن المعيار في التقييم الإجمالي
    is_active INTEGER DEFAULT 1 -- 1 للنشط، 0 للمعطل
);
""")

# جدول الفترات التقييمية (ربع سنوية)
c.execute("""
CREATE TABLE IF NOT EXISTS evaluation_periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, -- مثل "الربع الأول 2024"
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL, -- 1, 2, 3, 4
    status TEXT DEFAULT 'active', -- active, completed, draft
    created_date TEXT DEFAULT CURRENT_TIMESTAMP
);
""")

# جدول التقييمات الرئيسي
c.execute("""
CREATE TABLE IF NOT EXISTS performance_evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    evaluator_id INTEGER NOT NULL, -- مسؤول الموارد البشرية الذي أجرى التقييم
    overall_rating TEXT NOT NULL, -- ممتاز، جيد جداً، جيد، مقبول، ضعيف
    overall_score REAL, -- نقاط إجمالية محسوبة
    strengths TEXT, -- نقاط القوة
    areas_for_improvement TEXT, -- مجالات التحسين
    goals_next_period TEXT, -- أهداف الفترة القادمة
    comments TEXT, -- تعليقات إضافية
    status TEXT DEFAULT 'draft', -- draft, completed, approved
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    completed_date TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (period_id) REFERENCES evaluation_periods(id),
    FOREIGN KEY (evaluator_id) REFERENCES employees(id),
    UNIQUE(employee_id, period_id)
);
""")

# جدول تفاصيل التقييم لكل معيار
c.execute("""
CREATE TABLE IF NOT EXISTS evaluation_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluation_id INTEGER NOT NULL,
    criteria_id INTEGER NOT NULL,
    rating TEXT NOT NULL, -- ممتاز، جيد جداً، جيد، مقبول، ضعيف
    score REAL, -- نقاط المعيار (محسوبة من التقييم الوصفي)
    comments TEXT, -- تعليقات خاصة بهذا المعيار
    FOREIGN KEY (evaluation_id) REFERENCES performance_evaluations(id),
    FOREIGN KEY (criteria_id) REFERENCES evaluation_criteria(id),
    UNIQUE(evaluation_id, criteria_id)
);
""")

# جدول تاريخ التقييمات (لتتبع التغييرات)
c.execute("""
CREATE TABLE IF NOT EXISTS evaluation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluation_id INTEGER NOT NULL,
    action TEXT NOT NULL, -- created, updated, completed, approved
    changed_by INTEGER NOT NULL,
    change_date TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (evaluation_id) REFERENCES performance_evaluations(id),
    FOREIGN KEY (changed_by) REFERENCES employees(id)
);
""")

# إدراج معايير التقييم الافتراضية
c.execute("""
INSERT OR IGNORE INTO evaluation_criteria (name, description, weight) VALUES 
('الأداء الوظيفي', 'تقييم جودة العمل المنجز ومدى تحقيق المهام المطلوبة', 0.7),
('الالتزام بالمواعيد', 'تقييم الانضباط في الحضور والالتزام بمواعيد العمل والمهام', 0.3)
""")

# إدراج فترة تقييمية افتراضية (الربع الحالي)
current_year = 2024
current_quarter = 4

c.execute("""
INSERT OR IGNORE INTO evaluation_periods (name, start_date, end_date, year, quarter) VALUES 
('الربع الرابع 2024', '2024-10-01', '2024-12-31', ?, ?)
""", (current_year, current_quarter))

conn.commit()
conn.close()

print("تم إنشاء جداول إدارة الأداء بنجاح.")

