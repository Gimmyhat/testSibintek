"""
Add NOT NULL constraints and checks
Migration: 20231126_003
"""

def upgrade(cursor):
    """Применение миграции"""
    # Сначала создаем временную таблицу с нужными ограничениями
    cursor.execute('''
        CREATE TABLE students_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT NOT NULL CHECK (gender IN ('Мужской', 'Женский')),
            last_name TEXT NOT NULL CHECK (length(last_name) <= 40 AND length(last_name) > 0),
            first_name TEXT NOT NULL CHECK (length(first_name) <= 40 AND length(first_name) > 0),
            middle_name TEXT CHECK (middle_name IS NULL OR length(middle_name) <= 60),
            department_id INTEGER NOT NULL,
            photo_path TEXT,
            email TEXT,
            phone TEXT,
            FOREIGN KEY (department_id) REFERENCES departments (id),
            UNIQUE(last_name, first_name, middle_name),
            CHECK (
                (email IS NULL) OR 
                (email LIKE '%@%.%' AND length(email) >= 5)
            )
        )
    ''')
    
    # Копируем данные
    cursor.execute('''
        INSERT INTO students_new 
        SELECT * FROM students 
        WHERE gender IS NOT NULL 
        AND last_name IS NOT NULL 
        AND first_name IS NOT NULL 
        AND department_id IS NOT NULL
    ''')
    
    # Удаляем старую таблицу
    cursor.execute('DROP TABLE students')
    
    # Переименовываем новую таблицу
    cursor.execute('ALTER TABLE students_new RENAME TO students')
    
    # Создаем индексы для оптимизации
    cursor.execute('CREATE INDEX idx_students_names ON students(last_name, first_name)')
    cursor.execute('CREATE INDEX idx_students_department ON students(department_id)')

def downgrade(cursor):
    """Откат миграции"""
    cursor.execute('''
        CREATE TABLE students_old (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT,
            last_name TEXT,
            first_name TEXT,
            middle_name TEXT,
            department_id INTEGER,
            photo_path TEXT,
            email TEXT,
            phone TEXT,
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
    ''')
    
    cursor.execute('INSERT INTO students_old SELECT * FROM students')
    cursor.execute('DROP TABLE students')
    cursor.execute('ALTER TABLE students_old RENAME TO students') 