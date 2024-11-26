import pytest
from app.models.student import Student

@pytest.fixture
def valid_student():
    """Фикстура для создания валидного студента"""
    return Student(
        id=None,
        gender="Мужской",
        last_name="Иванов",
        first_name="Иван",
        middle_name="Иванович",
        department_id=1
    )

def test_student_validation_valid(valid_student):
    """Тест валидации корректных данных студента"""
    is_valid, _ = valid_student.validate()
    assert is_valid == True

def test_student_validation_long_last_name(valid_student):
    """Тест валидации слишком длинной фамилии"""
    valid_student.last_name = "И" * 41
    is_valid, error = valid_student.validate()
    assert is_valid == False
    assert error == "Фамилия не может быть длиннее 40 символов"

def test_student_validation_no_department(valid_student):
    """Тест валидации отсутствия кафедры"""
    valid_student.department_id = None
    is_valid, error = valid_student.validate()
    assert is_valid == False
    assert error == "Необходимо выбрать кафедру"

def test_student_full_name(valid_student):
    """Тест формирования полного имени"""
    assert valid_student.full_name == "Иванов Иван Иванович"

def test_student_full_name_without_middle_name(valid_student):
    """Тест формирования имени без отчества"""
    valid_student.middle_name = None
    assert valid_student.full_name == "Иванов Иван "
 