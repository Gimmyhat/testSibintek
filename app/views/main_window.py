from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTableWidget, QPushButton, QTableWidgetItem, QHeaderView,
                            QMessageBox, QLineEdit, QLabel, QComboBox, QDialog, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QScreen
from ..controllers.student_controller import StudentController
from .student_dialog import StudentDialog
from ..utils.logger import Logger
from .backup_dialog import BackupDialog
from .restore_dialog import RestoreDialog

class StatisticsDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Статистика')
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        # Получаем статистику
        stats = self.controller.get_statistics()

        # Статистика по кафедрам
        layout.addWidget(QLabel('<b>Студенты по кафедрам:</b>'))
        for dept, count in stats['departments'].items():
            layout.addWidget(QLabel(f'{dept}: {count} студентов'))

        # Статистика по полу
        layout.addWidget(QLabel('<b>Распределение по полу:</b>'))
        for gender, count in stats['gender'].items():
            layout.addWidget(QLabel(f'{gender}: {count} студентов'))

        # Кнопка закрытия
        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

class MainWindow(QMainWindow):
    restart_signal = pyqtSignal()  # Сигнал для перезапуска

    def __init__(self):
        super().__init__()
        self.student_controller = StudentController()
        self.logger = Logger()
        self.init_ui()
        self.center_on_screen()  # Добавляем центрирование
        self.logger.info("Приложение запущено")

    def center_on_screen(self):
        """Центрирование окна на экране"""
        # Получаем геометрию экрана
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        
        # Получаем размеры окна
        window_size = self.geometry()
        
        # Вычисляем центральную позицию
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        
        # Перемещаем окно
        self.move(x, y)

    def init_ui(self):
        self.setWindowTitle('Менеджер студентов')
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Панель поиска
        search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText('Поиск по ФИО...')
        self.search_field.textChanged.connect(self.filter_table)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['Все кафедры'])
        self.filter_combo.currentTextChanged.connect(self.filter_table)
        
        search_layout.addWidget(QLabel('Поиск:'))
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(QLabel('Кафедра:'))
        search_layout.addWidget(self.filter_combo)
        main_layout.addLayout(search_layout)

        # Панель с кнопками
        button_layout = QHBoxLayout()
        
        add_button = QPushButton('Добавить студента')
        edit_button = QPushButton('Редактировать')
        delete_button = QPushButton('Удалить')
        stats_button = QPushButton('Статистика')
        backup_button = QPushButton('Создать резервную копию')
        restore_button = QPushButton('Восстановить из копии')
        
        add_button.clicked.connect(self.add_student)
        edit_button.clicked.connect(self.edit_student)
        delete_button.clicked.connect(self.delete_student)
        stats_button.clicked.connect(self.show_statistics)
        backup_button.clicked.connect(self.show_backup_dialog)
        restore_button.clicked.connect(self.show_restore_dialog)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(stats_button)
        button_layout.addWidget(backup_button)
        button_layout.addWidget(restore_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'ID', 'ФИО', 'Пол', 'Кафедра', 'Преподаватели'
        ])
        
        # Настройка таблицы
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Настройка заголовков
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        self.table.doubleClicked.connect(self.on_table_double_click)
        
        main_layout.addWidget(self.table)
        
        # Загружаем данные
        self.update_department_filter()
        self.load_students()

    def filter_table(self):
        """Фильтрация таблицы по поисковому запросу и кафедре"""
        search_text = self.search_field.text().lower()
        selected_dept = self.filter_combo.currentText()

        for row in range(self.table.rowCount()):
            hide_row = False
            
            # Проверяем поисковый запрос
            if search_text:
                name = self.table.item(row, 1).text().lower()
                if search_text not in name:
                    hide_row = True
            
            # Проверяем фильтр по кафедре
            if selected_dept != 'Все кафедры':
                dept = self.table.item(row, 3).text()
                if dept != selected_dept:
                    hide_row = True
            
            self.table.setRowHidden(row, hide_row)

    def update_department_filter(self):
        """Обновление списка кафедр в фильтре"""
        departments = self.student_controller.get_departments()
        self.filter_combo.clear()
        self.filter_combo.addItem('Все кафедры')
        self.filter_combo.addItems([d['name'] for d in departments])

    def show_statistics(self):
        """Показать окно статистики"""
        dialog = StatisticsDialog(self.student_controller, self)
        dialog.exec_()

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
        self.logger.info("Открыта форма добавления студента")
        dialog = StudentDialog(self)
        if dialog.exec_():
            self.load_students()
            self.logger.info("Форма добавления студента закрыта")

    def edit_student(self):
        """Редактирование выбранного студента"""
        current_row = self.table.currentRow()
        if current_row < 0:
            self.logger.warning("Попытка редактирования без выбора студента")
            QMessageBox.warning(self, 'Предупреждение', 
                              'Пожалуйста, выберите студента для редактирования')
            return
            
        student_id = int(self.table.item(current_row, 0).text())
        self.logger.info(f"Открыта форма редактирования студента (ID: {student_id})")
        dialog = StudentDialog(self, student_id)
        if dialog.exec_():
            self.load_students()
            self.logger.info(f"Завершено редактирование студента (ID: {student_id})")

    def delete_student(self):
        """Удаление выбранного студента"""
        current_row = self.table.currentRow()
        if current_row < 0:
            self.logger.warning("Попытка удаления без выбора студента")
            QMessageBox.warning(self, 'Предупреждение', 
                              'Пожалуйста, выберите студента для удаления')
            return
            
        student_id = int(self.table.item(current_row, 0).text())
        student_name = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(self, 'Подтверждение', 
                                   'Вы уверены, что хотите удалить этого студента?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.logger.info(f"Попытка удаления студента: {student_name} (ID: {student_id})")
            success, message = self.student_controller.delete_student(student_id)
            if success:
                self.load_students()
            else:
                self.logger.error(f"Ошибка при удалении студента: {message}")
                QMessageBox.critical(self, 'Ошибка', 
                                   f'Не удалось удалить студента: {message}')

    def on_table_double_click(self, index):
        """Обработка двойного клика по таблице"""
        student_id = int(self.table.item(index.row(), 0).text())
        student_name = self.table.item(index.row(), 1).text()
        self.logger.info(f"Открыта форма редактирования студента по двойному клику: {student_name} (ID: {student_id})")
        dialog = StudentDialog(self, student_id)
        if dialog.exec_():
            self.load_students()
            self.logger.info(f"Завершено редактирование студента: {student_name} (ID: {student_id})")

    def show_backup_dialog(self):
        dialog = BackupDialog(self.student_controller, self)
        dialog.exec_()

    def show_restore_dialog(self):
        """Показать диалог восстановления из резервной копии"""
        dialog = RestoreDialog(self.student_controller, self)
        if dialog.exec_() == QDialog.Accepted:
            reply = QMessageBox.question(
                self,
                'Перезапуск приложения',
                'Для применения изменений необходимо перезапустить приложение. '
                'Перезапустить сейчас?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.logger.info("Перезапуск приложения после восстановления из резервной копии")
                self.restart_signal.emit()  # Испускаем сигнал для перезапуска
            else:
                QMessageBox.information(
                    self,
                    'Информация',
                    'Изменения вступят в силу после перезапуска приложения'
                )