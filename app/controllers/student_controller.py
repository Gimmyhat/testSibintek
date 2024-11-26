from typing import List, Optional
from ..models.student import Student
from ..database.db_manager import DatabaseManager
import sqlite3
from ..utils.logger import Logger
import os
from datetime import datetime

class StudentController:
    def __init__(self):
        self.db = DatabaseManager()
        self.logger = Logger()
    
    def _execute_query(self, query: str, params: tuple = None) -> tuple[bool, str, any]:
        """Выполнение SQL запроса с обработкой ошибок"""
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchall() if 'SELECT' in query.upper() else None
                return True, "", result
        except sqlite3.IntegrityError as e:
            error_msg = str(e)
            self.logger.error(f"Ошибка целостности данных: {error_msg}")
            return False, "Нарушение уникальности данных", None
        except sqlite3.OperationalError as e:
            error_msg = str(e)
            if "RAISE(ABORT" in error_msg:
                # Извлекаем сообщение об ошибке из триггера
                error_msg = error_msg.split('RAISE(ABORT,')[-1].strip("')")
            self.logger.error(f"Ошибка валидации: {error_msg}")
            return False, error_msg, None
        except Exception as e:
            self.logger.error(f"Ошибка базы данных: {str(e)}")
            return False, f"Ошибка базы данных: {str(e)}", None
    
    def add_student(self, student: Student) -> tuple[bool, str]:
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                cursor = conn.cursor()
                
                # Добавляем студента
                cursor.execute('''
                    INSERT INTO students 
                    (gender, last_name, first_name, middle_name, department_id, 
                     photo_path, email, phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (student.gender, student.last_name, student.first_name, 
                      student.middle_name, student.department_id, student.photo_path,
                      student.email, student.phone))
                
                student_id = cursor.lastrowid
                
                # Добавляем связи с преподавателями
                if student.teachers:
                    for teacher_id in student.teachers:
                        cursor.execute('''
                            INSERT INTO student_teachers (student_id, teacher_id)
                            VALUES (?, ?)
                        ''', (student_id, teacher_id))
                
                self.logger.info(f"Добавлен новый студент: {student.full_name}")
                return True, "Студент успешно добавлен"
                
        except sqlite3.IntegrityError as e:
            self.logger.error(f"Ошибка целостности данных: {str(e)}")
            return False, "Нарушение уникальности данных"
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении студента: {str(e)}")
            return False, f"Ошибка при добавлении студента: {str(e)}"
    
    def get_all_students(self) -> List[Student]:
        with sqlite3.connect(self.db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    s.id,
                    s.gender,
                    s.last_name,
                    s.first_name,
                    s.middle_name,
                    s.department_id,
                    s.photo_path,
                    d.name as department_name,
                    GROUP_CONCAT(st.teacher_id) as teacher_ids
                FROM students s
                LEFT JOIN departments d ON s.department_id = d.id
                LEFT JOIN student_teachers st ON s.id = st.student_id
                GROUP BY s.id
            ''')
            
            students = []
            for row in cursor.fetchall():
                teachers = [int(t) for t in row[8].split(',')] if row[8] else []
                students.append(Student(
                    id=row[0],
                    gender=row[1],
                    last_name=row[2],
                    first_name=row[3],
                    middle_name=row[4],
                    department_id=row[5],
                    photo_path=row[6],
                    department_name=row[7],
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
        try:
            success, error, _ = self._execute_query('''
                UPDATE students 
                SET gender = ?, 
                    last_name = ?, 
                    first_name = ?, 
                    middle_name = ?, 
                    department_id = ?, 
                    photo_path = ?,
                    email = ?,
                    phone = ?
                WHERE id = ?
            ''', (student.gender, student.last_name, student.first_name,
                  student.middle_name, student.department_id, student.photo_path,
                  student.email, student.phone, student.id))
            
            if not success:
                return False, error
            
            # Обновляем связи с преподавателями
            self._execute_query(
                'DELETE FROM student_teachers WHERE student_id = ?', 
                (student.id,)
            )
            
            if student.teachers:
                for teacher_id in student.teachers:
                    self._execute_query('''
                        INSERT INTO student_teachers (student_id, teacher_id)
                        VALUES (?, ?)
                    ''', (student.id, teacher_id))
            
            self.logger.info(f"Обновлены данные студента: {student.full_name}")
            return True, "Данные студента успешно обновлены"
            
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении данных студента: {str(e)}")
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
    
    def get_statistics(self) -> dict:
        """Получение статистики по студентам"""
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                cursor = conn.cursor()
                
                # Статистика по кафедрам
                cursor.execute('''
                    SELECT d.name, COUNT(s.id)
                    FROM departments d
                    LEFT JOIN students s ON d.id = s.department_id
                    GROUP BY d.name
                ''')
                departments_stats = dict(cursor.fetchall())
                
                # Статистика по полу
                cursor.execute('''
                    SELECT gender, COUNT(id)
                    FROM students
                    GROUP BY gender
                ''')
                gender_stats = dict(cursor.fetchall())
                
                return {
                    'departments': departments_stats,
                    'gender': gender_stats
                }
        except Exception as e:
            self.logger.error(f"Ошибка при получении статистики: {str(e)}")
            return {'departments': {}, 'gender': {}}
    
    def log_change(self, student_id: int, field_name: str, old_value: str, new_value: str):
        """Логирование изменений в данных студента"""
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO student_history 
                    (student_id, field_name, old_value, new_value)
                    VALUES (?, ?, ?, ?)
                ''', (student_id, field_name, old_value, new_value))
                self.logger.info(f"Изменение данных студента {student_id}: {field_name}")
        except Exception as e:
            self.logger.error(f"Ошибка при логировании изменений: {str(e)}")
    
    def get_student_history(self, student_id: int) -> List[dict]:
        """Получение и��тории изменений студента"""
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT field_name, old_value, new_value, changed_at
                    FROM student_history
                    WHERE student_id = ?
                    ORDER BY changed_at DESC
                ''', (student_id,))
                
                history = []
                for row in cursor.fetchall():
                    history.append({
                        'field': row[0],
                        'old_value': row[1],
                        'new_value': row[2],
                        'date': row[3]
                    })
                return history
        except Exception as e:
            self.logger.error(f"Ошибка при получении истории: {str(e)}")
            return []
    
    def backup_database(self):
        """Создание резервной копии базы данных"""
        try:
            backup_dir = 'backups'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f'backup_{timestamp}.db')
            
            with sqlite3.connect(self.db.db_name) as conn:
                backup = sqlite3.connect(backup_path)
                conn.backup(backup)
                backup.close()
            
            self.logger.info(f"Создана резервная копия базы данных: {backup_path}")
            return True, "Резервная копия создана успешно"
        except Exception as e:
            self.logger.error(f"Ошибка при создании резервной копии: {str(e)}")
            return False, str(e)