from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLineEdit, QComboBox, QPushButton, QMessageBox, 
                            QListWidget, QListWidgetItem, QLabel)
from PyQt5.QtCore import Qt
from ..models.student import Student
from .history_dialog import HistoryDialog
from .photo_dialog import PhotoDialog

class StudentDialog(QDialog):
    def __init__(self, parent=None, student_id=None):
        super().__init__(parent)
        self.student_controller = parent.student_controller
        self.student_id = student_id
        self.student = None
        self.init_ui()
        
        if student_id:
            self.load_student_data()

    def init_ui(self):
        self.setWindowTitle('Добавление студента' if not self.student_id else 'Редактирование студента')
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        # Создаем поля ввода с валидацией
        self.last_name_edit = QLineEdit()
        self.last_name_edit.setMaxLength(40)
        self.last_name_edit.setPlaceholderText("Обязательное поле")
        
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setMaxLength(40)
        self.first_name_edit.setPlaceholderText("Обязательное поле")
        
        self.middle_name_edit = QLineEdit()
        self.middle_name_edit.setMaxLength(60)
        self.middle_name_edit.setPlaceholderText("Необязательное поле")
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(['', 'Мужской', 'Женский'])
        
        self.department_combo = QComboBox()
        self.department_combo.addItem('', None)  # Пустой элемент
        self.load_departments()
        
        self.teachers_list = QListWidget()
        self.teachers_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_teachers()
        
        # Добавляем поля в форму
        form_layout.addRow('* Фамилия:', self.last_name_edit)
        form_layout.addRow('* Имя:', self.first_name_edit)
        form_layout.addRow('Отчество:', self.middle_name_edit)
        form_layout.addRow('* Пол:', self.gender_combo)
        form_layout.addRow('* Кафедра:', self.department_combo)
        form_layout.addRow('Преподаватели:', self.teachers_list)
        
        # Добавляем подсказку об обязательных полях
        hint_label = QLabel('* - обязательные поля')
        hint_label.setStyleSheet('color: red')
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        save_button = QPushButton('Сохранить')
        cancel_button = QPushButton('Отмена')
        history_button = QPushButton('История изменений')
        photo_button = QPushButton('Фотография')
        
        save_button.clicked.connect(self.validate_and_save)
        cancel_button.clicked.connect(self.reject)
        history_button.clicked.connect(self.show_history)
        photo_button.clicked.connect(self.show_photo)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(history_button)
        buttons_layout.addWidget(photo_button)
        
        layout.addLayout(form_layout)
        layout.addWidget(hint_label)
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

    def validate_and_save(self):
        """Валидация и сохранение данных"""
        # Проверяем обязательные поля
        if not self.last_name_edit.text().strip():
            QMessageBox.warning(self, 'Ошибка', 'Поле "Фамилия" обязательно для заполнения')
            self.last_name_edit.setFocus()
            return
            
        if not self.first_name_edit.text().strip():
            QMessageBox.warning(self, 'Ошибка', 'Поле "Имя" обязательно для заполнения')
            self.first_name_edit.setFocus()
            return
            
        if not self.gender_combo.currentText():
            QMessageBox.warning(self, 'Ошибка', 'Необходимо выбрать пол')
            self.gender_combo.setFocus()
            return
            
        if not self.department_combo.currentData():
            QMessageBox.warning(self, 'Ошибка', 'Необходимо выбрать кафедру')
            self.department_combo.setFocus()
            return

        # Создаем объект студента
        student = Student(
            id=self.student_id,
            gender=self.gender_combo.currentText(),
            last_name=self.last_name_edit.text().strip(),
            first_name=self.first_name_edit.text().strip(),
            middle_name=self.middle_name_edit.text().strip() or None,
            department_id=self.department_combo.currentData(),
            department_name=self.department_combo.currentText(),
            photo_path=self.student.photo_path if hasattr(self, 'student') and self.student else None,
            teachers=[item.data(Qt.UserRole) for item in 
                     self.teachers_list.selectedItems()]
        )
        
        # Валидация через модель
        is_valid, error = student.validate()
        if not is_valid:
            QMessageBox.warning(self, 'Ошибка', error)
            return
        
        # Сохранение
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
        self.student = next((s for s in students if s.id == self.student_id), None)
        
        if self.student:
            self.last_name_edit.setText(self.student.last_name)
            self.first_name_edit.setText(self.student.first_name)
            self.middle_name_edit.setText(self.student.middle_name or '')
            
            # Устанавливаем пол
            index = self.gender_combo.findText(self.student.gender)
            if index >= 0:
                self.gender_combo.setCurrentIndex(index)
            
            # Устанавливаем кафедру
            index = self.department_combo.findData(self.student.department_id)
            if index >= 0:
                self.department_combo.setCurrentIndex(index)
            
            # Выбираем преподавателей
            if self.student.teachers:
                for i in range(self.teachers_list.count()):
                    item = self.teachers_list.item(i)
                    if item.data(Qt.UserRole) in self.student.teachers:
                        item.setSelected(True)

    def show_history(self):
        if self.student_id:
            dialog = HistoryDialog(self.student_controller, self.student_id, self)
            dialog.exec_()

    def show_photo(self):
        """Показать диалог работы с фото"""
        if not self.student:
            self.student = Student(
                id=self.student_id,
                gender=self.gender_combo.currentText(),
                last_name=self.last_name_edit.text(),
                first_name=self.first_name_edit.text(),
                middle_name=self.middle_name_edit.text(),
                department_id=self.department_combo.currentData(),
                photo_path=None
            )
        
        dialog = PhotoDialog(
            self.student_id, 
            self.student.photo_path if self.student else None,
            self
        )
        if dialog.exec_() and dialog.new_photo_path:
            self.student.photo_path = dialog.new_photo_path