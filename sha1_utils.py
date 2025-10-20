"""
Утилиты для вычисления SHA1 хеша файлов изображений (без зависимости от Django).
"""
import hashlib
import os


def get_image_file_sha1_hash(file_path):
    """
    Получить SHA1 хеш файла по его пути.
    
    Args:
        file_path (str): Путь к файлу изображения
        
    Returns:
        str: SHA1 хеш в шестнадцатеричном формате или None если файл не существует
    """
    try:
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'rb') as image_file:
            sha1_hash = hashlib.sha1()
            
            # Читаем файл блоками для эффективности памяти
            for chunk in iter(lambda: image_file.read(4096), b""):
                sha1_hash.update(chunk)
            
            return sha1_hash.hexdigest()
            
    except (IOError, OSError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def get_image_field_sha1_hash(image_field):
    """
    Получить SHA1 хеш Django ImageField.
    
    Args:
        image_field: Django ImageField объект
        
    Returns:
        str: SHA1 хеш в шестнадцатеричном формате или None если файл не существует
    """
    if not image_field:
        return None
        
    try:
        # Используем Django storage для открытия файла
        with image_field.open('rb') as image_file:
            sha1_hash = hashlib.sha1()
            
            # Читаем файл блоками для эффективности памяти
            for chunk in iter(lambda: image_file.read(4096), b""):
                sha1_hash.update(chunk)
            
            return sha1_hash.hexdigest()
            
    except (IOError, OSError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def calculate_sha1_from_bytes(data):
    """
    Вычислить SHA1 хеш из байтовых данных.
    
    Args:
        data (bytes): Байтовые данные
        
    Returns:
        str: SHA1 хеш в шестнадцатеричном формате
    """
    return hashlib.sha1(data).hexdigest()


if __name__ == "__main__":
    # Пример использования
    import tempfile
    
    # Создаем тестовые данные
    test_data = b"Test image data for SHA1 hashing"
    expected_hash = calculate_sha1_from_bytes(test_data)
    
    print("=== Демонстрация вычисления SHA1 хеша ===")
    print(f"Тестовые данные: {test_data}")
    print(f"Ожидаемый SHA1: {expected_hash}")
    
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(test_data)
        temp_file_path = temp_file.name
    
    try:
        # Вычисляем хеш файла
        file_hash = get_image_file_sha1_hash(temp_file_path)
        print(f"SHA1 файла: {file_hash}")
        
        # Проверяем совпадение
        if file_hash == expected_hash:
            print("✅ Хеши совпадают!")
        else:
            print("❌ Хеши не совпадают!")
            
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)
    
    # Тест с несуществующим файлом
    print(f"\nТест с несуществующим файлом:")
    result = get_image_file_sha1_hash("/nonexistent/file.jpg")
    print(f"Результат: {result}")  # Должно быть None