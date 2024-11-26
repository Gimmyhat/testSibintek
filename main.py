import sys
import os
from PyQt5.QtWidgets import QApplication
from app.views.main_window import MainWindow

def restart_application():
    """Перезапуск приложения"""
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.restart_signal.connect(restart_application)  # Подключаем сигнал
    window.show()
    sys.exit(app.exec_()) 