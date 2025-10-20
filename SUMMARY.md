# 📋 Итоговое решение: SHA1 хеш из Django ImageField

## 🎯 Что реализовано

### 1. **Модель Django с ImageField и автоматическим вычислением хеша**
- `ImageWithHash` - модель с полями `name`, `image`, `image_hash`
- Автоматическое вычисление SHA1 хеша при сохранении
- Метод `get_image_sha1_hash()` для ручного получения хеша
- Метод `update_hash()` для обновления хеша

### 2. **Утилитарные функции**
- `ImageHashUtility.calculate_django_file_hash()` - для Django файлов
- `ImageHashUtility.calculate_file_hash()` - для файлов по пути
- `ImageHashUtility.compare_images_by_hash()` - для сравнения изображений

### 3. **Функции поиска и анализа**
- Поиск изображений по хешу: `ImageWithHash.find_by_hash()`
- Поиск дубликатов: `ImageWithHash.find_duplicates()`
- Сравнение изображений по хешам

### 4. **Веб-интерфейс и API**
- HTML интерфейс для загрузки изображений
- REST API endpoints для всех операций
- Поиск дубликатов через веб-интерфейс
- Быстрое вычисление хеша без сохранения

### 5. **Примеры использования**
- `demo.py` - полная демонстрация с Django
- `simple_example.py` - простой пример без Django
- `django_imagefield_sha1_examples.py` - все примеры кода

## 🚀 Быстрый старт

```python
# 1. Создание модели
class ImageWithHash(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    image_hash = models.CharField(max_length=40, blank=True, null=True)
    
    def get_image_sha1_hash(self):
        if not self.image:
            return None
        with self.image.open('rb') as f:
            return hashlib.sha1(f.read()).hexdigest()
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image_hash = self.get_image_sha1_hash()
        super().save(*args, **kwargs)

# 2. Использование
image_obj = ImageWithHash(name="Тест", image=uploaded_file)
image_obj.save()  # Хеш вычисляется автоматически
print(f"SHA1: {image_obj.image_hash}")

# 3. Ручное получение хеша
hash_value = image_obj.get_image_sha1_hash()
```

## 🔧 Запуск

```bash
# Установка
pip install Django Pillow

# Миграции
python manage.py makemigrations
python manage.py migrate

# Демонстрация
python demo.py
```

## 📁 Файлы проекта

- `imagehash/models.py` - Модели Django
- `imagehash/views.py` - API и веб-интерфейс
- `imagehash/urls.py` - URL маршруты
- `demo.py` - Демонстрация с Django
- `simple_example.py` - Простой пример
- `django_imagefield_sha1_examples.py` - Все примеры кода
- `templates/index.html` - Веб-интерфейс

## 🌐 API Endpoints

- `POST /api/upload/` - Загрузка изображения
- `GET /api/hash/{id}/` - Получение хеша по ID
- `GET /api/search/?hash={hash}` - Поиск по хешу
- `GET /api/duplicates/` - Поиск дубликатов
- `POST /api/calculate-hash/` - Быстрое вычисление хеша

## ✅ Ключевые особенности

1. **Автоматическое вычисление** хеша при сохранении
2. **Поиск дубликатов** по хешам
3. **Веб-интерфейс** для управления
4. **REST API** для программного доступа
5. **Утилитарные функции** для различных случаев
6. **Полная документация** и примеры

## 🎯 Результат

Получено полное решение для работы с SHA1 хешами изображений в Django, включающее:
- Модели с автоматическим вычислением хеша
- API для всех операций
- Веб-интерфейс для тестирования
- Примеры использования
- Документацию

Все готово к использованию! 🚀