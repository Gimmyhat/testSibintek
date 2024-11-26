import os
import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QResource

def resource_path(relative_path):
    """Получить абсолютный путь к ресурсу"""
    if getattr(sys, 'frozen', False):
        # Если приложение собрано PyInstaller
        base_path = sys._MEIPASS
    else:
        # Если приложение запущено из исходников
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    return os.path.join(base_path, 'app', 'resources', relative_path)

def get_icon():
    """Получить иконку приложения"""
    return QIcon(resource_path('icon.ico'))

def get_splash():
    """Получить изображение для splash screen"""
    return QPixmap(resource_path('splash.png'))
 