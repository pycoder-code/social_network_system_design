#!/usr/bin/env python
"""
Примеры кода для получения SHA1 хеша содержимого изображения из Django ImageField
"""

import hashlib
from django.db import models
from django.core.files.base import ContentFile


# ============================================================================
# 1. МОДЕЛЬ С IMAGEFIELD И АВТОМАТИЧЕСКИМ ВЫЧИСЛЕНИЕМ ХЕША
# ============================================================================

class ImageWithHash(models.Model):
    """
    Модель с ImageField и функциональностью для получения SHA1 хеша
    """
    name = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(upload_to='images/', verbose_name="Изображение")
    image_hash = models.CharField(max_length=40, blank=True, null=True, verbose_name="SHA1 хеш")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    
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


# ============================================================================
# 2. УТИЛИТАРНЫЕ ФУНКЦИИ ДЛЯ РАБОТЫ С ХЕШАМИ
# ============================================================================

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


# ============================================================================
# 3. ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def example_basic_usage():
    """
    Базовый пример использования
    """
    print("=== Базовый пример использования ===")
    
    # Создаем тестовое изображение
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Создаем объект загруженного файла
    uploaded_file = ContentFile(test_image_data, name="test_image.png")
    
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
        images_with_same_hash = ImageWithHash.objects.filter(image_hash=original_image.image_hash)
        print(f"Найдено изображений с хешем {original_image.image_hash}: {images_with_same_hash.count()}")
        
        # Поиск дубликатов
        from django.db.models import Count
        duplicate_hashes = ImageWithHash.objects.values('image_hash').annotate(
            count=Count('image_hash')
        ).filter(count__gt=1, image_hash__isnull=False)
        
        print(f"Найдено групп дубликатов: {duplicate_hashes.count()}")
        for item in duplicate_hashes:
            hash_value = item['image_hash']
            duplicates = ImageWithHash.objects.filter(image_hash=hash_value)
            print(f"Хеш {hash_value}: {duplicates.count()} изображений")


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


# ============================================================================
# 4. ОСНОВНЫЕ ПРИНЦИПЫ
# ============================================================================

def print_principles():
    """
    Выводит основные принципы работы с хешами изображений
    """
    print("\n" + "="*60)
    print("📝 ОСНОВНЫЕ ПРИНЦИПЫ РАБОТЫ С SHA1 ХЕШАМИ ИЗОБРАЖЕНИЙ")
    print("="*60)
    print("1. Хеш вычисляется для СОДЕРЖИМОГО файла, а не для имени или пути")
    print("2. Одинаковые файлы ВСЕГДА имеют одинаковый хеш")
    print("3. Разные файлы имеют разные хеши (даже если отличаются на 1 байт)")
    print("4. Хеш НЕ зависит от имени файла или его атрибутов")
    print("5. Хеш НЕ изменяется при переименовании файла")
    print("6. Хеш можно использовать для поиска дубликатов")
    print("7. Хеш можно использовать для проверки целостности файла")
    print("\n🔧 ОСНОВНЫЕ МЕТОДЫ:")
    print("   - image_obj.get_image_sha1_hash() - получить хеш изображения")
    print("   - image_obj.image_hash - поле с хешем (заполняется автоматически)")
    print("   - ImageHashUtility.calculate_django_file_hash(file) - утилита")
    print("   - ImageHashUtility.calculate_file_hash(path) - по пути к файлу")
    print("="*60)


if __name__ == "__main__":
    print("🔍 Примеры получения SHA1 хеша из Django ImageField")
    print("="*60)
    
    try:
        # Запускаем примеры
        example_basic_usage()
        example_manual_hash_calculation()
        example_utility_functions()
        example_search_and_duplicates()
        example_file_path_hash()
        example_comparison()
        
        # Выводим принципы
        print_principles()
        
        print("\n✅ Все примеры выполнены успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении примеров: {e}")
        import traceback
        traceback.print_exc()