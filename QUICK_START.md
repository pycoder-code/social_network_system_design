# 🚀 Быстрый старт: SHA1 хеш из Django ImageField

## Основной код для получения SHA1 хеша

### 1. Модель с ImageField и автоматическим вычислением хеша

```python
import hashlib
from django.db import models

class ImageWithHash(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    image_hash = models.CharField(max_length=40, blank=True, null=True)
    
    def get_image_sha1_hash(self):
        """Получает SHA1 хеш содержимого изображения"""
        if not self.image:
            return None
            
        try:
            with self.image.open('rb') as image_file:
                file_content = image_file.read()
                return hashlib.sha1(file_content).hexdigest()
        except Exception as e:
            print(f"Ошибка при вычислении хеша: {e}")
            return None
    
    def save(self, *args, **kwargs):
        """Автоматическое вычисление хеша при сохранении"""
        if self.image:
            self.image_hash = self.get_image_sha1_hash()
        super().save(*args, **kwargs)
```

### 2. Использование

```python
# Создание изображения (хеш вычисляется автоматически)
image_obj = ImageWithHash(
    name="Мое изображение",
    image=uploaded_file
)
image_obj.save()
print(f"SHA1 хеш: {image_obj.image_hash}")

# Ручное получение хеша
hash_value = image_obj.get_image_sha1_hash()
print(f"SHA1 хеш: {hash_value}")
```

### 3. Утилитарные функции

```python
import hashlib

def calculate_django_file_hash(django_file):
    """Вычисляет SHA1 хеш Django файла"""
    if not django_file:
        return None
        
    try:
        with django_file.open('rb') as f:
            file_content = f.read()
            return hashlib.sha1(file_content).hexdigest()
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

# Использование
hash_value = calculate_django_file_hash(image_obj.image)
```

### 4. Поиск дубликатов

```python
# Поиск изображений по хешу
images = ImageWithHash.objects.filter(image_hash=target_hash)

# Поиск дубликатов
from django.db.models import Count

duplicate_hashes = ImageWithHash.objects.values('image_hash').annotate(
    count=Count('image_hash')
).filter(count__gt=1, image_hash__isnull=False)

for item in duplicate_hashes:
    hash_value = item['image_hash']
    duplicates = ImageWithHash.objects.filter(image_hash=hash_value)
    print(f"Хеш {hash_value}: {duplicates.count()} копий")
```

## 🎯 Ключевые принципы

1. **Хеш вычисляется для содержимого файла**, а не для имени или пути
2. **Одинаковые файлы всегда имеют одинаковый хеш**
3. **Разные файлы имеют разные хеши** (даже если отличаются на 1 байт)
4. **Хеш не зависит от имени файла** или его атрибутов

## 🔧 Запуск демонстрации

```bash
# Установка зависимостей
pip install Django Pillow

# Выполнение миграций
python manage.py makemigrations
python manage.py migrate

# Запуск демонстрации Django
python demo.py

# Запуск простого примера (без Django)
python simple_example.py
```

## 📁 Структура файлов

- `imagehash/models.py` - Модели Django с ImageField
- `imagehash/views.py` - API endpoints и веб-интерфейс
- `demo.py` - Полная демонстрация с Django
- `simple_example.py` - Простой пример без Django
- `templates/index.html` - Веб-интерфейс для загрузки изображений

## 🌐 API Endpoints

- `POST /api/upload/` - Загрузка изображения
- `GET /api/hash/{id}/` - Получение хеша по ID
- `GET /api/search/?hash={hash}` - Поиск по хешу
- `GET /api/duplicates/` - Поиск дубликатов
- `POST /api/calculate-hash/` - Быстрое вычисление хеша