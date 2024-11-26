import pytest
import os
import sqlite3
from app.controllers.student_controller import StudentController
from app.models.student import Student
from app.database.db_manager import DatabaseManager

class TestStudentController:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup для каждого теста"""
        # Создаем тестовую базу данных
        self.test_db = "test_student_manager.db"
        if os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except PermissionError:
                pass
            
        # Создаем новый экземпляр DatabaseManager для тестовой базы
        self.db_manager = DatabaseManager(self.test_db)
        # Создаем контроллер с тестовой базой
        self.controller = StudentController()
        self.controller.db = self.db_manager
        
        yield
        
        # Закрываем все соединения перед удалением
        try:
            # Создаем временное соединение для закрытия всех открытых транзакций
            temp_conn = sqlite3.connect(self.test_db)
            temp_conn.close()
            
            # Принудительно закрываем соединения контроллера
            if hasattr(self.controller, 'db'):
                del self.controller.db
            if hasattr(self, 'db_manager'):
                del self.db_manager
                
            # Теперь можно удалить файл
            if os.path.exists(self.test_db):
                os.remove(self.test_db)
        except Exception:
            pass  # Игнорируем любые ошибки при очистке

    def test_add_student(self):
        """Тест добавления студента"""
        student = Student(
            id=None,
            gender="Мужской",
            last_name="ТестовФамилия",
            first_name="ТестИмя",
            middle_name="Тестович",
            department_id=1,
            department_name=None,
            teachers=[]
        )
        
        success, message = self.controller.add_student(student)
        assert success == True, f"Failed to add student: {message}"
        
        # Проверяем, что студент добавлен
        students = self.controller.get_all_students()
        added_student = next(
            (s for s in students 
             if s.last_name == "ТестовФамилия" and s.first_name == "ТестИмя"), 
            None
        )
        assert added_student is not None, "Added student not found in database"

    def test_add_duplicate_student(self):
        """Тест добавления дубликата студента"""
        student = Student(
            id=None,
            gender="Мужской",
            last_name="ДубликатФамилия",
            first_name="ДубликатИмя",
            middle_name="Тестович",
            department_id=1,
            department_name=None,
            teachers=[]
        )
        
        # Добавляем студента первый раз
        success, message = self.controller.add_student(student)
        assert success == True, "Failed to add first student"
        
        # Пробуем добавить того же студента второй раз
        success, message = self.controller.add_student(student)
        assert success == False
        assert "уже существует" in message.lower()

    def test_get_departments(self):
        """Тест получения списка кафедр"""
        departments = self.controller.get_departments()
        assert len(departments) > 0
        assert all(isinstance(d, dict) for d in departments)
        assert all("id" in d and "name" in d for d in departments)

    def test_get_teachers(self):
        """Тест получения списка преподавателей"""
        teachers = self.controller.get_teachers()
        assert len(teachers) > 0
        assert all(isinstance(t, dict) for t in teachers)
        assert all("id" in t and "last_name" in t for t in teachers)