"""
Initial database structure
Migration: 20231126_001
"""

def upgrade(cursor):
    """Применение миграции"""
    # Создание таблицы кафедр
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Создание таблицы преподавателей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            middle_name TEXT
        )
    ''')
    
    # Создание таблицы студентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT NOT NULL,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            department_id INTEGER,
            photo_path TEXT,
            email TEXT,
            phone TEXT,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments (id),
            UNIQUE(last_name, first_name, middle_name)
        )
    ''')
    
    # Создание связующей таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_teachers (
            student_id INTEGER,
            teacher_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (teacher_id) REFERENCES teachers (id),
            PRIMARY KEY (student_id, teacher_id)
        )
    ''')
    
    # Создание таблицы истории
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            field_name TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')

def downgrade(cursor):
    """Откат миграции"""
    cursor.execute('DROP TABLE IF EXISTS student_history')
    cursor.execute('DROP TABLE IF EXISTS student_teachers')
    cursor.execute('DROP TABLE IF EXISTS students')
    cursor.execute('DROP TABLE IF EXISTS teachers')
    cursor.execute('DROP TABLE IF EXISTS departments') 