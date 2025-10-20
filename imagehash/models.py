import hashlib
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class ImageWithHash(models.Model):
    """
    Модель с ImageField и функциональностью для получения SHA1 хеша
    """
    name = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(upload_to='images/', verbose_name="Изображение")
    image_hash = models.CharField(max_length=40, blank=True, null=True, verbose_name="SHA1 хеш")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    
    class Meta:
        verbose_name = "Изображение с хешем"
        verbose_name_plural = "Изображения с хешами"
    
    def __str__(self):
        return f"{self.name} - {self.image_hash or 'Нет хеша'}"
    
    def get_image_sha1_hash(self):
        """
        Получает SHA1 хеш содержимого изображения
        
        Returns:
            str: SHA1 хеш в шестнадцатеричном формате или None если файл не найден
        """
        if not self.image:
            return None
            
        try:
            # Открываем файл изображения
            with self.image.open('rb') as image_file:
                # Читаем содержимое файла
                file_content = image_file.read()
                
                # Вычисляем SHA1 хеш
                sha1_hash = hashlib.sha1(file_content).hexdigest()
                
                return sha1_hash
                
        except Exception as e:
            print(f"Ошибка при вычислении хеша: {e}")
            return None
    
    def save(self, *args, **kwargs):
        """
        Переопределяем метод save для автоматического вычисления хеша
        """
        # Вычисляем хеш перед сохранением
        if self.image:
            self.image_hash = self.get_image_sha1_hash()
        
        super().save(*args, **kwargs)
    
    def update_hash(self):
        """
        Обновляет хеш изображения (полезно если файл был изменен)
        """
        self.image_hash = self.get_image_sha1_hash()
        self.save(update_fields=['image_hash'])
    
    @classmethod
    def find_by_hash(cls, target_hash):
        """
        Находит изображение по SHA1 хешу
        
        Args:
            target_hash (str): SHA1 хеш для поиска
            
        Returns:
            QuerySet: Найденные изображения
        """
        return cls.objects.filter(image_hash=target_hash)
    
    @classmethod
    def find_duplicates(cls):
        """
        Находит дубликаты изображений по хешу
        
        Returns:
            dict: Словарь где ключ - хеш, значение - список объектов
        """
        from django.db.models import Count
        
        # Находим хеши, которые встречаются больше одного раза
        duplicate_hashes = cls.objects.values('image_hash').annotate(
            count=Count('image_hash')
        ).filter(count__gt=1, image_hash__isnull=False)
        
        duplicates = {}
        for item in duplicate_hashes:
            hash_value = item['image_hash']
            duplicates[hash_value] = cls.objects.filter(image_hash=hash_value)
        
        return duplicates


class ImageHashUtility:
    """
    Утилитарный класс для работы с хешами изображений
    """
    
    @staticmethod
    def calculate_file_hash(file_path):
        """
        Вычисляет SHA1 хеш файла по пути
        
        Args:
            file_path (str): Путь к файлу
            
        Returns:
            str: SHA1 хеш или None при ошибке
        """
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
                return hashlib.sha1(file_content).hexdigest()
        except Exception as e:
            print(f"Ошибка при вычислении хеша файла {file_path}: {e}")
            return None
    
    @staticmethod
    def calculate_django_file_hash(django_file):
        """
        Вычисляет SHA1 хеш Django файла (FileField/ImageField)
        
        Args:
            django_file: Объект Django файла
            
        Returns:
            str: SHA1 хеш или None при ошибке
        """
        if not django_file:
            return None
            
        try:
            with django_file.open('rb') as f:
                file_content = f.read()
                return hashlib.sha1(file_content).hexdigest()
        except Exception as e:
            print(f"Ошибка при вычислении хеша Django файла: {e}")
            return None
    
    @staticmethod
    def compare_images_by_hash(image1, image2):
        """
        Сравнивает два изображения по их хешам
        
        Args:
            image1: Первое изображение (ImageWithHash объект)
            image2: Второе изображение (ImageWithHash объект)
            
        Returns:
            bool: True если изображения одинаковые, False если разные
        """
        if not image1.image_hash or not image2.image_hash:
            return False
        
        return image1.image_hash == image2.image_hash