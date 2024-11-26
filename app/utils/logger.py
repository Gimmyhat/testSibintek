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
            self.logs_dir = os.path.join('logs')
            if not os.path.exists(self.logs_dir):
                os.makedirs(self.logs_dir)

            # Создаем логгер только если его еще нет
            self.logger = logging.getLogger('StudentManager')
            if not self.logger.handlers:  # Проверяем наличие обработчиков
                self.logger.setLevel(logging.INFO)

                # Форматтер для всех обработчиков
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

                # Файловый обработчик
                current_date = datetime.now().strftime('%Y-%m-%d')
                file_handler = logging.FileHandler(
                    os.path.join(self.logs_dir, f'student_manager_{current_date}.log'),
                    encoding='utf-8'
                )
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

                # Консольный обработчик
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

            Logger._initialized = True

    def __getattr__(self, name):
        """Проксируем все неизвестные атрибуты к self.logger"""
        return getattr(self.logger, name) 