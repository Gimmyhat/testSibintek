# 📚 Менеджер студентов

> Приложение для управления данными студентов с графическим интерфейсом.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![PyQt Version](https://img.shields.io/badge/PyQt-5.15.9-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Возможности

- 📝 **Управление данными студентов**
  - Добавление, редактирование, удаление
  - Поиск и фильтрация
  - Привязка к кафедрам и преподавателям

- 📸 **Работа с фотографиями**
  - Загрузка и хранение фотографий
  - Просмотр и редактирование

- 📊 **Дополнительные функции**
  - История изменений данных
  - Статистика
  - Резервное копирование

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.11 или выше
- Git

### Установка

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/Gimmyhat/testSibintek.git
   cd testSibintek
   ```

2. **Создание виртуального окружения**
   ```bash
   python -m venv venv
   ```

3. **Активация окружения**
   
   Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```

### 🎯 Запуск

```bash
python main.py
```

## 🛠 Разработка

### Миграции

Создание новой миграции:
```bash
python -m migrations.migration_manager create "название_миграции"
```

Применение миграций:
```bash
python -m migrations.migration_manager apply
```

Откат миграций:
```bash
python -m migrations.migration_manager rollback
```

### Тестирование

Запуск всех тестов:
```bash
pytest
```


## 📊 Основные функции

### 👥 Работа со студентами
- Управление данными
- Поиск и фильтрация
- Привязка к кафедрам

### 📸 Работа с фотографиями
- Загрузка и просмотр
- Управление изображениями

### 📜 История и backup
- Отслеживание изменений
- Резервное копирование

## ⚙️ Конфигурация

Основные настройки находятся в `config/settings.py`:
- 📁 Пути к директориям
- 🗄️ Настройки базы данных
- 📝 Параметры логирования
- ✅ Настройки валидации

## 📄 Лицензия

Этот проект лицензирован под MIT License - подробности в файле [LICENSE](LICENSE)

## 👤 Автор

**Никитченко Александр**
- 📧 Email: [nikitchenko.as@gmail.com]
- 🌐 GitHub: [Gimmyhat]

---

<div align="center">
Made with ❤️ and Python
</div>

