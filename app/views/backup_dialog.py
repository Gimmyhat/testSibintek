from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QProgressBar)
from PyQt5.QtCore import Qt, QTimer

class BackupDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Резервное копирование')
        self.setMinimumWidth(300)
        
        layout = QVBoxLayout(self)
        
        # Информационная метка
        self.info_label = QLabel('Создание резервной копии...')
        layout.addWidget(self.info_label)
        
        # Прогресс бар
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Бесконечный прогресс
        layout.addWidget(self.progress)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.backup_button = QPushButton('Создать копию')
        close_button = QPushButton('Закрыть')
        
        self.backup_button.clicked.connect(self.create_backup)
        close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.backup_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

    def create_backup(self):
        self.backup_button.setEnabled(False)
        self.progress.setRange(0, 0)
        
        # Создаем резервную копию
        success, message = self.controller.backup_database()
        
        # Обновляем интерфейс
        self.progress.setRange(0, 100)
        self.progress.setValue(100 if success else 0)
        self.info_label.setText(message)
        self.backup_button.setEnabled(True) 