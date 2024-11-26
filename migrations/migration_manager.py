import sqlite3
import os
from datetime import datetime
from config.settings import DATABASE

class MigrationManager:
    def __init__(self):
        self.db_path = DATABASE['name']
        self.migrations_dir = DATABASE['migrations_dir']
        self.init_migrations_table()

    def init_migrations_table(self):
        """Инициализация таблицы миграций"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def create_migration(self, name: str):
        """Создание нового файла миграции"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{name}.py"
        filepath = os.path.join(self.migrations_dir, filename)

        template = '''"""
{name}
Migration: {timestamp}
"""

def upgrade(cursor):
    """Применение миграции"""
    cursor.execute("""
        -- Ваш SQL код здесь
    """)

def downgrade(cursor):
    """Откат миграции"""
    cursor.execute("""
        -- Ваш SQL код для отката здесь
    """)
'''

        with open(filepath, 'w') as f:
            f.write(template.format(
                name=name,
                timestamp=timestamp
            ))

    def get_applied_migrations(self):
        """Получение списка примененных миграций"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM migrations')
            return {row[0] for row in cursor.fetchall()}

    def apply_migrations(self):
        """Применение всех неприменённых миграций"""
        applied = self.get_applied_migrations()
        
        # Получаем все файлы миграций
        migration_files = sorted([
            f for f in os.listdir(self.migrations_dir)
            if f.endswith('.py') and f != '__init__.py'
        ])

        for file in migration_files:
            name = file[:-3]  # Убираем .py
            if name not in applied:
                print(f"Applying migration: {name}")
                
                # Импортируем и выполняем миграцию
                migration = __import__(f"migrations.{name}", fromlist=['upgrade'])
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    migration.upgrade(cursor)
                    cursor.execute(
                        'INSERT INTO migrations (name) VALUES (?)',
                        (name,)
                    ) 