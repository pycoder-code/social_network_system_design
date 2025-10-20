# SHA1 хеш для Django ImageField

Этот проект содержит решения для получения SHA1 хеша содержимого файлов изображений из Django ImageField.

## Файлы проекта

- `models.py` - Полная Django модель с ImageField и методами для вычисления SHA1
- `sha1_utils.py` - Утилиты без зависимости от Django для вычисления SHA1
- `usage_examples.py` - Примеры использования в различных сценариях Django
- `test_sha1_hash.py` - Тесты для проверки функциональности

## Основные способы получения SHA1 хеша

### 1. Метод модели Django

```python
class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    
    def get_image_sha1_hash(self):
        """Получить SHA1 хеш содержимого изображения."""
        if not self.image:
            return None
            
        try:
            with self.image.open('rb') as image_file:
                sha1_hash = hashlib.sha1()
                for chunk in iter(lambda: image_file.read(4096), b""):
                    sha1_hash.update(chunk)
                return sha1_hash.hexdigest()
        except (IOError, OSError) as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

# Использование:
image_obj = ImageModel.objects.get(id=1)
sha1_hash = image_obj.get_image_sha1_hash()
```

### 2. Утилитарная функция для ImageField

```python
def get_image_field_sha1_hash(image_field):
    """Утилитарная функция для получения SHA1 хеша любого ImageField."""
    if not image_field:
        return None
        
    try:
        with image_field.open('rb') as image_file:
            sha1_hash = hashlib.sha1()
            for chunk in iter(lambda: image_file.read(4096), b""):
                sha1_hash.update(chunk)
            return sha1_hash.hexdigest()
    except (IOError, OSError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

# Использование:
sha1_hash = get_image_field_sha1_hash(some_model.image)
```

### 3. Функция для файла по пути

```python
def get_image_file_sha1_hash(file_path):
    """Получить SHA1 хеш файла по его пути."""
    try:
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'rb') as image_file:
            sha1_hash = hashlib.sha1()
            for chunk in iter(lambda: image_file.read(4096), b""):
                sha1_hash.update(chunk)
            return sha1_hash.hexdigest()
    except (IOError, OSError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

# Использование:
sha1_hash = get_image_file_sha1_hash('/path/to/image.jpg')
```

## Примеры использования

### В Django View

```python
def get_image_hash_view(request, image_id):
    image_obj = get_object_or_404(ImageModel, id=image_id)
    
    if not image_obj.image:
        return JsonResponse({'error': 'У объекта нет изображения'}, status=400)
    
    sha1_hash = image_obj.get_image_sha1_hash()
    
    return JsonResponse({
        'id': image_obj.id,
        'sha1_hash': sha1_hash,
        'image_url': image_obj.image.url
    })
```

### В Django REST Framework Serializer

```python
class ImageModelSerializer(serializers.ModelSerializer):
    sha1_hash = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageModel
        fields = ['id', 'name', 'image', 'sha1_hash']
    
    def get_sha1_hash(self, obj):
        if obj.image:
            return obj.get_image_sha1_hash()
        return None
```

### Массовое вычисление хешей

```python
def calculate_all_hashes():
    images = ImageModel.objects.filter(image__isnull=False)
    
    for image_obj in images:
        sha1_hash = image_obj.get_image_sha1_hash()
        print(f"ID: {image_obj.id}, SHA1: {sha1_hash}")
```

### Сравнение изображений

```python
def compare_images(image1, image2):
    hash1 = image1.get_image_sha1_hash()
    hash2 = image2.get_image_sha1_hash()
    
    return hash1 == hash2  # True если изображения идентичны
```

## Особенности реализации

1. **Эффективность памяти**: Файлы читаются блоками по 4096 байт, что позволяет обрабатывать большие изображения без загрузки всего файла в память.

2. **Обработка ошибок**: Все функции корректно обрабатывают ошибки ввода-вывода и возвращают `None` в случае проблем.

3. **Совместимость с Django Storage**: Используется `image_field.open()` для работы с различными storage backend'ами Django.

4. **Альтернативный метод**: Предоставлен альтернативный метод через `image.path` для случаев, когда нужен прямой доступ к файлу.

## Тестирование

Запустите тесты:

```bash
python3 sha1_utils.py  # Базовое тестирование без Django
python3 test_sha1_hash.py  # Полные тесты (требует Django)
```

## Требования

- Python 3.6+
- Django 2.0+ (для полной функциональности)
- Pillow (для работы с ImageField)

## Применение

Эти функции полезны для:
- Проверки дублирующихся изображений
- Верификации целостности файлов
- Кеширования на основе содержимого
- Создания уникальных идентификаторов изображений