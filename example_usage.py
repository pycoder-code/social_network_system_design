"""
Примеры использования функций для вычисления SHA1 хэша из Django ImageField.
"""

# ============================================================================
# ПРИМЕР 1: Простое использование в Django shell или view
# ============================================================================

"""
from image_sha1_hash import get_image_file_sha1
from myapp.models import Photo

# Получить объект с изображением
photo = Photo.objects.get(id=1)

# Вычислить SHA1 хэш
sha1_hash = get_image_file_sha1(photo.image)
print(f"SHA1: {sha1_hash}")
"""


# ============================================================================
# ПРИМЕР 2: Django модель с автоматическим вычислением SHA1 при сохранении
# ============================================================================

"""
# В models.py:

from django.db import models
from image_sha1_hash import get_image_file_sha1

class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/')
    image_sha1 = models.CharField(max_length=40, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Автоматически вычисляем SHA1 при сохранении
        if self.image:
            self.image_sha1 = get_image_file_sha1(self.image)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
"""


# ============================================================================
# ПРИМЕР 3: Использование в Django View
# ============================================================================

"""
# В views.py:

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from myapp.models import Photo
from image_sha1_hash import get_image_file_sha1

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    sha1_hash = get_image_file_sha1(photo.image)
    
    context = {
        'photo': photo,
        'sha1_hash': sha1_hash
    }
    return render(request, 'photo_detail.html', context)

def photo_hash_api(request, photo_id):
    '''API endpoint для получения SHA1 хэша изображения'''
    photo = get_object_or_404(Photo, id=photo_id)
    sha1_hash = get_image_file_sha1(photo.image)
    
    return JsonResponse({
        'photo_id': photo.id,
        'title': photo.title,
        'sha1_hash': sha1_hash
    })
"""


# ============================================================================
# ПРИМЕР 4: Проверка дубликатов изображений
# ============================================================================

"""
# В utils.py:

from django.db.models import Count
from myapp.models import Photo
from image_sha1_hash import get_image_file_sha1

def find_duplicate_images():
    '''Находит дубликаты изображений по SHA1 хэшу'''
    duplicates = {}
    
    for photo in Photo.objects.filter(image__isnull=False):
        sha1 = get_image_file_sha1(photo.image)
        if sha1:
            if sha1 in duplicates:
                duplicates[sha1].append(photo)
            else:
                duplicates[sha1] = [photo]
    
    # Возвращаем только хэши с дубликатами
    return {k: v for k, v in duplicates.items() if len(v) > 1}

def update_all_sha1_hashes():
    '''Обновляет SHA1 хэши для всех фотографий'''
    photos = Photo.objects.filter(image__isnull=False)
    updated = 0
    
    for photo in photos:
        sha1 = get_image_file_sha1(photo.image)
        if sha1:
            photo.image_sha1 = sha1
            photo.save(update_fields=['image_sha1'])
            updated += 1
    
    return updated
"""


# ============================================================================
# ПРИМЕР 5: Django Management Command
# ============================================================================

"""
# В management/commands/calculate_image_hashes.py:

from django.core.management.base import BaseCommand
from myapp.models import Photo
from image_sha1_hash import get_image_file_sha1

class Command(BaseCommand):
    help = 'Вычисляет SHA1 хэши для всех изображений'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезаписать существующие хэши',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        if force:
            photos = Photo.objects.filter(image__isnull=False)
        else:
            photos = Photo.objects.filter(image__isnull=False, image_sha1='')
        
        total = photos.count()
        updated = 0
        
        self.stdout.write(f'Обработка {total} изображений...')
        
        for photo in photos:
            sha1 = get_image_file_sha1(photo.image)
            if sha1:
                photo.image_sha1 = sha1
                photo.save(update_fields=['image_sha1'])
                updated += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Успешно обновлено {updated} хэшей')
        )

# Использование:
# python manage.py calculate_image_hashes
# python manage.py calculate_image_hashes --force
"""


# ============================================================================
# ПРИМЕР 6: Django REST Framework Serializer
# ============================================================================

"""
# В serializers.py:

from rest_framework import serializers
from myapp.models import Photo
from image_sha1_hash import get_image_file_sha1

class PhotoSerializer(serializers.ModelSerializer):
    image_sha1_hash = serializers.SerializerMethodField()
    
    class Meta:
        model = Photo
        fields = ['id', 'title', 'image', 'image_sha1_hash', 'created_at']
    
    def get_image_sha1_hash(self, obj):
        '''Вычисляет SHA1 хэш изображения для API'''
        if obj.image:
            return get_image_file_sha1(obj.image)
        return None
"""


# ============================================================================
# ПРИМЕР 7: Использование с Django Signals
# ============================================================================

"""
# В signals.py:

from django.db.models.signals import pre_save
from django.dispatch import receiver
from myapp.models import Photo
from image_sha1_hash import get_image_file_sha1

@receiver(pre_save, sender=Photo)
def calculate_image_sha1(sender, instance, **kwargs):
    '''Автоматически вычисляет SHA1 хэш при сохранении'''
    if instance.image:
        instance.image_sha1 = get_image_file_sha1(instance.image)

# Не забудьте импортировать signals в apps.py:
# В apps.py:
class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    
    def ready(self):
        import myapp.signals
"""


# ============================================================================
# ПРИМЕР 8: Асинхронное вычисление с Celery
# ============================================================================

"""
# В tasks.py:

from celery import shared_task
from myapp.models import Photo
from image_sha1_hash import get_image_file_sha1

@shared_task
def calculate_photo_sha1(photo_id):
    '''Celery задача для вычисления SHA1 хэша'''
    try:
        photo = Photo.objects.get(id=photo_id)
        sha1 = get_image_file_sha1(photo.image)
        if sha1:
            photo.image_sha1 = sha1
            photo.save(update_fields=['image_sha1'])
            return f'SHA1 для фото {photo_id}: {sha1}'
    except Photo.DoesNotExist:
        return f'Фото {photo_id} не найдено'

# Использование:
# from myapp.tasks import calculate_photo_sha1
# calculate_photo_sha1.delay(photo_id=1)
"""
