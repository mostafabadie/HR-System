import sqlite3
from datetime import datetime, timedelta

def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect("hr.db")
    conn.row_factory = sqlite3.Row
    return conn

# ====== وظائف تقارير الحضور ======
def get_daily_attendance_summary(start_date, end_date):
    """الحصول على ملخص الحضور اليومي لفترة معينة"""
    conn = get_db_connection()
    summary = conn.execute("""
        SELECT das.date, e.name as employee_name, das.total_hours_worked, 
               das.is_absent, das.is_late, das.is_early_departure
        FROM daily_attendance_summary das
        JOIN employees e ON das.employee_id = e.id
        WHERE das.date BETWEEN ? AND ?
        ORDER BY das.date, e.name
    """, (start_date, end_date)).fetchall()
    conn.close()
    return summary

def get_attendance_overview_by_date(start_date, end_date):
    """الحصول على نظرة عامة على الحضور (إجمالي الحاضرين، الغائبين، المتأخرين) حسب التاريخ"""
    conn = get_db_connection()
    overview = conn.execute("""
        SELECT date, 
               COUNT(*) as total_employees_recorded,
               SUM(CASE WHEN is_absent = 0 THEN 1 ELSE 0 END) as total_present,
               SUM(is_absent) as total_absent,
               SUM(is_late) as total_late
        FROM daily_attendance_summary
        WHERE date BETWEEN ? AND ?
        GROUP BY date
        ORDER BY date
    """, (start_date, end_date)).fetchall()
    conn.close()
    return overview

def get_employee_attendance_trend(employee_id, year):
    """الحصول على اتجاه حضور موظف معين خلال سنة"""
    conn = get_db_connection()
    trend = conn.execute("""
        SELECT date, total_hours_worked, is_absent, is_late
        FROM daily_attendance_summary
        WHERE employee_id = ? AND strftime("%Y", date) = ?
        ORDER BY date
    """, (employee_id, str(year))).fetchall()
    conn.close()
    return trend

# ====== وظائف تقارير الرواتب ======
def get_monthly_payroll_summary(year, month=None):
    """الحصول على ملخص الرواتب الشهرية لسنة معينة أو شهر معين"""
    conn = get_db_connection()
    query = """
        SELECT mps.month, e.name as employee_name, mps.total_salary, 
               mps.total_bonus, mps.total_deductions, mps.net_salary
        FROM monthly_payroll_summary mps
        JOIN employees e ON mps.employee_id = e.id
        WHERE strftime("%Y", mps.month || "-01") = ?
    """
    params = [str(year)]
    
    if month:
        query += " AND mps.month = ?"
        params.append(f"{year}-{month:02d}")
        
    query += " ORDER BY mps.month, e.name"
    
    summary = conn.execute(query, params).fetchall()
    conn.close()
    return summary

def get_total_payroll_by_month(year):
    """الحصول على إجمالي الرواتب الصافية حسب الشهر لسنة معينة"""
    conn = get_db_connection()
    total_payroll = conn.execute("""
        SELECT mps.month, SUM(mps.net_salary) as total_net_salary
        FROM monthly_payroll_summary mps
        WHERE strftime("%Y", mps.month || "-01") = ?
        GROUP BY mps.month
        ORDER BY mps.month
    """, (str(year),)).fetchall()
    conn.close()
    return total_payroll

# ====== وظائف تقارير الإجازات ======
def get_annual_leave_summary(year):
    """الحصول على ملخص استخدام الإجازات السنوي لجميع الموظفين"""
    conn = get_db_connection()
    summary = conn.execute("""
        SELECT als.year, e.name as employee_name, lt.name as leave_type_name,
               als.days_allocated, als.days_used, als.days_remaining
        FROM annual_leave_summary als
        JOIN employees e ON als.employee_id = e.id
        JOIN leave_types lt ON als.leave_type_id = lt.id
        WHERE als.year = ?
        ORDER BY e.name, lt.name
    """, (str(year),)).fetchall()
    conn.close()
    return summary

def get_leave_usage_by_type(year):
    """الحصول على إجمالي أيام الإجازات المستخدمة حسب نوع الإجازة لسنة معينة"""
    conn = get_db_connection()
    usage = conn.execute("""
        SELECT lt.name as leave_type_name, SUM(als.days_used) as total_days_used
        FROM annual_leave_summary als
        JOIN leave_types lt ON als.leave_type_id = lt.id
        WHERE als.year = ?
        GROUP BY lt.name
        ORDER BY total_days_used DESC
    """, (str(year),)).fetchall()
    conn.close()
    return usage

# ====== وظائف التحليلات التنبؤية (أمثلة بسيطة) ======
def predict_future_absenteeism(employee_id, months=3):
    """مثال بسيط للتنبؤ بالغياب المستقبلي بناءً على الأنماط السابقة"""
    conn = get_db_connection()
    # افتراض: نحصل على عدد أيام الغياب في آخر 6 أشهر
    past_absences = conn.execute("""
        SELECT COUNT(*) as absences
        FROM daily_attendance_summary
        WHERE employee_id = ? AND is_absent = 1
        AND date >= strftime("%Y-%m-%d", date("now", "-6 months"))
    """, (employee_id,)).fetchone()["absences"]
    conn.close()
    
    # هذا مجرد مثال بسيط جداً: متوسط الغياب الشهري
    avg_monthly_absences = past_absences / 6 if past_absences else 0
    predicted_absences = avg_monthly_absences * months
    
    return {"employee_id": employee_id, "predicted_absences_next_months": predicted_absences}

def predict_leave_demand(leave_type_id, months=3):
    """مثال بسيط للتنبؤ بالطلب على نوع معين من الإجازات"""
    conn = get_db_connection()
    # افتراض: نحصل على عدد أيام الإجازات المطلوبة في آخر 6 أشهر لنوع معين
    past_demand = conn.execute("""
        SELECT SUM(days_requested) as total_days
        FROM leave_requests
        WHERE leave_type_id = ? AND status = 'approved'
        AND request_date >= strftime("%Y-%m-%d", date("now", "-6 months"))
    """, (leave_type_id,)).fetchone()["total_days"]
    conn.close()
    
    avg_monthly_demand = past_demand / 6 if past_demand else 0
    predicted_demand = avg_monthly_demand * months
    
    return {"leave_type_id": leave_type_id, "predicted_demand_next_months": predicted_demand}

# ====== وظائف تحديث جداول الملخص (يجب تشغيلها بشكل دوري) ======
def update_daily_attendance_summary():
    """تحديث جدول ملخص الحضور اليومي بناءً على جدول attendance"""
    conn = get_db_connection()
    
    # جلب جميع سجلات الحضور التي لم يتم تلخيصها بعد (أو إعادة تلخيص اليوم الحالي)
    # يمكن تحسين هذا لجلب السجلات الجديدة فقط
    attendance_records = conn.execute("""
        SELECT a.employee_id, a.date, a.check_in, a.check_out
        FROM attendance a
    """).fetchall()
    
    for record in attendance_records:
        employee_id = record["employee_id"]
        date = record["date"]
        check_in_str = record["check_in"]
        check_out_str = record["check_out"]
        
        total_hours_worked = 0
        is_absent = 0
        is_late = 0
        is_early_departure = 0
        
        if check_in_str and check_out_str:
            check_in_time = datetime.strptime(check_in_str, ")%H:%M:%S").time()
            check_out_time = datetime.strptime(check_out_str, ")%H:%M:%S").time()
            
            # حساب ساعات العمل
            time_diff = datetime.combine(datetime.min, check_out_time) - datetime.combine(datetime.min, check_in_time)
            total_hours_worked = time_diff.total_seconds() / 3600.0
            
            # مثال بسيط لتحديد التأخر والمغادرة المبكرة (يمكن تحسينه)
            # افتراض: بداية الدوام 9:00، نهاية الدوام 17:00
            if check_in_time > datetime.strptime("09:00:00", "%H:%M:%S").time():
                is_late = 1
            if check_out_time < datetime.strptime("17:00:00", "%H:%M:%S").time():
                is_early_departure = 1
        else:
            is_absent = 1 # إذا لم يسجل دخول أو خروج، يعتبر غائباً
            
        conn.execute("""
            INSERT OR REPLACE INTO daily_attendance_summary 
            (employee_id, date, total_hours_worked, is_absent, is_late, is_early_departure)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (employee_id, date, total_hours_worked, is_absent, is_late, is_early_departure))
    
    conn.commit()
    conn.close()

def update_monthly_payroll_summary():
    """تحديث جدول ملخص الرواتب الشهرية بناءً على جدول payrolls"""
    conn = get_db_connection()
    
    # جلب جميع سجلات الرواتب التي لم يتم تلخيصها بعد (أو إعادة تلخيص الشهر الحالي)
    payroll_records = conn.execute("""
        SELECT employee_id, payment_date, net_salary, bonus, deductions
        FROM payrolls
    """).fetchall()
    
    monthly_data = {}
    for record in payroll_records:
        employee_id = record["employee_id"]
        payment_month = datetime.strptime(record["payment_date"], "%Y-%m-%d").strftime("%Y-%m")
        
        if (employee_id, payment_month) not in monthly_data:
            monthly_data[(employee_id, payment_month)] = {
                "total_salary": 0,
                "total_bonus": 0,
                "total_deductions": 0,
                "net_salary": 0
            }
        
        monthly_data[(employee_id, payment_month)]["total_salary"] += record["net_salary"] + record["deductions"] - record["bonus"] # افتراض: الراتب الأساسي
        monthly_data[(employee_id, payment_month)]["total_bonus"] += record["bonus"]
        monthly_data[(employee_id, payment_month)]["total_deductions"] += record["deductions"]
        monthly_data[(employee_id, payment_month)]["net_salary"] += record["net_salary"]
        
    for (employee_id, month), data in monthly_data.items():
        conn.execute("""
            INSERT OR REPLACE INTO monthly_payroll_summary
            (employee_id, month, total_salary, total_bonus, total_deductions, net_salary)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (employee_id, month, data["total_salary"], data["total_bonus"], 
              data["total_deductions"], data["net_salary"]))
    
    conn.commit()
    conn.close()

def update_annual_leave_summary():
    """تحديث جدول ملخص الإجازات السنوي بناءً على جدول leave_requests و employee_leave_balance"""
    conn = get_db_connection()
    
    # جلب جميع أرصدة الإجازات الحالية
    leave_balances = conn.execute("SELECT * FROM employee_leave_balance").fetchall()
    
    for balance in leave_balances:
        employee_id = balance["employee_id"]
        leave_type_id = balance["leave_type_id"]
        year = balance["year"]
        allocated_days = balance["allocated_days"]
        used_days = balance["used_days"]
        remaining_days = balance["remaining_days"]
        
        conn.execute("""
            INSERT OR REPLACE INTO annual_leave_summary
            (employee_id, leave_type_id, year, days_allocated, days_used, days_remaining)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (employee_id, leave_type_id, year, allocated_days, used_days, remaining_days))
    
    conn.commit()
    conn.close()

# وظيفة لتشغيل جميع وظائف التحديث
def run_all_summary_updates():
    update_daily_attendance_summary()
    update_monthly_payroll_summary()
    update_annual_leave_summary()
    print("تم تحديث جميع جداول الملخص بنجاح.")

# مثال على كيفية استخدام الوظائف (يمكن حذف هذا الجزء في الإنتاج)
if __name__ == "__main__":
    # تأكد من وجود بيانات في الجداول الأصلية (employees, attendance, payrolls, leave_requests, leave_types, employee_leave_balance)
    # قبل تشغيل وظائف التحديث
    
    # تشغيل التحديثات
    run_all_summary_updates()
    
    # أمثلة على جلب التقارير
    print("\n--- تقرير الحضور اليومي (آخر 30 يوم) ---")
    today = datetime.now().strftime("%Y-%m-%d")
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    attendance_summary = get_daily_attendance_summary(thirty_days_ago, today)
    for row in attendance_summary:
        print(row)
        
    print("\n--- نظرة عامة على الحضور حسب التاريخ (آخر 30 يوم) ---")
    attendance_overview = get_attendance_overview_by_date(thirty_days_ago, today)
    for row in attendance_overview:
        print(row)

    print("\n--- ملخص الرواتب الشهرية (للسنة الحالية) ---")
    current_year = datetime.now().year
    payroll_summary = get_monthly_payroll_summary(current_year)
    for row in payroll_summary:
        print(row)
        
    print("\n--- إجمالي الرواتب حسب الشهر (للسنة الحالية) ---")
    total_payroll = get_total_payroll_by_month(current_year)
    for row in total_payroll:
        print(row)

    print("\n--- ملخص استخدام الإجازات السنوي (للسنة الحالية) ---")
    leave_summary = get_annual_leave_summary(current_year)
    for row in leave_summary:
        print(row)
        
    print("\n--- إجمالي أيام الإجازات المستخدمة حسب النوع (للسنة الحالية) ---")
    leave_usage = get_leave_usage_by_type(current_year)
    for row in leave_usage:
        print(row)

    print("\n--- تنبؤ بالغياب المستقبلي للموظف رقم 1 (3 أشهر) ---")
    predicted_absences = predict_future_absenteeism(1, 3)
    print(predicted_absences)

    print("\n--- تنبؤ بالطلب على الإجازة السنوية (نوع الإجازة رقم 1) (3 أشهر) ---")
    predicted_leave_demand = predict_leave_demand(1, 3)
    print(predicted_leave_demand)


