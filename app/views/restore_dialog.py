from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QProgressBar, QMessageBox, QListWidget)
from PyQt5.QtCore import Qt
import os
import shutil
from datetime import datetime

class RestoreDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Восстановление из резервной копии')
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout(self)
        
        # Информационная метка
        self.info_label = QLabel('Выберите резервную копию для восстановления:')
        layout.addWidget(self.info_label)
        
        # Список резервных копий
        self.backup_list = QListWidget()
        self.load_backups()
        layout.addWidget(self.backup_list)
        
        # Прогресс бар
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.restore_button = QPushButton('Восстановить')
        refresh_button = QPushButton('Обновить список')
        close_button = QPushButton('Закрыть')
        
        self.restore_button.clicked.connect(self.restore_backup)
        refresh_button.clicked.connect(self.load_backups)
        close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.restore_button)
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

    def load_backups(self):
        """Загрузка списка резервных копий"""
        self.backup_list.clear()
        backup_dir = 'backups'
        if os.path.exists(backup_dir):
            backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
            backups.sort(reverse=True)  # Самые новые сверху
            self.backup_list.addItems(backups)

    def restore_backup(self):
        """Восстановление из выбранной резервной копии"""
        if not self.backup_list.currentItem():
            QMessageBox.warning(self, 'Предупреждение', 
                              'Выберите резервную копию для восстановления')
            return

        reply = QMessageBox.question(
            self,
            'Подтверждение',
            'Все текущие данные будут заменены данными из резервной копии. Продолжить?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.restore_button.setEnabled(False)
                self.progress.setValue(25)
                
                backup_name = self.backup_list.currentItem().text()
                backup_path = os.path.join('backups', backup_name)
                
                # Создаем дополнительную резервную копию текущей базы
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                current_backup = os.path.join('backups', f'pre_restore_{timestamp}.db')
                shutil.copy2(self.controller.db.db_name, current_backup)
                
                self.progress.setValue(50)
                
                # Восстанавливаем из резервной копии
                shutil.copy2(backup_path, self.controller.db.db_name)
                
                self.progress.setValue(100)
                QMessageBox.information(
                    self,
                    'Успех',
                    'База данных успешно восстановлена из резервной копии.\n' +
                    'Перезапустите приложение для применения изменений.'
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Ошибка',
                    f'Не удалось восстановить базу данных: {str(e)}'
                )
            finally:
                self.restore_button.setEnabled(True) 