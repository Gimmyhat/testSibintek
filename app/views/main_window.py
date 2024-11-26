from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTableWidget, QPushButton, QTableWidgetItem, QHeaderView,
                            QMessageBox)
from PyQt5.QtCore import Qt
from ..controllers.student_controller import StudentController
from .student_dialog import StudentDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.student_controller = StudentController()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Менеджер студентов')
        self.setGeometry(100, 100, 800, 600)

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Создаем главный layout
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем панель с кнопками
        button_layout = QHBoxLayout()
        
        # Кнопки управления
        add_button = QPushButton('Добавить студента')
        edit_button = QPushButton('Редактировать')
        delete_button = QPushButton('Удалить')
        
        add_button.clicked.connect(self.add_student)
        edit_button.clicked.connect(self.edit_student)
        delete_button.clicked.connect(self.delete_student)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch()
        
        # Создаем таблицу студентов
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'ID', 'ФИО', 'Пол', 'Кафедра', 'Преподаватели'
        ])
        
        # Делаем таблицу только для чтения
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Настраиваем растягивание колонок
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # ФИО
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Кафедра
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # Преподаватели
        
        # Разрешаем выделение только целых строк
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Добавляем обработчик двойного клика
        self.table.doubleClicked.connect(self.on_table_double_click)
        
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        self.load_students()

    def load_students(self):
        """Загрузка списка студентов"""
        students = self.student_controller.get_all_students()
        self.table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            # ID
            item = QTableWidgetItem(str(student.id))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, item)
            
            # ФИО
            full_name = f"{student.last_name} {student.first_name}"
            if student.middle_name:
                full_name += f" {student.middle_name}"
            item = QTableWidgetItem(full_name)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, item)
            
            # Пол
            item = QTableWidgetItem(student.gender)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 2, item)
            
            # Кафедра
            item = QTableWidgetItem(student.department_name or '')
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 3, item)
            
            # Преподаватели
            if student.teachers:
                teachers = self.student_controller.get_teacher_names(student.teachers)
                item = QTableWidgetItem(', '.join(teachers))
            else:
                item = QTableWidgetItem('')
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 4, item)

    def add_student(self):
        """Добавление нового студента"""
        dialog = StudentDialog(self)
        if dialog.exec_():
            self.load_students()

    def edit_student(self):
        """Редактирование выбранного студента"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Предупреждение', 
                              'Пожалуйста, выберите студента для редактирования')
            return
            
        student_id = int(self.table.item(current_row, 0).text())
        dialog = StudentDialog(self, student_id)
        if dialog.exec_():
            self.load_students()

    def delete_student(self):
        """Удаление выбранного студента"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Предупреждение', 
                              'Пожалуйста, выберите студента для удаления')
            return
            
        student_id = int(self.table.item(current_row, 0).text())
        reply = QMessageBox.question(self, 'Подтверждение', 
                                   'Вы уверены, что хотите удалить этого студента?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            success, message = self.student_controller.delete_student(student_id)
            if success:
                self.load_students()
            else:
                QMessageBox.critical(self, 'Ошибка', 
                                   f'Не удалось удалить студента: {message}') 

    def on_table_double_click(self, index):
        """Обработка двойного клика по таблице"""
        student_id = int(self.table.item(index.row(), 0).text())
        dialog = StudentDialog(self, student_id)
        if dialog.exec_():
            self.load_students()