from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Создание иконки приложения"""
    # Создаем изображение
    size = (256, 256)
    icon = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Рисуем круг
    draw.ellipse([20, 20, 236, 236], fill='#2196F3')
    
    # Добавляем текст
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    draw.text((85, 60), "S", fill='white', font=font)
    
    # Создаем директорию resources если её нет
    os.makedirs('app/resources', exist_ok=True)
    
    # Сохраняем как .ico
    icon.save('app/resources/icon.ico', format='ICO')

def create_splash():
    """Создание splash screen"""
    # Создаем изображение
    size = (600, 400)
    splash = Image.new('RGBA', size, '#1976D2')
    draw = ImageDraw.Draw(splash)
    
    # Добавляем градиент
    for y in range(size[1]):
        alpha = int(255 * (1 - y/size[1]))
        draw.line([(0, y), (size[0], y)], fill=(25, 118, 210, alpha))
    
    # Добавляем текст
    try:
        font = ImageFont.truetype("arial.ttf", 48)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Добавляем тень
    draw.text((153, 153), "Student Manager", fill=(0, 0, 0, 128), font=font)
    # Основной текст
    draw.text((150, 150), "Student Manager", fill='white', font=font)
    # Подзаголовок
    draw.text((200, 250), "Version 1.0", fill='white', font=small_font)
    
    # Сохраняем как PNG
    splash.save('app/resources/splash.png', format='PNG')

if __name__ == "__main__":
    create_icon()
    create_splash()
    print("Ресурсы успешно созданы в директории app/resources/") 