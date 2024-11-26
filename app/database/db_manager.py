import sqlite3
from typing import List, Tuple

class DatabaseManager:
    def __init__(self, db_name: str = "student_manager.db"):
        self.db_name = db_name
        self.init_database()
        self.populate_initial_data()

    def init_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
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
            
            # Создание таблицы студентов с новыми полями
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
            
            # Создание связующей таблицы между студентами и преподавателями
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS student_teachers (
                    student_id INTEGER,
                    teacher_id INTEGER,
                    FOREIGN KEY (student_id) REFERENCES students (id),
                    FOREIGN KEY (teacher_id) REFERENCES teachers (id),
                    PRIMARY KEY (student_id, teacher_id)
                )
            ''')
            
            # Создание таблицы истории изменений
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
            
            # Добавляем новые колонки в существующую таблицу students
            try:
                cursor.execute('ALTER TABLE students ADD COLUMN photo_path TEXT')
                cursor.execute('ALTER TABLE students ADD COLUMN email TEXT')
                cursor.execute('ALTER TABLE students ADD COLUMN phone TEXT')
                cursor.execute('ALTER TABLE students ADD COLUMN modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            except sqlite3.OperationalError:
                # Колонки уже существуют
                pass

    def populate_initial_data(self):
        departments = [
            "Кафедра информационных технологий",
            "Кафедра математики",
            "Кафедра физики",
            "Кафедра экономики",
            "Кафедра иностранных языков"
        ]
        
        teachers = [
            ("Иванов", "Иван", "Иванович"),
            ("Петров", "Петр", "Петрович"),
            ("Сидорова", "Мария", "Александровна"),
            ("Козлов", "Андрей", "Викторович"),
            ("Морозова", "Елена", "Сергеевна"),
            ("Волков", "Дмитрий", "Николаевич")
        ]
        
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Проверяем, есть ли уже данные в таблицах
                cursor.execute("SELECT COUNT(*) FROM departments")
                if cursor.fetchone()[0] == 0:
                    # Добавляем кафедры
                    for dept in departments:
                        cursor.execute(
                            "INSERT INTO departments (name) VALUES (?)",
                            (dept,)
                        )
                
                cursor.execute("SELECT COUNT(*) FROM teachers")
                if cursor.fetchone()[0] == 0:
                    # Добавляем преподавателей
                    for last_name, first_name, middle_name in teachers:
                        cursor.execute('''
                            INSERT INTO teachers 
                            (last_name, first_name, middle_name)
                            VALUES (?, ?, ?)
                        ''', (last_name, first_name, middle_name))
                
                conn.commit()
        except Exception as e:
            print(f"Ошибка при добавлении начальных данных: {str(e)}")