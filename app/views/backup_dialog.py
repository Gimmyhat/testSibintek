from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
import os
import shutil
from datetime import datetime

class BackupDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Резервное копирование')
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Информационная метка
        self.info_label = QLabel('Нажмите кнопку для создания резервной копии')
        layout.addWidget(self.info_label)
        
        # Прогресс бар
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
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
        try:
            self.backup_button.setEnabled(False)
            self.info_label.setText('Создание резервной копии...')
            self.progress.setValue(25)

            # Создаем директорию для бэкапов если её нет
            backup_dir = 'backups'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # Формируем имя файла бэкапа
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f'backup_{timestamp}.db')

            self.progress.setValue(50)

            # Копируем файл базы данных
            shutil.copy2(self.controller.db.db_name, backup_path)

            self.progress.setValue(100)
            self.info_label.setText(f'Резервная копия создана: {backup_path}')
            
            QMessageBox.information(
                self,
                'Успех',
                'Резервная копия успешно создана'
            )

        except Exception as e:
            self.info_label.setText(f'Ошибка: {str(e)}')
            QMessageBox.critical(
                self,
                'Ошибка',
                f'Не удалось создать резервную копию: {str(e)}'
            )
        finally:
            self.backup_button.setEnabled(True) 