from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
from .models import ImageWithHash, ImageHashUtility


def index(request):
    """
    Главная страница с формой загрузки изображения
    """
    images = ImageWithHash.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'images': images})


@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request):
    """
    API endpoint для загрузки изображения и получения его SHA1 хеша
    """
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'Файл изображения не найден'}, status=400)
        
        image_file = request.FILES['image']
        name = request.POST.get('name', image_file.name)
        
        # Создаем объект изображения
        image_obj = ImageWithHash(name=name, image=image_file)
        image_obj.save()  # Хеш будет вычислен автоматически в методе save()
        
        return JsonResponse({
            'success': True,
            'id': image_obj.id,
            'name': image_obj.name,
            'image_url': image_obj.image.url,
            'sha1_hash': image_obj.image_hash,
            'message': 'Изображение успешно загружено и хеш вычислен'
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Ошибка при загрузке: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def get_image_hash(request, image_id):
    """
    API endpoint для получения SHA1 хеша изображения по ID
    """
    try:
        image_obj = get_object_or_404(ImageWithHash, id=image_id)
        
        # Если хеш еще не вычислен, вычисляем его
        if not image_obj.image_hash:
            image_obj.update_hash()
        
        return JsonResponse({
            'success': True,
            'id': image_obj.id,
            'name': image_obj.name,
            'sha1_hash': image_obj.image_hash,
            'image_url': image_obj.image.url
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Ошибка при получении хеша: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def find_duplicates(request):
    """
    API endpoint для поиска дубликатов изображений
    """
    try:
        duplicates = ImageWithHash.find_duplicates()
        
        result = []
        for hash_value, images in duplicates.items():
            result.append({
                'hash': hash_value,
                'count': images.count(),
                'images': [
                    {
                        'id': img.id,
                        'name': img.name,
                        'image_url': img.image.url
                    } for img in images
                ]
            })
        
        return JsonResponse({
            'success': True,
            'duplicates': result,
            'total_duplicate_groups': len(result)
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Ошибка при поиске дубликатов: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def search_by_hash(request):
    """
    API endpoint для поиска изображений по хешу
    """
    try:
        target_hash = request.GET.get('hash')
        if not target_hash:
            return JsonResponse({'error': 'Параметр hash обязателен'}, status=400)
        
        images = ImageWithHash.find_by_hash(target_hash)
        
        result = []
        for img in images:
            result.append({
                'id': img.id,
                'name': img.name,
                'image_url': img.image.url,
                'sha1_hash': img.image_hash
            })
        
        return JsonResponse({
            'success': True,
            'images': result,
            'count': len(result)
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Ошибка при поиске: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def calculate_hash_from_file(request):
    """
    API endpoint для вычисления хеша из загруженного файла без сохранения
    """
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'Файл не найден'}, status=400)
        
        file_obj = request.FILES['file']
        hash_value = ImageHashUtility.calculate_django_file_hash(file_obj)
        
        if hash_value:
            return JsonResponse({
                'success': True,
                'filename': file_obj.name,
                'size': file_obj.size,
                'sha1_hash': hash_value
            })
        else:
            return JsonResponse({'error': 'Не удалось вычислить хеш'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': f'Ошибка при вычислении хеша: {str(e)}'}, status=500)