"""
Пример Django модели с ImageField и функцией для получения SHA1 хеша содержимого изображения.
"""
import hashlib
import os
from django.db import models
from django.core.files.storage import default_storage


class ImageModel(models.Model):
    """
    Модель с полем изображения.
    """
    name = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(upload_to='images/', verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
    
    def __str__(self):
        return self.name
    
    def get_image_sha1_hash(self):
        """
        Получить SHA1 хеш содержимого файла изображения.
        
        Returns:
            str: SHA1 хеш в шестнадцатеричном формате или None если файл не существует
        """
        if not self.image:
            return None
            
        try:
            # Открываем файл через Django storage
            with self.image.open('rb') as image_file:
                # Создаем объект SHA1
                sha1_hash = hashlib.sha1()
                
                # Читаем файл блоками для эффективности памяти
                for chunk in iter(lambda: image_file.read(4096), b""):
                    sha1_hash.update(chunk)
                
                # Возвращаем хеш в шестнадцатеричном формате
                return sha1_hash.hexdigest()
                
        except (IOError, OSError) as e:
            print(f"Ошибка при чтении файла: {e}")
            return None
    
    def get_image_sha1_hash_alternative(self):
        """
        Альтернативный способ получения SHA1 хеша через путь к файлу.
        
        Returns:
            str: SHA1 хеш в шестнадцатеричном формате или None если файл не существует
        """
        if not self.image:
            return None
            
        try:
            # Получаем полный путь к файлу
            file_path = self.image.path
            
            # Проверяем, существует ли файл
            if not os.path.exists(file_path):
                return None
            
            # Читаем файл и вычисляем хеш
            with open(file_path, 'rb') as image_file:
                sha1_hash = hashlib.sha1()
                
                # Читаем файл блоками
                for chunk in iter(lambda: image_file.read(4096), b""):
                    sha1_hash.update(chunk)
                
                return sha1_hash.hexdigest()
                
        except (IOError, OSError, AttributeError) as e:
            print(f"Ошибка при чтении файла: {e}")
            return None


def get_image_field_sha1_hash(image_field):
    """
    Утилитарная функция для получения SHA1 хеша любого ImageField.
    
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
            
            # Читаем файл блоками
            for chunk in iter(lambda: image_file.read(4096), b""):
                sha1_hash.update(chunk)
            
            return sha1_hash.hexdigest()
            
    except (IOError, OSError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return None