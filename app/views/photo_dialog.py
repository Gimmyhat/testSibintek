from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFileDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import shutil

class PhotoDialog(QDialog):
    def __init__(self, student_id, photo_path=None, parent=None):
        super().__init__(parent)
        self.student_id = student_id
        self.photo_path = photo_path
        self.new_photo_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Фотография студента')
        self.setMinimumSize(400, 500)
        
        layout = QVBoxLayout(self)
        
        # Область для фото
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setMinimumSize(300, 400)
        self.photo_label.setStyleSheet('border: 1px solid gray')
        
        # Загружаем фото если есть
        if self.photo_path and os.path.exists(self.photo_path):
            pixmap = QPixmap(self.photo_path)
            self.photo_label.setPixmap(pixmap.scaled(
                300, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        
        # Кнопки
        button_layout = QHBoxLayout()
        load_button = QPushButton('Загрузить фото')
        delete_button = QPushButton('Удалить фото')
        close_button = QPushButton('Закрыть')
        
        load_button.clicked.connect(self.load_photo)
        delete_button.clicked.connect(self.delete_photo)
        close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(load_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(close_button)
        
        layout.addWidget(self.photo_label)
        layout.addLayout(button_layout)

    def load_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            'Выберите фотографию',
            '',
            'Images (*.png *.jpg *.jpeg)'
        )
        
        if file_name:
            # Создаем директорию для фото если её нет
            photos_dir = 'photos'
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)
            
            # Копируем файл в директорию photos
            new_file_name = f'student_{self.student_id}{os.path.splitext(file_name)[1]}'
            new_path = os.path.join(photos_dir, new_file_name)
            shutil.copy2(file_name, new_path)
            
            # Обновляем отображение
            pixmap = QPixmap(new_path)
            self.photo_label.setPixmap(pixmap.scaled(
                300, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            
            self.new_photo_path = new_path

    def delete_photo(self):
        self.photo_label.clear()
        if self.photo_path and os.path.exists(self.photo_path):
            os.remove(self.photo_path)
        self.new_photo_path = None 