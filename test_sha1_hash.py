"""
Тесты для функций вычисления SHA1 хеша изображений.
"""
import hashlib
import os
import tempfile
from unittest.mock import Mock, patch, mock_open
import unittest

# Импортируем функции для тестирования
from models import get_image_field_sha1_hash, get_image_file_sha1_hash


class TestSHA1HashFunctions(unittest.TestCase):
    """
    Тесты для функций вычисления SHA1 хеша.
    """
    
    def setUp(self):
        """
        Настройка тестовых данных.
        """
        # Создаем тестовые данные
        self.test_data = b"Test image data for SHA1 hashing"
        self.expected_hash = hashlib.sha1(self.test_data).hexdigest()
    
    def test_get_image_file_sha1_hash_success(self):
        """
        Тест успешного вычисления SHA1 хеша файла.
        """
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(self.test_data)
            temp_file_path = temp_file.name
        
        try:
            # Вычисляем хеш
            result_hash = get_image_file_sha1_hash(temp_file_path)
            
            # Проверяем результат
            self.assertEqual(result_hash, self.expected_hash)
            
        finally:
            # Удаляем временный файл
            os.unlink(temp_file_path)
    
    def test_get_image_file_sha1_hash_nonexistent_file(self):
        """
        Тест обработки несуществующего файла.
        """
        result = get_image_file_sha1_hash("/nonexistent/path/image.jpg")
        self.assertIsNone(result)
    
    def test_get_image_field_sha1_hash_success(self):
        """
        Тест успешного вычисления SHA1 хеша ImageField.
        """
        # Создаем мок ImageField
        mock_image_field = Mock()
        mock_file = mock_open(read_data=self.test_data)
        mock_image_field.open.return_value.__enter__ = mock_file
        mock_image_field.open.return_value.__exit__ = Mock(return_value=None)
        
        # Настраиваем мок для чтения данных блоками
        mock_file.return_value.read.side_effect = [
            self.test_data[:16],  # Первый блок
            self.test_data[16:],  # Второй блок
            b""  # Конец файла
        ]
        
        # Вычисляем хеш
        result_hash = get_image_field_sha1_hash(mock_image_field)
        
        # Проверяем результат
        self.assertEqual(result_hash, self.expected_hash)
    
    def test_get_image_field_sha1_hash_empty_field(self):
        """
        Тест обработки пустого ImageField.
        """
        result = get_image_field_sha1_hash(None)
        self.assertIsNone(result)
        
        result = get_image_field_sha1_hash("")
        self.assertIsNone(result)
    
    def test_get_image_field_sha1_hash_io_error(self):
        """
        Тест обработки ошибки ввода-вывода.
        """
        # Создаем мок ImageField с ошибкой
        mock_image_field = Mock()
        mock_image_field.open.side_effect = IOError("File not found")
        
        # Вычисляем хеш
        result_hash = get_image_field_sha1_hash(mock_image_field)
        
        # Проверяем, что возвращается None при ошибке
        self.assertIsNone(result_hash)
    
    def test_large_file_hash(self):
        """
        Тест вычисления хеша большого файла (проверка чтения блоками).
        """
        # Создаем большие тестовые данные
        large_data = b"x" * 10000  # 10KB данных
        expected_hash = hashlib.sha1(large_data).hexdigest()
        
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(large_data)
            temp_file_path = temp_file.name
        
        try:
            # Вычисляем хеш
            result_hash = get_image_file_sha1_hash(temp_file_path)
            
            # Проверяем результат
            self.assertEqual(result_hash, expected_hash)
            
        finally:
            # Удаляем временный файл
            os.unlink(temp_file_path)


def create_test_image_file():
    """
    Создает тестовый файл изображения для демонстрации.
    """
    # Простые данные PNG (1x1 пиксель, прозрачный)
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_file.write(png_data)
        return temp_file.name


def demo_sha1_calculation():
    """
    Демонстрация вычисления SHA1 хеша.
    """
    print("=== Демонстрация вычисления SHA1 хеша ===")
    
    # Создаем тестовый файл изображения
    test_image_path = create_test_image_file()
    
    try:
        # Вычисляем хеш
        sha1_hash = get_image_file_sha1_hash(test_image_path)
        
        print(f"Путь к файлу: {test_image_path}")
        print(f"SHA1 хеш: {sha1_hash}")
        
        # Проверяем размер файла
        file_size = os.path.getsize(test_image_path)
        print(f"Размер файла: {file_size} байт")
        
    finally:
        # Удаляем тестовый файл
        os.unlink(test_image_path)


if __name__ == "__main__":
    # Запуск демонстрации
    demo_sha1_calculation()
    
    print("\n" + "="*50)
    print("Запуск тестов...")
    
    # Запуск тестов
    unittest.main(verbosity=2)