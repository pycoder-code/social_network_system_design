"""
Модуль для вычисления SHA1 хэша содержимого файла изображения из Django ImageField.
"""
import hashlib
from typing import Optional


def get_image_file_sha1(image_field) -> Optional[str]:
    """
    Вычисляет SHA1 хэш содержимого файла изображения из Django ImageField.
    
    Args:
        image_field: Django ImageField объект (например, model_instance.image)
        
    Returns:
        str: SHA1 хэш в шестнадцатеричном формате или None, если файл не существует
        
    Example:
        >>> from myapp.models import MyModel
        >>> instance = MyModel.objects.get(id=1)
        >>> sha1_hash = get_image_file_sha1(instance.image)
        >>> print(sha1_hash)
        'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'
    """
    if not image_field:
        return None
    
    try:
        # Открываем файл и вычисляем SHA1 хэш
        sha1 = hashlib.sha1()
        
        # Открываем файл в бинарном режиме
        image_field.open('rb')
        
        # Читаем файл по частям для эффективной работы с большими файлами
        for chunk in image_field.chunks(chunk_size=8192):
            sha1.update(chunk)
        
        # Закрываем файл
        image_field.close()
        
        # Возвращаем хэш в шестнадцатеричном формате
        return sha1.hexdigest()
    
    except Exception as e:
        print(f"Ошибка при вычислении SHA1: {e}")
        return None


def get_image_file_sha1_alternative(image_field) -> Optional[str]:
    """
    Альтернативный метод вычисления SHA1 хэша через прямое чтение файла.
    Полезен, если метод chunks() недоступен.
    
    Args:
        image_field: Django ImageField объект
        
    Returns:
        str: SHA1 хэш в шестнадцатеричном формате или None
    """
    if not image_field:
        return None
    
    try:
        sha1 = hashlib.sha1()
        
        # Используем path для прямого доступа к файлу
        with open(image_field.path, 'rb') as f:
            while True:
                data = f.read(8192)
                if not data:
                    break
                sha1.update(data)
        
        return sha1.hexdigest()
    
    except Exception as e:
        print(f"Ошибка при вычислении SHA1: {e}")
        return None


def add_sha1_to_model_method(model_class):
    """
    Декоратор или функция для добавления метода get_image_sha1 в модель Django.
    
    Пример использования в models.py:
    
    class MyModel(models.Model):
        image = models.ImageField(upload_to='images/')
        
        def get_image_sha1(self):
            '''Возвращает SHA1 хэш файла изображения'''
            return get_image_file_sha1(self.image)
    """
    pass


# Пример использования в Django модели
"""
# В models.py:

from django.db import models
from image_sha1_hash import get_image_file_sha1

class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/')
    image_sha1 = models.CharField(max_length=40, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        # Автоматически вычисляем SHA1 при сохранении
        if self.image:
            self.image_sha1 = get_image_file_sha1(self.image)
        super().save(*args, **kwargs)
    
    def get_image_hash(self):
        '''Метод для получения SHA1 хэша изображения'''
        return get_image_file_sha1(self.image)


# В views.py или в Django shell:

from myapp.models import Photo

# Получить SHA1 хэш существующего изображения
photo = Photo.objects.get(id=1)
sha1_hash = photo.get_image_hash()
print(f"SHA1 хэш изображения: {sha1_hash}")

# Или напрямую:
from image_sha1_hash import get_image_file_sha1
sha1_hash = get_image_file_sha1(photo.image)
print(f"SHA1 хэш: {sha1_hash}")
"""
