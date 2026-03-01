import sqlite3
from datetime import datetime, timedelta

def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect('hr.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_leave_days(start_date, end_date):
    """حساب عدد أيام الإجازة (باستثناء عطلة نهاية الأسبوع)"""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    days = 0
    current_date = start
    while current_date <= end:
        # تجاهل السبت والأحد (عطلة نهاية الأسبوع)
        if current_date.weekday() < 5:  # 0-4 هي أيام العمل
            days += 1
        current_date += timedelta(days=1)
    
    return days

def get_employee_leave_balance(employee_id, leave_type_id, year=None):
    """الحصول على رصيد الإجازات للموظف"""
    if year is None:
        year = datetime.now().year
    
    conn = get_db_connection()
    balance = conn.execute('''
        SELECT * FROM employee_leave_balance 
        WHERE employee_id = ? AND leave_type_id = ? AND year = ?
    ''', (employee_id, leave_type_id, year)).fetchone()
    conn.close()
    
    return balance

def create_leave_balance_for_employee(employee_id, year=None):
    """إنشاء رصيد إجازات للموظف للسنة الحالية"""
    if year is None:
        year = datetime.now().year
    
    conn = get_db_connection()
    
    # الحصول على جميع أنواع الإجازات
    leave_types = conn.execute('SELECT * FROM leave_types').fetchall()
    
    for leave_type in leave_types:
        # التحقق من وجود رصيد للموظف لهذا النوع من الإجازة
        existing = conn.execute('''
            SELECT * FROM employee_leave_balance 
            WHERE employee_id = ? AND leave_type_id = ? AND year = ?
        ''', (employee_id, leave_type['id'], year)).fetchone()
        
        if not existing:
            # إنشاء رصيد جديد
            conn.execute('''
                INSERT INTO employee_leave_balance 
                (employee_id, leave_type_id, year, allocated_days, used_days, remaining_days)
                VALUES (?, ?, ?, ?, 0, ?)
            ''', (employee_id, leave_type['id'], year, leave_type['max_days'], leave_type['max_days']))
    
    conn.commit()
    conn.close()

def submit_leave_request(employee_id, leave_type_id, start_date, end_date, reason):
    """تقديم طلب إجازة"""
    conn = get_db_connection()
    
    # حساب عدد الأيام المطلوبة
    days_requested = calculate_leave_days(start_date, end_date)
    
    # التحقق من الرصيد المتاح
    balance = get_employee_leave_balance(employee_id, leave_type_id)
    
    if not balance:
        # إنشاء رصيد إذا لم يكن موجوداً
        create_leave_balance_for_employee(employee_id)
        balance = get_employee_leave_balance(employee_id, leave_type_id)
    
    if balance['remaining_days'] < days_requested:
        conn.close()
        return False, "الرصيد المتاح غير كافي"
    
    # إدراج طلب الإجازة
    request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''
        INSERT INTO leave_requests 
        (employee_id, leave_type_id, start_date, end_date, days_requested, reason, request_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (employee_id, leave_type_id, start_date, end_date, days_requested, reason, request_date))
    
    conn.commit()
    conn.close()
    
    return True, "تم تقديم طلب الإجازة بنجاح"

def approve_leave_request(request_id, approved_by, comments=None):
    """الموافقة على طلب إجازة"""
    conn = get_db_connection()
    
    # الحصول على تفاصيل الطلب
    request = conn.execute('''
        SELECT * FROM leave_requests WHERE id = ?
    ''', (request_id,)).fetchone()
    
    if not request or request['status'] != 'pending':
        conn.close()
        return False, "الطلب غير موجود أو تم التعامل معه مسبقاً"
    
    # تحديث حالة الطلب
    approved_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''
        UPDATE leave_requests 
        SET status = 'approved', approved_by = ?, approved_date = ?, comments = ?
        WHERE id = ?
    ''', (approved_by, approved_date, comments, request_id))
    
    # تحديث رصيد الإجازات
    conn.execute('''
        UPDATE employee_leave_balance 
        SET used_days = used_days + ?, remaining_days = remaining_days - ?
        WHERE employee_id = ? AND leave_type_id = ? AND year = ?
    ''', (request['days_requested'], request['days_requested'], 
          request['employee_id'], request['leave_type_id'], datetime.now().year))
    
    conn.commit()
    conn.close()
    
    return True, "تم الموافقة على الطلب بنجاح"

def reject_leave_request(request_id, approved_by, comments=None):
    """رفض طلب إجازة"""
    conn = get_db_connection()
    
    # الحصول على تفاصيل الطلب
    request = conn.execute('''
        SELECT * FROM leave_requests WHERE id = ?
    ''', (request_id,)).fetchone()
    
    if not request or request['status'] != 'pending':
        conn.close()
        return False, "الطلب غير موجود أو تم التعامل معه مسبقاً"
    
    # تحديث حالة الطلب
    approved_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''
        UPDATE leave_requests 
        SET status = 'rejected', approved_by = ?, approved_date = ?, comments = ?
        WHERE id = ?
    ''', (approved_by, approved_date, comments, request_id))
    
    conn.commit()
    conn.close()
    
    return True, "تم رفض الطلب"

def get_employee_leave_requests(employee_id):
    """الحصول على طلبات الإجازة للموظف"""
    conn = get_db_connection()
    
    requests = conn.execute('''
        SELECT lr.*, lt.name as leave_type_name, e.name as approved_by_name
        FROM leave_requests lr
        JOIN leave_types lt ON lr.leave_type_id = lt.id
        LEFT JOIN employees e ON lr.approved_by = e.id
        WHERE lr.employee_id = ?
        ORDER BY lr.request_date DESC
    ''', (employee_id,)).fetchall()
    
    conn.close()
    return requests

def get_all_leave_requests():
    """الحصول على جميع طلبات الإجازة للمديرين"""
    conn = get_db_connection()
    
    requests = conn.execute('''
        SELECT lr.*, lt.name as leave_type_name, emp.name as employee_name, 
               mgr.name as approved_by_name
        FROM leave_requests lr
        JOIN leave_types lt ON lr.leave_type_id = lt.id
        JOIN employees emp ON lr.employee_id = emp.id
        LEFT JOIN employees mgr ON lr.approved_by = mgr.id
        ORDER BY lr.request_date DESC
    ''').fetchall()
    
    conn.close()
    return requests

def get_pending_leave_requests():
    """الحصول على طلبات الإجازة المعلقة"""
    conn = get_db_connection()
    
    requests = conn.execute('''
        SELECT lr.*, lt.name as leave_type_name, emp.name as employee_name
        FROM leave_requests lr
        JOIN leave_types lt ON lr.leave_type_id = lt.id
        JOIN employees emp ON lr.employee_id = emp.id
        WHERE lr.status = 'pending'
        ORDER BY lr.request_date ASC
    ''').fetchall()
    
    conn.close()
    return requests

def get_employee_leave_balances(employee_id, year=None):
    """الحصول على رصيد جميع أنواع الإجازات للموظف"""
    if year is None:
        year = datetime.now().year
    
    conn = get_db_connection()
    
    balances = conn.execute('''
        SELECT elb.*, lt.name as leave_type_name
        FROM employee_leave_balance elb
        JOIN leave_types lt ON elb.leave_type_id = lt.id
        WHERE elb.employee_id = ? AND elb.year = ?
    ''', (employee_id, year)).fetchall()
    
    conn.close()
    return balances

