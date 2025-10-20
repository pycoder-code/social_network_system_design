#!/usr/bin/env python
"""
Примеры использования функциональности для получения SHA1 хеша изображений
из Django ImageField
"""

import os
import sys
import django
from django.core.files.uploadedfile import SimpleUploadedFile

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagehash.settings')
django.setup()

from imagehash.models import ImageWithHash, ImageHashUtility


def example_basic_usage():
    """
    Базовый пример использования
    """
    print("=== Базовый пример использования ===")
    
    # Создаем тестовое изображение (1x1 пиксель PNG)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Создаем объект загруженного файла
    uploaded_file = SimpleUploadedFile(
        "test_image.png",
        test_image_data,
        content_type="image/png"
    )
    
    # Создаем объект изображения
    image_obj = ImageWithHash(
        name="Тестовое изображение",
        image=uploaded_file
    )
    
    # Сохраняем (хеш будет вычислен автоматически)
    image_obj.save()
    
    print(f"Изображение создано с ID: {image_obj.id}")
    print(f"SHA1 хеш: {image_obj.image_hash}")
    print(f"URL изображения: {image_obj.image.url}")
    
    return image_obj


def example_manual_hash_calculation():
    """
    Пример ручного вычисления хеша
    """
    print("\n=== Ручное вычисление хеша ===")
    
    # Получаем существующее изображение
    image_obj = ImageWithHash.objects.first()
    if not image_obj:
        print("Нет изображений в базе данных")
        return
    
    # Вычисляем хеш вручную
    hash_value = image_obj.get_image_sha1_hash()
    print(f"Вычисленный хеш: {hash_value}")
    
    # Обновляем хеш в базе данных
    image_obj.update_hash()
    print(f"Хеш обновлен в базе данных: {image_obj.image_hash}")


def example_utility_functions():
    """
    Пример использования утилитарных функций
    """
    print("\n=== Использование утилитарных функций ===")
    
    image_obj = ImageWithHash.objects.first()
    if not image_obj:
        print("Нет изображений в базе данных")
        return
    
    # Вычисление хеша через утилиту
    hash_from_utility = ImageHashUtility.calculate_django_file_hash(image_obj.image)
    print(f"Хеш через утилиту: {hash_from_utility}")
    
    # Сравнение с хешем в базе данных
    if hash_from_utility == image_obj.image_hash:
        print("✅ Хеши совпадают!")
    else:
        print("❌ Хеши не совпадают!")


def example_search_and_duplicates():
    """
    Пример поиска и поиска дубликатов
    """
    print("\n=== Поиск и дубликаты ===")
    
    # Создаем дубликат изображения
    original_image = ImageWithHash.objects.first()
    if original_image:
        # Создаем копию с тем же содержимым
        duplicate_image = ImageWithHash(
            name="Дубликат изображения",
            image=original_image.image  # Тот же файл
        )
        duplicate_image.save()
        
        print(f"Создан дубликат с ID: {duplicate_image.id}")
        print(f"Хеш дубликата: {duplicate_image.image_hash}")
        
        # Поиск по хешу
        images_with_same_hash = ImageWithHash.find_by_hash(original_image.image_hash)
        print(f"Найдено изображений с хешем {original_image.image_hash}: {images_with_same_hash.count()}")
        
        # Поиск дубликатов
        duplicates = ImageWithHash.find_duplicates()
        print(f"Найдено групп дубликатов: {len(duplicates)}")
        
        for hash_value, images in duplicates.items():
            print(f"Хеш {hash_value}: {images.count()} изображений")


def example_file_path_hash():
    """
    Пример вычисления хеша файла по пути
    """
    print("\n=== Вычисление хеша файла по пути ===")
    
    image_obj = ImageWithHash.objects.first()
    if not image_obj:
        print("Нет изображений в базе данных")
        return
    
    # Получаем путь к файлу
    file_path = image_obj.image.path
    print(f"Путь к файлу: {file_path}")
    
    # Вычисляем хеш по пути
    hash_from_path = ImageHashUtility.calculate_file_hash(file_path)
    print(f"Хеш по пути: {hash_from_path}")
    
    # Сравниваем с хешем в базе данных
    if hash_from_path == image_obj.image_hash:
        print("✅ Хеши совпадают!")
    else:
        print("❌ Хеши не совпадают!")


def example_comparison():
    """
    Пример сравнения изображений
    """
    print("\n=== Сравнение изображений ===")
    
    images = ImageWithHash.objects.all()[:2]
    if len(images) < 2:
        print("Нужно минимум 2 изображения для сравнения")
        return
    
    img1, img2 = images[0], images[1]
    
    print(f"Изображение 1: {img1.name} (хеш: {img1.image_hash})")
    print(f"Изображение 2: {img2.name} (хеш: {img2.image_hash})")
    
    are_same = ImageHashUtility.compare_images_by_hash(img1, img2)
    print(f"Изображения одинаковые: {'Да' if are_same else 'Нет'}")


def cleanup_database():
    """
    Очистка базы данных от тестовых данных
    """
    print("\n=== Очистка базы данных ===")
    count = ImageWithHash.objects.count()
    ImageWithHash.objects.all().delete()
    print(f"Удалено {count} записей")


if __name__ == "__main__":
    print("🔍 Примеры использования Django ImageField SHA1 Hash Calculator")
    print("=" * 60)
    
    try:
        # Запускаем примеры
        example_basic_usage()
        example_manual_hash_calculation()
        example_utility_functions()
        example_search_and_duplicates()
        example_file_path_hash()
        example_comparison()
        
        # Очищаем базу данных
        cleanup_database()
        
        print("\n✅ Все примеры выполнены успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении примеров: {e}")
        import traceback
        traceback.print_exc()