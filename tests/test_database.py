import pytest
import sqlite3
import os
from app.database.db_manager import DatabaseManager

class TestDatabase:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup для каждого теста"""
        self.test_db = "test_student_manager.db"
        # Удаляем базу если она существует
        if os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except PermissionError:
                pass  # Игнорируем ошибку, если файл занят
                
        self.db_manager = DatabaseManager(self.test_db)
        yield
        # Удаляем тестовую базу после каждого теста
        try:
            if os.path.exists(self.test_db):
                os.remove(self.test_db)
        except PermissionError:
            pass  # Игнорируем ошибку, если файл занят

    def test_database_initialization(self):
        """Тест создания таблиц в базе данных"""
        conn = sqlite3.connect(self.test_db)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            
            assert "departments" in tables
            assert "teachers" in tables
            assert "students" in tables
            assert "student_teachers" in tables
        finally:
            conn.close()

    def test_initial_data_population(self):
        """Тест заполнения начальных данных"""
        conn = sqlite3.connect(self.test_db)
        try:
            cursor = conn.cursor()
            
            # Проверяем наличие кафедр
            cursor.execute("SELECT COUNT(*) FROM departments")
            dept_count = cursor.fetchone()[0]
            assert dept_count == 5, f"Expected 5 departments, got {dept_count}"
            
            # Проверяем наличие преподавателей
            cursor.execute("SELECT COUNT(*) FROM teachers")
            teacher_count = cursor.fetchone()[0]
            assert teacher_count == 6, f"Expected 6 teachers, got {teacher_count}"
        finally:
            conn.close()

    def test_department_data(self):
        """Тест данных кафедр"""
        conn = sqlite3.connect(self.test_db)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM departments")
            departments = {row[0] for row in cursor.fetchall()}
            
            expected_departments = {
                "Кафедра информационных технологий",
                "Кафедра математики",
                "Кафедра физики",
                "Кафедра экономики",
                "Кафедра иностранных языков"
            }
            assert departments == expected_departments
        finally:
            conn.close()

    def test_teacher_data(self):
        """Тест данных преподавателей"""
        conn = sqlite3.connect(self.test_db)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT last_name, first_name FROM teachers")
            teachers = {f"{row[0]} {row[1]}" for row in cursor.fetchall()}
            
            assert "Иванов Иван" in teachers
            assert "Петров Петр" in teachers
            assert len(teachers) == 6
        finally:
            conn.close()