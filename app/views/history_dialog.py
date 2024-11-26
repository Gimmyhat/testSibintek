from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QHeaderView)
from PyQt5.QtCore import Qt

class HistoryDialog(QDialog):
    def __init__(self, controller, student_id, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.student_id = student_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('История изменений')
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Создаем таблицу
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            'Поле', 'Старое значение', 'Новое значение', 'Дата изменения'
        ])
        
        # Настраиваем таблицу
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Загружаем историю
        self.load_history()
        
        # Кнопка закрытия
        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(self.accept)
        
        layout.addWidget(self.table)
        layout.addWidget(close_button)

    def load_history(self):
        history = self.controller.get_student_history(self.student_id)
        self.table.setRowCount(len(history))
        
        for row, record in enumerate(history):
            self.table.setItem(row, 0, QTableWidgetItem(record['field']))
            self.table.setItem(row, 1, QTableWidgetItem(str(record['old_value'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(record['new_value'])))
            self.table.setItem(row, 3, QTableWidgetItem(record['date'])) 