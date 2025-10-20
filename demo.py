#!/usr/bin/env python
"""
Демонстрация получения SHA1 хеша содержимого изображения из Django ImageField
"""

import os
import sys
import django
from django.core.files.uploadedfile import SimpleUploadedFile

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagehash.settings')
django.setup()

from imagehash.models import ImageWithHash, ImageHashUtility


def create_test_image():
    """
    Создает тестовое изображение (1x1 пиксель PNG)
    """
    # Минимальный PNG файл (1x1 пиксель, прозрачный)
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Создаем файл с правильным поведением для Django
    from django.core.files.base import ContentFile
    return ContentFile(png_data, name="test_image.png")


def main():
    """
    Основная демонстрация функциональности
    """
    print("🔍 Демонстрация получения SHA1 хеша из Django ImageField")
    print("=" * 60)
    
    try:
        # Создаем тестовое изображение
        print("1. Создание тестового изображения...")
        test_image = create_test_image()
        
        # Создаем объект ImageWithHash
        print("2. Создание объекта ImageWithHash...")
        image_obj = ImageWithHash(
            name="Демо изображение",
            image=test_image
        )
        
        # Сохраняем объект (хеш вычисляется автоматически)
        print("3. Сохранение объекта (хеш вычисляется автоматически)...")
        image_obj.save()
        
        print(f"   ✅ Объект сохранен с ID: {image_obj.id}")
        print(f"   ✅ SHA1 хеш: {image_obj.image_hash}")
        print(f"   ✅ URL изображения: {image_obj.image.url}")
        
        # Демонстрация ручного вычисления хеша
        print("\n4. Ручное вычисление хеша...")
        manual_hash = image_obj.get_image_sha1_hash()
        print(f"   ✅ Вычисленный хеш: {manual_hash}")
        print(f"   ✅ Хеши совпадают: {manual_hash == image_obj.image_hash}")
        
        # Демонстрация утилитарных функций
        print("\n5. Использование утилитарных функций...")
        utility_hash = ImageHashUtility.calculate_django_file_hash(image_obj.image)
        print(f"   ✅ Хеш через утилиту: {utility_hash}")
        print(f"   ✅ Хеши совпадают: {utility_hash == image_obj.image_hash}")
        
        # Создаем дубликат для демонстрации поиска
        print("\n6. Создание дубликата изображения...")
        duplicate_image = ImageWithHash(
            name="Дубликат изображения",
            image=test_image  # Тот же файл
        )
        duplicate_image.save()
        print(f"   ✅ Дубликат создан с ID: {duplicate_image.id}")
        print(f"   ✅ Хеш дубликата: {duplicate_image.image_hash}")
        
        # Поиск по хешу
        print("\n7. Поиск изображений по хешу...")
        found_images = ImageWithHash.find_by_hash(image_obj.image_hash)
        print(f"   ✅ Найдено изображений с хешем {image_obj.image_hash}: {found_images.count()}")
        for img in found_images:
            print(f"      - {img.name} (ID: {img.id})")
        
        # Поиск дубликатов
        print("\n8. Поиск дубликатов...")
        duplicates = ImageWithHash.find_duplicates()
        print(f"   ✅ Найдено групп дубликатов: {len(duplicates)}")
        for hash_value, images in duplicates.items():
            print(f"      - Хеш {hash_value}: {images.count()} изображений")
        
        # Сравнение изображений
        print("\n9. Сравнение изображений...")
        are_same = ImageHashUtility.compare_images_by_hash(image_obj, duplicate_image)
        print(f"   ✅ Изображения одинаковые: {'Да' if are_same else 'Нет'}")
        
        print("\n✅ Демонстрация завершена успешно!")
        print("\n📝 Основные методы для получения SHA1 хеша:")
        print("   - image_obj.get_image_sha1_hash() - получить хеш изображения")
        print("   - image_obj.image_hash - поле с хешем (заполняется автоматически)")
        print("   - ImageHashUtility.calculate_django_file_hash(file) - утилита")
        print("   - ImageHashUtility.calculate_file_hash(path) - по пути к файлу")
        
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении демонстрации: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()