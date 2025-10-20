# 🔍 Django ImageField SHA1 Hash Calculator

Полное решение для получения SHA1 хеша содержимого изображения из Django ImageField с автоматическим вычислением, поиском дубликатов и веб-интерфейсом.

## 🚀 Возможности

- **Автоматическое вычисление SHA1 хеша** при сохранении изображения
- **Ручное вычисление хеша** для существующих изображений
- **Поиск изображений по хешу**
- **Поиск дубликатов** изображений
- **Сравнение изображений** по хешам
- **Веб-интерфейс** для загрузки и управления изображениями
- **REST API** для программного доступа

## 📦 Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Создайте суперпользователя (опционально):
```bash
python manage.py createsuperuser
```

4. Запустите сервер разработки:
```bash
python manage.py runserver
```

5. Откройте браузер и перейдите по адресу: http://127.0.0.1:8000/

## 🔧 Использование

### Базовое использование

```python
from imagehash.models import ImageWithHash

# Создание изображения с автоматическим вычислением хеша
image_obj = ImageWithHash(
    name="Мое изображение",
    image=uploaded_file
)
image_obj.save()  # Хеш вычисляется автоматически

print(f"SHA1 хеш: {image_obj.image_hash}")
```

### Ручное вычисление хеша

```python
# Получение хеша существующего изображения
hash_value = image_obj.get_image_sha1_hash()
print(f"SHA1 хеш: {hash_value}")

# Обновление хеша в базе данных
image_obj.update_hash()
```

### Поиск по хешу

```python
# Поиск изображений по хешу
images = ImageWithHash.find_by_hash("abc123...")
for img in images:
    print(f"Найдено: {img.name}")
```

### Поиск дубликатов

```python
# Поиск дубликатов
duplicates = ImageWithHash.find_duplicates()
for hash_value, images in duplicates.items():
    print(f"Хеш {hash_value}: {images.count()} копий")
```

### Утилитарные функции

```python
from imagehash.models import ImageHashUtility

# Вычисление хеша Django файла
hash_value = ImageHashUtility.calculate_django_file_hash(image_field)

# Вычисление хеша файла по пути
hash_value = ImageHashUtility.calculate_file_hash("/path/to/image.jpg")

# Сравнение изображений
are_same = ImageHashUtility.compare_images_by_hash(image1, image2)
```

## 🌐 API Endpoints

### POST /api/upload/
Загрузка изображения и получение SHA1 хеша

**Параметры:**
- `image` (file) - файл изображения
- `name` (string, опционально) - название изображения

**Ответ:**
```json
{
    "success": true,
    "id": 1,
    "name": "Мое изображение",
    "image_url": "/media/images/image.jpg",
    "sha1_hash": "abc123...",
    "message": "Изображение успешно загружено и хеш вычислен"
}
```

### GET /api/hash/{image_id}/
Получение SHA1 хеша изображения по ID

**Ответ:**
```json
{
    "success": true,
    "id": 1,
    "name": "Мое изображение",
    "sha1_hash": "abc123...",
    "image_url": "/media/images/image.jpg"
}
```

### GET /api/search/?hash={hash}
Поиск изображений по SHA1 хешу

**Ответ:**
```json
{
    "success": true,
    "images": [
        {
            "id": 1,
            "name": "Мое изображение",
            "image_url": "/media/images/image.jpg",
            "sha1_hash": "abc123..."
        }
    ],
    "count": 1
}
```

### GET /api/duplicates/
Поиск дубликатов изображений

**Ответ:**
```json
{
    "success": true,
    "duplicates": [
        {
            "hash": "abc123...",
            "count": 2,
            "images": [
                {
                    "id": 1,
                    "name": "Изображение 1",
                    "image_url": "/media/images/image1.jpg"
                },
                {
                    "id": 2,
                    "name": "Изображение 2",
                    "image_url": "/media/images/image2.jpg"
                }
            ]
        }
    ],
    "total_duplicate_groups": 1
}
```

### POST /api/calculate-hash/
Быстрое вычисление хеша без сохранения

**Параметры:**
- `file` (file) - файл изображения

**Ответ:**
```json
{
    "success": true,
    "filename": "image.jpg",
    "size": 12345,
    "sha1_hash": "abc123..."
}
```

## 🧪 Тестирование

Запустите примеры использования:

```bash
python example_usage.py
```

## 📁 Структура проекта

```
imagehash/
├── models.py          # Модели Django с ImageField и хешированием
├── views.py           # API endpoints и веб-интерфейс
├── urls.py            # URL маршруты
├── admin.py           # Админ-панель Django
├── apps.py            # Конфигурация приложения
├── settings.py        # Настройки Django
├── manage.py          # Управление Django
├── requirements.txt   # Зависимости Python
├── example_usage.py   # Примеры использования
├── templates/
│   └── index.html     # Веб-интерфейс
└── README.md          # Документация
```

## 🔍 Как это работает

1. **Автоматическое вычисление**: При сохранении объекта `ImageWithHash` в методе `save()` автоматически вызывается `get_image_sha1_hash()`, который:
   - Открывает файл изображения в бинарном режиме
   - Читает все содержимое файла
   - Вычисляет SHA1 хеш с помощью `hashlib.sha1()`
   - Сохраняет хеш в поле `image_hash`

2. **Ручное вычисление**: Метод `get_image_sha1_hash()` можно вызвать в любое время для получения хеша существующего изображения

3. **Утилитарные функции**: Класс `ImageHashUtility` предоставляет статические методы для работы с хешами файлов

## ⚠️ Важные замечания

- Хеш вычисляется для **содержимого файла**, а не для пути или метаданных
- Одинаковые файлы всегда будут иметь одинаковый хеш, независимо от имени файла
- Хеш не изменяется при переименовании файла или изменении его атрибутов
- Для больших файлов процесс вычисления хеша может занять время

## 🛠️ Настройка

В `settings.py` можно настроить:

- `FILE_UPLOAD_MAX_MEMORY_SIZE` - максимальный размер файла в памяти
- `DATA_UPLOAD_MAX_MEMORY_SIZE` - максимальный размер данных для загрузки
- `MEDIA_ROOT` и `MEDIA_URL` - настройки для медиа файлов

## 📝 Лицензия

Этот проект создан в образовательных целях и может быть свободно использован и модифицирован.