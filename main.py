import sys
import os
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QScreen
from app.views.main_window import MainWindow
from app.resources.resources import get_icon, get_splash

def restart_application():
    """Перезапуск приложения"""
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    try:
        # Устанавливаем иконку приложения
        app_icon = get_icon()
        app.setWindowIcon(app_icon)
        
        # Создаем и показываем splash screen
        splash_pix = get_splash()
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.setEnabled(False)
        
        # Центрируем splash screen
        screen = app.primaryScreen().availableGeometry()
        splash_rect = splash.frameGeometry()
        splash_rect.moveCenter(screen.center())
        splash.move(splash_rect.topLeft())
        
        # Добавляем текст на splash screen
        splash.showMessage("Загрузка приложения...", 
                          Qt.AlignBottom | Qt.AlignCenter, 
                          Qt.white)
        splash.show()
        app.processEvents()
        
        # Создаем главное окно
        window = MainWindow()
        window.restart_signal.connect(restart_application)
        
        # Задержка для отображения splash screen
        QTimer.singleShot(2000, lambda: [
            window.show(),
            splash.finish(window)
        ])
        
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Ошибка при запуске приложения: {str(e)}")
        sys.exit(1) 