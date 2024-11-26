"""
Add validation triggers
Migration: 20231126_002
"""

def upgrade(cursor):
    """Применение миграции"""
    
    # Триггер для проверки длины имени и фамилии
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS check_name_length
        BEFORE INSERT ON students
        BEGIN
            SELECT
                CASE
                    WHEN length(NEW.last_name) > 40
                        THEN RAISE(ABORT, 'Фамилия не может быть длиннее 40 символов')
                    WHEN length(NEW.first_name) > 40
                        THEN RAISE(ABORT, 'Имя не может быть длиннее 40 символов')
                    WHEN NEW.middle_name IS NOT NULL AND length(NEW.middle_name) > 60
                        THEN RAISE(ABORT, 'Отчество не может быть длиннее 60 символов')
                END;
        END;
    ''')
    
    # Триггер для проверки email
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS check_email_format
        BEFORE INSERT ON students
        WHEN NEW.email IS NOT NULL
        BEGIN
            SELECT
                CASE
                    WHEN NEW.email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
                        THEN RAISE(ABORT, 'Некорректный формат email')
                END;
        END;
    ''')
    
    # Триггер для проверки телефона
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS check_phone_format
        BEFORE INSERT ON students
        WHEN NEW.phone IS NOT NULL
        BEGIN
            SELECT
                CASE
                    WHEN NEW.phone NOT REGEXP '^\+?[1-9][0-9]{10,11}$'
                        THEN RAISE(ABORT, 'Некорректный формат телефона')
                END;
        END;
    ''')
    
    # Триггер для проверки обязательных полей
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS check_required_fields
        BEFORE INSERT ON students
        BEGIN
            SELECT
                CASE
                    WHEN NEW.gender IS NULL OR NEW.gender = ''
                        THEN RAISE(ABORT, 'Поле "Пол" обязательно для заполнения')
                    WHEN NEW.last_name IS NULL OR NEW.last_name = ''
                        THEN RAISE(ABORT, 'Поле "Фамилия" обязательно для заполнения')
                    WHEN NEW.first_name IS NULL OR NEW.first_name = ''
                        THEN RAISE(ABORT, 'Поле "Имя" обязательно для заполнения')
                    WHEN NEW.department_id IS NULL
                        THEN RAISE(ABORT, 'Необходимо выбрать кафедру')
                END;
        END;
    ''')
    
    # Триггер для проверки существования кафедры
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS check_department_exists
        BEFORE INSERT ON students
        BEGIN
            SELECT
                CASE
                    WHEN NEW.department_id NOT IN (SELECT id FROM departments)
                        THEN RAISE(ABORT, 'Указанная кафедра не существует')
                END;
        END;
    ''')
    
    # Триггеры для UPDATE операций
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS check_name_length_update
        BEFORE UPDATE ON students
        BEGIN
            SELECT
                CASE
                    WHEN length(NEW.last_name) > 40
                        THEN RAISE(ABORT, 'Фамилия не может быть длиннее 40 символов')
                    WHEN length(NEW.first_name) > 40
                        THEN RAISE(ABORT, 'Имя не может быть длиннее 40 символов')
                    WHEN NEW.middle_name IS NOT NULL AND length(NEW.middle_name) > 60
                        THEN RAISE(ABORT, 'Отчество не может быть длиннее 60 символов')
                END;
        END;
    ''')
    
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS check_email_format_update
        BEFORE UPDATE ON students
        WHEN NEW.email IS NOT NULL
        BEGIN
            SELECT
                CASE
                    WHEN NEW.email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
                        THEN RAISE(ABORT, 'Некорректный формат email')
                END;
        END;
    ''')

def downgrade(cursor):
    """Откат миграции"""
    cursor.execute('DROP TRIGGER IF EXISTS check_name_length')
    cursor.execute('DROP TRIGGER IF EXISTS check_email_format')
    cursor.execute('DROP TRIGGER IF EXISTS check_phone_format')
    cursor.execute('DROP TRIGGER IF EXISTS check_required_fields')
    cursor.execute('DROP TRIGGER IF EXISTS check_department_exists')
    cursor.execute('DROP TRIGGER IF EXISTS check_name_length_update')
    cursor.execute('DROP TRIGGER IF EXISTS check_email_format_update') 