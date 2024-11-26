import PyInstaller.__main__
import os
import shutil
from scripts.generate_resources import create_icon, create_splash

def build_app():
    # Создаем директорию для ресурсов если её нет
    resources_dir = os.path.join('app', 'resources')
    os.makedirs(resources_dir, exist_ok=True)

    # Генерируем ресурсы
    create_icon()
    create_splash()

    # Проверяем наличие ресурсов
    icon_path = os.path.join(resources_dir, 'icon.ico')
    splash_path = os.path.join(resources_dir, 'splash.png')

    if not (os.path.exists(icon_path) and os.path.exists(splash_path)):
        raise FileNotFoundError("Ресурсы не были созданы")

    # Получаем абсолютные пути
    base_path = os.path.abspath(os.path.dirname(__file__))
    icon_path = os.path.join(base_path, icon_path)

    # Создаем список файлов для добавления
    datas = [
        (resources_dir, 'app/resources'),
    ]

    # Запускаем PyInstaller
    PyInstaller.__main__.run([
        'main.py',
        '--name=StudentManager',
        '--onefile',
        '--windowed',
        f'--icon={icon_path}',
        *[f'--add-data={src};{dst}' for src, dst in datas],
        '--clean',
        '--noconfirm'
    ])

if __name__ == "__main__":
    build_app() 