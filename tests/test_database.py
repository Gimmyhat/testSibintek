import pytest
import sqlite3

def test_database_initialization(test_db):
    """Тест создания таблиц в базе данных"""
    with sqlite3.connect(test_db.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        
        assert "departments" in tables
        assert "teachers" in tables
        assert "students" in tables
        assert "student_teachers" in tables