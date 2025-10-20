# Вычисление SHA1 хэша из Django ImageField

Этот репозиторий содержит готовые решения для вычисления SHA1 хэша содержимого файлов изображений из Django ImageField.

## Файлы

- **`image_sha1_hash.py`** - основной модуль с функциями для вычисления SHA1 хэша
- **`example_usage.py`** - примеры использования в различных сценариях Django

## Основные функции

### `get_image_file_sha1(image_field)`

Вычисляет SHA1 хэш содержимого файла изображения из Django ImageField.

```python
from image_sha1_hash import get_image_file_sha1
from myapp.models import Photo

photo = Photo.objects.get(id=1)
sha1_hash = get_image_file_sha1(photo.image)
print(sha1_hash)  # Выведет: 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'
```

### `get_image_file_sha1_alternative(image_field)`

Альтернативный метод через прямое чтение файла (полезен, если метод `chunks()` недоступен).

## Быстрый старт

1. Скопируйте `image_sha1_hash.py` в ваш Django проект
2. Импортируйте функцию в нужном месте:

```python
from image_sha1_hash import get_image_file_sha1
```

3. Используйте с вашими моделями, которые содержат ImageField

## Примеры использования

### 1. Автоматическое вычисление при сохранении модели

```python
from django.db import models
from image_sha1_hash import get_image_file_sha1

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    image_sha1 = models.CharField(max_length=40, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image_sha1 = get_image_file_sha1(self.image)
        super().save(*args, **kwargs)
```

### 2. Использование в Django View

```python
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def photo_hash_api(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    sha1_hash = get_image_file_sha1(photo.image)
    
    return JsonResponse({
        'photo_id': photo.id,
        'sha1_hash': sha1_hash
    })
```

### 3. Поиск дубликатов изображений

```python
def find_duplicate_images():
    duplicates = {}
    for photo in Photo.objects.filter(image__isnull=False):
        sha1 = get_image_file_sha1(photo.image)
        if sha1 in duplicates:
            duplicates[sha1].append(photo)
        else:
            duplicates[sha1] = [photo]
    return {k: v for k, v in duplicates.items() if len(v) > 1}
```

Больше примеров смотрите в файле `example_usage.py`.

## Особенности

- ✅ Эффективная работа с большими файлами (чтение по частям)
- ✅ Обработка исключений
- ✅ Два варианта реализации (через chunks() и через прямое чтение)
- ✅ Совместимость с Django ImageField и FileField
- ✅ Примеры для различных сценариев (Views, Signals, Celery, DRF)

## Требования

- Python 3.6+
- Django 2.0+

## Лицензия

MIT
