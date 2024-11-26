import logging
import os
from datetime import datetime

class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            # Создаем директорию для логов если её нет
            self.logs_dir = 'logs'
            if not os.path.exists(self.logs_dir):
                os.makedirs(self.logs_dir)

            # Создаем имя файла лога с текущей датой
            current_date = datetime.now().strftime('%Y-%m-%d')
            log_file = os.path.join(self.logs_dir, f'student_manager_{current_date}.log')

            # Настраиваем логгер
            self.logger = logging.getLogger('StudentManager')
            self.logger.setLevel(logging.INFO)

            # Проверяем, нет ли уже обработчиков
            if not self.logger.handlers:
                # Создаем обработчик для файла
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(logging.INFO)

                # Создаем обработчик для консоли
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.INFO)

                # Создаем форматтер
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)
                console_handler.setFormatter(formatter)

                # Добавляем обработчики к логгеру
                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)

            Logger._initialized = True

    def info(self, message):
        """Логирование информационных сообщений"""
        self.logger.info(message)

    def error(self, message):
        """Логирование ошибок"""
        self.logger.error(message)

    def warning(self, message):
        """Логирование предупреждений"""
        self.logger.warning(message)

    def debug(self, message):
        """Логирование отладочной информации"""
        self.logger.debug(message) 