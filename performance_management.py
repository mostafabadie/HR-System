import sqlite3
from datetime import datetime, timedelta

def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect("hr.db")
    conn.row_factory = sqlite3.Row
    return conn

# ====== وظائف إدارة معايير التقييم ======
def get_evaluation_criteria():
    """الحصول على جميع معايير التقييم النشطة"""
    conn = get_db_connection()
    criteria = conn.execute("""
        SELECT * FROM evaluation_criteria 
        WHERE is_active = 1 
        ORDER BY name
    """).fetchall()
    conn.close()
    return criteria

def add_evaluation_criteria(name, description, weight=1.0):
    """إضافة معيار تقييم جديد"""
    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO evaluation_criteria (name, description, weight)
            VALUES (?, ?, ?)
        """, (name, description, weight))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# ====== وظائف إدارة الفترات التقييمية ======
def get_evaluation_periods():
    """الحصول على جميع الفترات التقييمية"""
    conn = get_db_connection()
    periods = conn.execute("""
        SELECT * FROM evaluation_periods 
        ORDER BY year DESC, quarter DESC
    """).fetchall()
    conn.close()
    return periods

def get_active_evaluation_period():
    """الحصول على الفترة التقييمية النشطة"""
    conn = get_db_connection()
    period = conn.execute("""
        SELECT * FROM evaluation_periods 
        WHERE status = 'active' 
        ORDER BY year DESC, quarter DESC 
        LIMIT 1
    """).fetchone()
    conn.close()
    return period

def create_evaluation_period(name, start_date, end_date, year, quarter):
    """إنشاء فترة تقييمية جديدة"""
    conn = get_db_connection()
    cursor = conn.execute("""
        INSERT INTO evaluation_periods (name, start_date, end_date, year, quarter)
        VALUES (?, ?, ?, ?, ?)
    """, (name, start_date, end_date, year, quarter))
    conn.commit()
    period_id = cursor.lastrowid
    conn.close()
    return period_id

# ====== وظائف التقييم ======
def rating_to_score(rating):
    """تحويل التقييم الوصفي إلى نقاط"""
    rating_scores = {
        'ممتاز': 5.0,
        'جيد جداً': 4.0,
        'جيد': 3.0,
        'مقبول': 2.0,
        'ضعيف': 1.0
    }
    return rating_scores.get(rating, 0.0)

def score_to_rating(score):
    """تحويل النقاط إلى تقييم وصفي"""
    if score >= 4.5:
        return 'ممتاز'
    elif score >= 3.5:
        return 'جيد جداً'
    elif score >= 2.5:
        return 'جيد'
    elif score >= 1.5:
        return 'مقبول'
    else:
        return 'ضعيف'

def calculate_overall_score(evaluation_details, criteria_weights):
    """حساب النقاط الإجمالية بناءً على الأوزان"""
    total_score = 0.0
    total_weight = 0.0
    
    for detail in evaluation_details:
        criteria_id = detail['criteria_id']
        rating = detail['rating']
        weight = criteria_weights.get(criteria_id, 1.0)
        
        score = rating_to_score(rating)
        total_score += score * weight
        total_weight += weight
    
    if total_weight > 0:
        return total_score / total_weight
    return 0.0

def create_performance_evaluation(employee_id, period_id, evaluator_id, evaluation_data):
    """إنشاء تقييم أداء جديد"""
    conn = get_db_connection()
    
    try:
        # إنشاء التقييم الرئيسي
        cursor = conn.execute("""
            INSERT INTO performance_evaluations 
            (employee_id, period_id, evaluator_id, overall_rating, overall_score, 
             strengths, areas_for_improvement, goals_next_period, comments, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (employee_id, period_id, evaluator_id, 
              evaluation_data.get('overall_rating', ''),
              evaluation_data.get('overall_score', 0.0),
              evaluation_data.get('strengths', ''),
              evaluation_data.get('areas_for_improvement', ''),
              evaluation_data.get('goals_next_period', ''),
              evaluation_data.get('comments', ''),
              'draft'))
        
        evaluation_id = cursor.lastrowid
        
        # إضافة تفاصيل التقييم لكل معيار
        criteria_details = evaluation_data.get('criteria_details', [])
        for detail in criteria_details:
            conn.execute("""
                INSERT INTO evaluation_details 
                (evaluation_id, criteria_id, rating, score, comments)
                VALUES (?, ?, ?, ?, ?)
            """, (evaluation_id, detail['criteria_id'], detail['rating'],
                  rating_to_score(detail['rating']), detail.get('comments', '')))
        
        # تسجيل في التاريخ
        conn.execute("""
            INSERT INTO evaluation_history 
            (evaluation_id, action, changed_by, notes)
            VALUES (?, 'created', ?, 'تم إنشاء التقييم')
        """, (evaluation_id, evaluator_id))
        
        conn.commit()
        return evaluation_id
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_performance_evaluation(evaluation_id, evaluator_id, evaluation_data):
    """تحديث تقييم أداء موجود"""
    conn = get_db_connection()
    
    try:
        # تحديث التقييم الرئيسي
        conn.execute("""
            UPDATE performance_evaluations 
            SET overall_rating = ?, overall_score = ?, strengths = ?, 
                areas_for_improvement = ?, goals_next_period = ?, comments = ?
            WHERE id = ?
        """, (evaluation_data.get('overall_rating', ''),
              evaluation_data.get('overall_score', 0.0),
              evaluation_data.get('strengths', ''),
              evaluation_data.get('areas_for_improvement', ''),
              evaluation_data.get('goals_next_period', ''),
              evaluation_data.get('comments', ''),
              evaluation_id))
        
        # حذف التفاصيل القديمة وإضافة الجديدة
        conn.execute("DELETE FROM evaluation_details WHERE evaluation_id = ?", (evaluation_id,))
        
        criteria_details = evaluation_data.get('criteria_details', [])
        for detail in criteria_details:
            conn.execute("""
                INSERT INTO evaluation_details 
                (evaluation_id, criteria_id, rating, score, comments)
                VALUES (?, ?, ?, ?, ?)
            """, (evaluation_id, detail['criteria_id'], detail['rating'],
                  rating_to_score(detail['rating']), detail.get('comments', '')))
        
        # تسجيل في التاريخ
        conn.execute("""
            INSERT INTO evaluation_history 
            (evaluation_id, action, changed_by, notes)
            VALUES (?, 'updated', ?, 'تم تحديث التقييم')
        """, (evaluation_id, evaluator_id))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def complete_performance_evaluation(evaluation_id, evaluator_id):
    """إكمال التقييم وتغيير حالته"""
    conn = get_db_connection()
    
    conn.execute("""
        UPDATE performance_evaluations 
        SET status = 'completed', completed_date = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (evaluation_id,))
    
    # تسجيل في التاريخ
    conn.execute("""
        INSERT INTO evaluation_history 
        (evaluation_id, action, changed_by, notes)
        VALUES (?, 'completed', ?, 'تم إكمال التقييم')
    """, (evaluation_id, evaluator_id))
    
    conn.commit()
    conn.close()

# ====== وظائف الاستعلام ======
def get_employee_evaluations(employee_id):
    """الحصول على جميع تقييمات موظف معين"""
    conn = get_db_connection()
    evaluations = conn.execute("""
        SELECT pe.*, ep.name as period_name, ep.year, ep.quarter,
               e.name as evaluator_name
        FROM performance_evaluations pe
        JOIN evaluation_periods ep ON pe.period_id = ep.id
        JOIN employees e ON pe.evaluator_id = e.id
        WHERE pe.employee_id = ?
        ORDER BY ep.year DESC, ep.quarter DESC
    """, (employee_id,)).fetchall()
    conn.close()
    return evaluations

def get_evaluation_by_id(evaluation_id):
    """الحصول على تقييم محدد مع تفاصيله"""
    conn = get_db_connection()
    
    # الحصول على التقييم الرئيسي
    evaluation = conn.execute("""
        SELECT pe.*, ep.name as period_name, ep.year, ep.quarter,
               emp.name as employee_name, eval.name as evaluator_name
        FROM performance_evaluations pe
        JOIN evaluation_periods ep ON pe.period_id = ep.id
        JOIN employees emp ON pe.employee_id = emp.id
        JOIN employees eval ON pe.evaluator_id = eval.id
        WHERE pe.id = ?
    """, (evaluation_id,)).fetchone()
    
    if not evaluation:
        conn.close()
        return None
    
    # الحصول على تفاصيل التقييم
    details = conn.execute("""
        SELECT ed.*, ec.name as criteria_name, ec.description as criteria_description
        FROM evaluation_details ed
        JOIN evaluation_criteria ec ON ed.criteria_id = ec.id
        WHERE ed.evaluation_id = ?
        ORDER BY ec.name
    """, (evaluation_id,)).fetchall()
    
    conn.close()
    
    return {
        'evaluation': evaluation,
        'details': details
    }

def get_evaluations_by_period(period_id):
    """الحصول على جميع التقييمات لفترة معينة"""
    conn = get_db_connection()
    evaluations = conn.execute("""
        SELECT pe.*, emp.name as employee_name, eval.name as evaluator_name
        FROM performance_evaluations pe
        JOIN employees emp ON pe.employee_id = emp.id
        JOIN employees eval ON pe.evaluator_id = eval.id
        WHERE pe.period_id = ?
        ORDER BY emp.name
    """, (period_id,)).fetchall()
    conn.close()
    return evaluations

def get_pending_evaluations(period_id=None):
    """الحصول على التقييمات المعلقة (غير المكتملة)"""
    conn = get_db_connection()
    
    query = """
        SELECT pe.*, emp.name as employee_name, eval.name as evaluator_name,
               ep.name as period_name
        FROM performance_evaluations pe
        JOIN employees emp ON pe.employee_id = emp.id
        JOIN employees eval ON pe.evaluator_id = eval.id
        JOIN evaluation_periods ep ON pe.period_id = ep.id
        WHERE pe.status = 'draft'
    """
    
    params = []
    if period_id:
        query += " AND pe.period_id = ?"
        params.append(period_id)
    
    query += " ORDER BY emp.name"
    
    evaluations = conn.execute(query, params).fetchall()
    conn.close()
    return evaluations

def get_employees_without_evaluation(period_id):
    """الحصول على الموظفين الذين لم يتم تقييمهم في فترة معينة"""
    conn = get_db_connection()
    employees = conn.execute("""
        SELECT e.id, e.name, e.position
        FROM employees e
        WHERE e.id NOT IN (
            SELECT pe.employee_id 
            FROM performance_evaluations pe 
            WHERE pe.period_id = ?
        )
        ORDER BY e.name
    """, (period_id,)).fetchall()
    conn.close()
    return employees

def get_employees_with_evaluations():
    """الحصول على الموظفين الذين لديهم تقييم واحد على الأقل عبر كل الفترات"""
    conn = get_db_connection()
    employees = conn.execute("""
        SELECT 
            e.id,
            e.name,
            e.department,
            e.position,
            COUNT(DISTINCT pe.id) AS evaluations_count,
            MIN(ep.year) AS first_year,
            MAX(ep.year) AS last_year,
            MAX(ep.quarter) AS last_quarter
        FROM employees e
        JOIN performance_evaluations pe ON pe.employee_id = e.id
        JOIN evaluation_periods ep ON pe.period_id = ep.id
        GROUP BY e.id, e.name, e.department, e.position
        ORDER BY e.name
    """).fetchall()
    conn.close()
    return employees

# ====== وظائف التقارير والإحصائيات ======
def get_evaluation_statistics(period_id=None):
    """الحصول على إحصائيات التقييمات"""
    conn = get_db_connection()
    
    query = """
        SELECT 
            overall_rating,
            COUNT(*) as count,
            AVG(overall_score) as avg_score
        FROM performance_evaluations
        WHERE status = 'completed'
    """
    
    params = []
    if period_id:
        query += " AND period_id = ?"
        params.append(period_id)
    
    query += " GROUP BY overall_rating ORDER BY avg_score DESC"
    
    stats = conn.execute(query, params).fetchall()
    conn.close()
    return stats

def get_employee_performance_trend(employee_id):
    """الحصول على اتجاه أداء موظف عبر الفترات"""
    conn = get_db_connection()
    trend = conn.execute("""
        SELECT pe.overall_rating, pe.overall_score, 
               ep.year, ep.quarter, ep.name as period_name
        FROM performance_evaluations pe
        JOIN evaluation_periods ep ON pe.period_id = ep.id
        WHERE pe.employee_id = ? AND pe.status = 'completed'
        ORDER BY ep.year, ep.quarter
    """, (employee_id,)).fetchall()
    conn.close()
    return trend

def get_criteria_performance_analysis(period_id=None):
    """تحليل الأداء حسب المعايير"""
    conn = get_db_connection()
    
    query = """
        SELECT ec.name as criteria_name, ed.rating, 
               COUNT(*) as count, AVG(ed.score) as avg_score
        FROM evaluation_details ed
        JOIN evaluation_criteria ec ON ed.criteria_id = ec.id
        JOIN performance_evaluations pe ON ed.evaluation_id = pe.id
        WHERE pe.status = 'completed'
    """
    
    params = []
    if period_id:
        query += " AND pe.period_id = ?"
        params.append(period_id)
    
    query += " GROUP BY ec.name, ed.rating ORDER BY ec.name, avg_score DESC"
    
    analysis = conn.execute(query, params).fetchall()
    conn.close()
    return analysis

# مثال على كيفية استخدام الوظائف (يمكن حذف هذا الجزء في الإنتاج)
if __name__ == "__main__":
    # أمثلة على الاستخدام
    print("=== معايير التقييم ===")
    criteria = get_evaluation_criteria()
    for criterion in criteria:
        print(f"- {criterion['name']}: {criterion['description']} (وزن: {criterion['weight']})")
    
    print("\n=== الفترات التقييمية ===")
    periods = get_evaluation_periods()
    for period in periods:
        print(f"- {period['name']}: {period['start_date']} إلى {period['end_date']} (حالة: {period['status']})")
    
    print("\n=== الفترة النشطة ===")
    active_period = get_active_evaluation_period()
    if active_period:
        print(f"الفترة النشطة: {active_period['name']}")
    else:
        print("لا توجد فترة نشطة")
    
    print("\n=== إحصائيات التقييمات ===")
    stats = get_evaluation_statistics()
    for stat in stats:
        print(f"- {stat['overall_rating']}: {stat['count']} تقييم، متوسط النقاط: {stat['avg_score']:.2f}")

