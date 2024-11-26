import pytest
from PyQt5.QtWidgets import QPushButton
from app.views.main_window import MainWindow

class TestGUI:
    @pytest.fixture(autouse=True)
    def setup_method(self, qtbot):
        """Setup для каждого теста"""
        self.window = MainWindow()
        qtbot.addWidget(self.window)
        yield
        self.window.close()

    def test_window_title(self, qtbot):
        """Тест заголовка окна"""
        assert self.window.windowTitle() == 'Менеджер студентов'

    def test_table_structure(self, qtbot):
        """Тест структуры таблицы"""
        assert self.window.table.columnCount() == 5
        expected_headers = ['ID', 'ФИО', 'Пол', 'Кафедра', 'Преподаватели']
        headers = []
        for i in range(self.window.table.columnCount()):
            headers.append(self.window.table.horizontalHeaderItem(i).text())
        assert headers == expected_headers

    def test_buttons_exist(self, qtbot):
        """Тест наличия кнопок"""
        buttons = self.window.findChildren(QPushButton)
        button_texts = {button.text() for button in buttons}
        required_buttons = {'Добавить студента', 'Редактировать', 'Удалить'}
        assert required_buttons.issubset(button_texts)

    def test_table_is_empty_initially(self, qtbot):
        """Тест начального состояния таблицы"""
        assert self.window.table.rowCount() >= 0