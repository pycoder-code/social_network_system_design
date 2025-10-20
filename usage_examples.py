"""
Примеры использования функций для получения SHA1 хеша изображений в Django.
"""

# Импорты (предполагается, что Django настроен)
from models import ImageModel, get_image_field_sha1_hash, get_image_file_sha1_hash


def example_usage():
    """
    Примеры использования различных способов получения SHA1 хеша изображения.
    """
    
    # Пример 1: Использование метода модели
    print("=== Пример 1: Метод модели ===")
    
    # Получаем объект модели (предполагается, что он существует)
    try:
        image_obj = ImageModel.objects.first()
        if image_obj and image_obj.image:
            sha1_hash = image_obj.get_image_sha1_hash()
            print(f"SHA1 хеш изображения '{image_obj.name}': {sha1_hash}")
        else:
            print("Нет объектов с изображениями в базе данных")
    except Exception as e:
        print(f"Ошибка при получении объекта: {e}")
    
    
    # Пример 2: Использование альтернативного метода модели
    print("\n=== Пример 2: Альтернативный метод модели ===")
    
    try:
        image_obj = ImageModel.objects.first()
        if image_obj and image_obj.image:
            sha1_hash = image_obj.get_image_sha1_hash_alternative()
            print(f"SHA1 хеш (альтернативный способ): {sha1_hash}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    
    # Пример 3: Использование утилитарной функции
    print("\n=== Пример 3: Утилитарная функция ===")
    
    try:
        image_obj = ImageModel.objects.first()
        if image_obj and image_obj.image:
            sha1_hash = get_image_field_sha1_hash(image_obj.image)
            print(f"SHA1 хеш (утилитарная функция): {sha1_hash}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    
    # Пример 4: Использование функции для файла по пути
    print("\n=== Пример 4: Хеш файла по пути ===")
    
    # Пример с конкретным путем к файлу
    file_path = "/path/to/your/image.jpg"  # Замените на реальный путь
    sha1_hash = get_image_file_sha1_hash(file_path)
    if sha1_hash:
        print(f"SHA1 хеш файла '{file_path}': {sha1_hash}")
    else:
        print(f"Не удалось получить хеш для файла '{file_path}'")


def example_in_view():
    """
    Пример использования в Django view.
    """
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404
    
    def get_image_hash_view(request, image_id):
        """
        View для получения SHA1 хеша изображения по ID.
        """
        try:
            image_obj = get_object_or_404(ImageModel, id=image_id)
            
            if not image_obj.image:
                return JsonResponse({
                    'error': 'У объекта нет изображения'
                }, status=400)
            
            sha1_hash = image_obj.get_image_sha1_hash()
            
            if sha1_hash:
                return JsonResponse({
                    'id': image_obj.id,
                    'name': image_obj.name,
                    'sha1_hash': sha1_hash,
                    'image_url': image_obj.image.url
                })
            else:
                return JsonResponse({
                    'error': 'Не удалось вычислить хеш изображения'
                }, status=500)
                
        except Exception as e:
            return JsonResponse({
                'error': f'Ошибка: {str(e)}'
            }, status=500)


def example_in_serializer():
    """
    Пример использования в Django REST Framework serializer.
    """
    from rest_framework import serializers
    
    class ImageModelSerializer(serializers.ModelSerializer):
        sha1_hash = serializers.SerializerMethodField()
        
        class Meta:
            model = ImageModel
            fields = ['id', 'name', 'image', 'created_at', 'sha1_hash']
        
        def get_sha1_hash(self, obj):
            """
            Получить SHA1 хеш изображения для сериализатора.
            """
            if obj.image:
                return obj.get_image_sha1_hash()
            return None


def example_bulk_hash_calculation():
    """
    Пример массового вычисления хешей для всех изображений.
    """
    print("=== Массовое вычисление SHA1 хешей ===")
    
    try:
        images = ImageModel.objects.filter(image__isnull=False)
        
        for image_obj in images:
            sha1_hash = image_obj.get_image_sha1_hash()
            print(f"ID: {image_obj.id}, Название: {image_obj.name}, SHA1: {sha1_hash}")
            
    except Exception as e:
        print(f"Ошибка при массовом вычислении: {e}")


def example_compare_images():
    """
    Пример сравнения изображений по их SHA1 хешам.
    """
    print("=== Сравнение изображений по SHA1 хешам ===")
    
    try:
        images = ImageModel.objects.filter(image__isnull=False)[:2]
        
        if len(images) >= 2:
            hash1 = images[0].get_image_sha1_hash()
            hash2 = images[1].get_image_sha1_hash()
            
            print(f"Изображение 1 ({images[0].name}): {hash1}")
            print(f"Изображение 2 ({images[1].name}): {hash2}")
            
            if hash1 == hash2:
                print("Изображения идентичны!")
            else:
                print("Изображения различны.")
        else:
            print("Недостаточно изображений для сравнения")
            
    except Exception as e:
        print(f"Ошибка при сравнении: {e}")


if __name__ == "__main__":
    # Запуск примеров (требует настроенного Django окружения)
    example_usage()
    example_bulk_hash_calculation()
    example_compare_images()