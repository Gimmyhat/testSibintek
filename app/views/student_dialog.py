from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLineEdit, QComboBox, QPushButton, QMessageBox, 
                            QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt
from ..models.student import Student

class StudentDialog(QDialog):
    def __init__(self, parent=None, student_id=None):
        super().__init__(parent)
        self.student_controller = parent.student_controller
        self.student_id = student_id
        self.init_ui()
        
        if student_id:
            self.load_student_data()

    def init_ui(self):
        self.setWindowTitle('Добавление студента' if not self.student_id else 'Редактирование студента')
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        # Создаем поля ввода
        self.last_name_edit = QLineEdit()
        self.first_name_edit = QLineEdit()
        self.middle_name_edit = QLineEdit()
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(['Мужской', 'Жеский'])
        
        self.department_combo = QComboBox()
        self.load_departments()
        
        self.teachers_list = QListWidget()
        self.teachers_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_teachers()
        
        # Добавляем поля в форму
        form_layout.addRow('Фамилия:', self.last_name_edit)
        form_layout.addRow('Имя:', self.first_name_edit)
        form_layout.addRow('Отчество:', self.middle_name_edit)
        form_layout.addRow('Пол:', self.gender_combo)
        form_layout.addRow('Кафедра:', self.department_combo)
        form_layout.addRow('Преподаватели:', self.teachers_list)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        save_button = QPushButton('Сохранить')
        cancel_button = QPushButton('Отмена')
        
        save_button.clicked.connect(self.save_student)
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)

    def load_departments(self):
        departments = self.student_controller.get_departments()
        self.department_combo.clear()
        for dept in departments:
            self.department_combo.addItem(dept['name'], dept['id'])

    def load_teachers(self):
        teachers = self.student_controller.get_teachers()
        self.teachers_list.clear()
        for teacher in teachers:
            item = QListWidgetItem(
                f"{teacher['last_name']} {teacher['first_name']} {teacher['middle_name']}"
            )
            item.setData(Qt.UserRole, teacher['id'])
            self.teachers_list.addItem(item)

    def save_student(self):
        student = Student(
            id=self.student_id,
            last_name=self.last_name_edit.text(),
            first_name=self.first_name_edit.text(),
            middle_name=self.middle_name_edit.text() or None,
            gender=self.gender_combo.currentText(),
            department_id=self.department_combo.currentData(),
            teachers=[item.data(Qt.UserRole) for item in 
                     self.teachers_list.selectedItems()]
        )
        
        if self.student_id:
            success, message = self.student_controller.update_student(student)
        else:
            success, message = self.student_controller.add_student(student)
            
        if success:
            self.accept()
        else:
            QMessageBox.warning(self, 'Ошибка', message) 

    def load_student_data(self):
        """Загрузка данных студента для редактирования"""
        students = self.student_controller.get_all_students()
        student = next((s for s in students if s.id == self.student_id), None)
        
        if student:
            self.last_name_edit.setText(student.last_name)
            self.first_name_edit.setText(student.first_name)
            self.middle_name_edit.setText(student.middle_name or '')
            
            # Устанавливаем пол
            index = self.gender_combo.findText(student.gender)
            if index >= 0:
                self.gender_combo.setCurrentIndex(index)
            
            # Устанавливаем кафедру
            index = self.department_combo.findData(student.department_id)
            if index >= 0:
                self.department_combo.setCurrentIndex(index)
            
            # Выбираем преподавателей
            if student.teachers:
                for i in range(self.teachers_list.count()):
                    item = self.teachers_list.item(i)
                    if item.data(Qt.UserRole) in student.teachers:
                        item.setSelected(True) 