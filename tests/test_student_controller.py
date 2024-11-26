import pytest
from app.controllers.student_controller import StudentController
from app.models.student import Student

def test_add_student(test_db):
    """Тест добавления студента"""
    controller = StudentController()
    controller.db = test_db
    
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
    
    success, message = controller.add_student(student)
    assert success == True, f"Failed to add student: {message}"

def test_get_departments(test_db):
    """Тест получения списка кафедр"""
    controller = StudentController()
    controller.db = test_db
    
    departments = controller.get_departments()
    assert len(departments) > 0
    assert all(isinstance(d, dict) for d in departments)
    assert all("id" in d and "name" in d for d in departments)

def test_get_teachers(test_db):
    """Тест получения списка преподавателей"""
    controller = StudentController()
    controller.db = test_db
    
    teachers = controller.get_teachers()
    assert len(teachers) > 0
    assert all(isinstance(t, dict) for t in teachers)
    assert all("id" in t and "last_name" in t for t in teachers)