import pytest
import os
import sqlite3
import time
from app.database.db_manager import DatabaseManager

@pytest.fixture(scope="function")
def test_db():
    """Создание тестовой базы данных"""
    db_name = "test_student_manager.db"
    
    # Пытаемся удалить файл базы данных, если он существует
    if os.path.exists(db_name):
        for _ in range(3):  # Пробуем несколько раз
            try:
                os.remove(db_name)
                break
            except PermissionError:
                time.sleep(0.1)  # Даем время на освобождение файла
        
    # Создаем новую базу данных
    db = DatabaseManager(db_name)
    
    # Добавляем тестовые данные
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        # Проверяем существование и добавляем тестовые кафедры
        cursor.execute("SELECT COUNT(*) FROM departments")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO departments (name) VALUES ('Test Department 1')")
            cursor.execute("INSERT INTO departments (name) VALUES ('Test Department 2')")
            cursor.execute("INSERT INTO departments (name) VALUES ('Test Department 3')")
            conn.commit()
        
        # Проверяем существование и добавляем тестового преподавателя
        cursor.execute("SELECT COUNT(*) FROM teachers")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO teachers (last_name, first_name, middle_name)
                VALUES ('TestTeacher', 'Test', 'Testovich')
            ''')
            conn.commit()
    
    yield db
    
    # Закрываем все соединения
    conn.close()
    
    # Пытаемся удалить файл после тестов
    if os.path.exists(db_name):
        for _ in range(3):  # Пробуем несколько раз
            try:
                os.remove(db_name)
                break
            except PermissionError:
                time.sleep(0.1)  # Даем время на освобождение файла