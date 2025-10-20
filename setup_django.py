#!/usr/bin/env python
"""
Скрипт для настройки Django проекта и выполнения миграций
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_django():
    """
    Настройка Django проекта
    """
    print("🔧 Настройка Django проекта...")
    
    # Устанавливаем переменную окружения
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagehash.settings')
    
    # Инициализируем Django
    django.setup()
    
    print("✅ Django инициализирован")
    
    # Выполняем миграции
    print("📦 Выполнение миграций...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Миграции выполнены успешно")
    except Exception as e:
        print(f"⚠️ Ошибка при выполнении миграций: {e}")
        print("Попробуйте выполнить команды вручную:")
        print("python manage.py makemigrations")
        print("python manage.py migrate")

if __name__ == "__main__":
    setup_django()