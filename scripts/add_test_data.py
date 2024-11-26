import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.controllers.student_controller import StudentController
from app.models.student import Student
from app.database.db_manager import DatabaseManager

def create_test_students():
    controller = StudentController()
    
    # Список тестовых студентов
    test_students = [
        {
            "last_name": "Иванов",
            "first_name": "Петр",
            "middle_name": "Сергеевич",
            "gender": "Мужской",
            "department_id": 1,
            "email": "ivanov@test.com",
            "phone": "+79001234567"
        },
        {
            "last_name": "Петрова",
            "first_name": "Анна",
            "middle_name": "Ивановна",
            "gender": "Женский",
            "department_id": 2,
            "email": "petrova@test.com",
            "phone": "+79002345678"
        },
        {
            "last_name": "Сидоров",
            "first_name": "Алексей",
            "middle_name": "Петрович",
            "gender": "Мужской",
            "department_id": 3,
            "email": "sidorov@test.com",
            "phone": "+79003456789"
        },
        {
            "last_name": "Козлова",
            "first_name": "Мария",
            "middle_name": "Александровна",
            "gender": "Женский",
            "department_id": 1,
            "email": "kozlova@test.com",
            "phone": "+79004567890"
        },
        {
            "last_name": "Морозов",
            "first_name": "Дмитрий",
            "middle_name": "Андреевич",
            "gender": "Мужской",
            "department_id": 2,
            "email": "morozov@test.com",
            "phone": "+79005678901"
        }
    ]
    
    # Добавляем каждого студента
    for student_data in test_students:
        student = Student(
            id=None,
            **student_data
        )
        success, message = controller.add_student(student)
        if success:
            print(f"Добавлен студент: {student.full_name}")
        else:
            print(f"Ошибка при добавлении студента {student.full_name}: {message}")

if __name__ == "__main__":
    create_test_students() 