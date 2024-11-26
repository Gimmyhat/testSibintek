from typing import List, Optional
from ..models.student import Student
from ..database.db_manager import DatabaseManager
import sqlite3
from ..utils.logger import Logger

class StudentController:
    def __init__(self):
        self.db = DatabaseManager()
        self.logger = Logger()
    
    def add_student(self, student: Student) -> tuple[bool, str]:
        is_valid, error = student.validate()
        if not is_valid:
            self.logger.error(f"Ошибка валидации при добавлении студента: {error}")
            return False, error
            
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO students 
                    (gender, last_name, first_name, middle_name, department_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (student.gender, student.last_name, student.first_name, 
                      student.middle_name, student.department_id))
                
                student_id = cursor.lastrowid
                
                if student.teachers:
                    for teacher_id in student.teachers:
                        cursor.execute('''
                            INSERT INTO student_teachers (student_id, teacher_id)
                            VALUES (?, ?)
                        ''', (student_id, teacher_id))
                        
                self.logger.info(f"Добавлен новый студент: {student.full_name}")
                return True, "Студент успешно добавлен"
        except sqlite3.IntegrityError:
            self.logger.error(f"Попытка добавить дубликат студента: {student.full_name}")
            return False, "Студент с такими ФИО уже существует"
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении студента {student.full_name}: {str(e)}")
            return False, f"Ошибка при добавлении студента: {str(e)}"
    
    def get_all_students(self) -> List[Student]:
        with sqlite3.connect(self.db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, d.name as department_name, GROUP_CONCAT(st.teacher_id)
                FROM students s
                LEFT JOIN departments d ON s.department_id = d.id
                LEFT JOIN student_teachers st ON s.id = st.student_id
                GROUP BY s.id
            ''')
            
            students = []
            for row in cursor.fetchall():
                teachers = [int(t) for t in row[7].split(',')] if row[7] else []
                students.append(Student(
                    id=row[0],
                    gender=row[1],
                    last_name=row[2],
                    first_name=row[3],
                    middle_name=row[4],
                    department_id=row[5],
                    department_name=row[6],
                    teachers=teachers
                ))
            return students 
    
    def delete_student(self, student_id: int) -> tuple[bool, str]:
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                cursor = conn.cursor()
                # Получаем данные студента перед удалением
                cursor.execute('SELECT last_name, first_name FROM students WHERE id = ?', 
                             (student_id,))
                student_data = cursor.fetchone()
                
                # Удаляем связи с преподавателями
                cursor.execute('DELETE FROM student_teachers WHERE student_id = ?', 
                             (student_id,))
                # Удаляем самого студента
                cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
                
                if student_data:
                    self.logger.info(f"Удален студент: {student_data[0]} {student_data[1]}")
                return True, "Студент успешно удален"
        except Exception as e:
            self.logger.error(f"Ошибка при удалении студента {student_id}: {str(e)}")
            return False, f"Ошибка при удалении студента: {str(e)}"
    
    def update_student(self, student: Student) -> tuple[bool, str]:
        is_valid, error = student.validate()
        if not is_valid:
            return False, error
        
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE students 
                    SET gender = ?, last_name = ?, first_name = ?, 
                        middle_name = ?, department_id = ?
                    WHERE id = ?
                ''', (student.gender, student.last_name, student.first_name,
                      student.middle_name, student.department_id, student.id))
                
                # Обновляем связи с преподавателями
                cursor.execute('DELETE FROM student_teachers WHERE student_id = ?', 
                             (student.id,))
                if student.teachers:
                    for teacher_id in student.teachers:
                        cursor.execute('''
                            INSERT INTO student_teachers (student_id, teacher_id)
                            VALUES (?, ?)
                        ''', (student.id, teacher_id))
                
                return True, "Данные студента успешно обновлены"
        except sqlite3.IntegrityError:
            return False, "Студент с такими ФИО уже существует"
        except Exception as e:
            return False, f"Ошибка при обновлении данных студента: {str(e)}"
    
    def get_departments(self) -> List[dict]:
        with sqlite3.connect(self.db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM departments')
            return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    
    def get_teachers(self) -> List[dict]:
        with sqlite3.connect(self.db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, last_name, first_name, middle_name 
                FROM teachers
            ''')
            return [{"id": row[0], "last_name": row[1], 
                    "first_name": row[2], "middle_name": row[3]} 
                    for row in cursor.fetchall()]
    
    def get_teacher_names(self, teacher_ids: List[int]) -> List[str]:
        with sqlite3.connect(self.db.db_name) as conn:
            cursor = conn.cursor()
            placeholders = ','.join('?' * len(teacher_ids))
            cursor.execute(f'''
                SELECT last_name, first_name
                FROM teachers
                WHERE id IN ({placeholders})
            ''', teacher_ids)
            
            return [f"{row[0]} {row[1]}" for row in cursor.fetchall()]