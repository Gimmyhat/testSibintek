import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'
PHOTOS_DIR = BASE_DIR / 'photos'
BACKUPS_DIR = BASE_DIR / 'backups'

# Создаем необходимые директории
for directory in [DATA_DIR, LOGS_DIR, PHOTOS_DIR, BACKUPS_DIR]:
    directory.mkdir(exist_ok=True)

# Настройки базы данных
DATABASE = {
    'name': str(DATA_DIR / 'student_manager.db'),
    'backup_path': BACKUPS_DIR,
    'migrations_dir': BASE_DIR / 'migrations'
}

# Настройки логирования
LOGGING = {
    'filename': str(LOGS_DIR / 'student_manager_{date}.log'),
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}

# Настройки приложения
APP = {
    'title': 'Менеджер студентов',
    'window_size': (800, 600),
    'window_position': (100, 100),
    'max_photo_size': 1024 * 1024  # 1MB
}

# Валидация
VALIDATION = {
    'max_name_length': 40,
    'max_middle_name_length': 60,
    'allowed_photo_extensions': ['.jpg', '.jpeg', '.png'],
    'email_pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone_pattern': r'^\+?[1-9]\d{10,11}$'
} 