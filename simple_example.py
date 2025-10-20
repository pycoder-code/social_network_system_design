#!/usr/bin/env python
"""
Простой пример получения SHA1 хеша содержимого изображения
без использования Django (только hashlib)
"""

import hashlib
import os
from io import BytesIO


def calculate_file_hash(file_path):
    """
    Вычисляет SHA1 хеш файла по пути
    
    Args:
        file_path (str): Путь к файлу
        
    Returns:
        str: SHA1 хеш в шестнадцатеричном формате
    """
    sha1_hash = hashlib.sha1()
    
    with open(file_path, 'rb') as f:
        # Читаем файл по частям для экономии памяти
        for chunk in iter(lambda: f.read(4096), b""):
            sha1_hash.update(chunk)
    
    return sha1_hash.hexdigest()


def calculate_bytes_hash(data):
    """
    Вычисляет SHA1 хеш из байтовых данных
    
    Args:
        data (bytes): Байтовые данные
        
    Returns:
        str: SHA1 хеш в шестнадцатеричном формате
    """
    return hashlib.sha1(data).hexdigest()


def calculate_file_like_hash(file_like_object):
    """
    Вычисляет SHA1 хеш из файлоподобного объекта
    
    Args:
        file_like_object: Объект с методом read() (например, BytesIO)
        
    Returns:
        str: SHA1 хеш в шестнадцатеричном формате
    """
    sha1_hash = hashlib.sha1()
    
    # Переходим в начало файла
    file_like_object.seek(0)
    
    # Читаем все содержимое
    data = file_like_object.read()
    sha1_hash.update(data)
    
    return sha1_hash.hexdigest()


def create_test_image_data():
    """
    Создает тестовые данные изображения (1x1 пиксель PNG)
    """
    # Минимальный PNG файл (1x1 пиксель, прозрачный)
    return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'


def main():
    """
    Демонстрация различных способов вычисления SHA1 хеша
    """
    print("🔍 Простой пример получения SHA1 хеша содержимого изображения")
    print("=" * 70)
    
    # Создаем тестовые данные изображения
    print("1. Создание тестовых данных изображения...")
    image_data = create_test_image_data()
    print(f"   ✅ Размер данных: {len(image_data)} байт")
    
    # Способ 1: Вычисление хеша из байтовых данных
    print("\n2. Вычисление хеша из байтовых данных...")
    hash_from_bytes = calculate_bytes_hash(image_data)
    print(f"   ✅ SHA1 хеш: {hash_from_bytes}")
    
    # Способ 2: Вычисление хеша из файлоподобного объекта
    print("\n3. Вычисление хеша из файлоподобного объекта...")
    file_like = BytesIO(image_data)
    hash_from_file_like = calculate_file_like_hash(file_like)
    print(f"   ✅ SHA1 хеш: {hash_from_file_like}")
    print(f"   ✅ Хеши совпадают: {hash_from_bytes == hash_from_file_like}")
    
    # Способ 3: Сохранение в файл и вычисление хеша по пути
    print("\n4. Сохранение в файл и вычисление хеша по пути...")
    test_file_path = "/tmp/test_image.png"
    
    with open(test_file_path, 'wb') as f:
        f.write(image_data)
    
    hash_from_file = calculate_file_hash(test_file_path)
    print(f"   ✅ SHA1 хеш: {hash_from_file}")
    print(f"   ✅ Хеши совпадают: {hash_from_bytes == hash_from_file}")
    
    # Очистка
    os.remove(test_file_path)
    print("   ✅ Временный файл удален")
    
    # Демонстрация с разными изображениями
    print("\n5. Сравнение разных изображений...")
    
    # Создаем второе изображение (немного другое)
    image_data_2 = image_data + b'\x00'  # Добавляем один байт
    
    hash_1 = calculate_bytes_hash(image_data)
    hash_2 = calculate_bytes_hash(image_data_2)
    
    print(f"   ✅ Хеш изображения 1: {hash_1}")
    print(f"   ✅ Хеш изображения 2: {hash_2}")
    print(f"   ✅ Изображения одинаковые: {hash_1 == hash_2}")
    
    # Демонстрация с одинаковыми изображениями
    print("\n6. Сравнение одинаковых изображений...")
    image_data_copy = image_data  # Тот же объект
    hash_copy = calculate_bytes_hash(image_data_copy)
    
    print(f"   ✅ Хеш оригинала: {hash_1}")
    print(f"   ✅ Хеш копии: {hash_copy}")
    print(f"   ✅ Изображения одинаковые: {hash_1 == hash_copy}")
    
    print("\n✅ Демонстрация завершена успешно!")
    print("\n📝 Основные принципы:")
    print("   - SHA1 хеш вычисляется для содержимого файла, а не для имени")
    print("   - Одинаковые файлы всегда имеют одинаковый хеш")
    print("   - Разные файлы (даже на 1 байт) имеют разные хеши")
    print("   - Хеш не зависит от пути к файлу или его атрибутов")
    print("\n🔧 Для Django ImageField используйте:")
    print("   - image_obj.get_image_sha1_hash() - получить хеш")
    print("   - image_obj.image_hash - поле с хешем")


if __name__ == "__main__":
    main()