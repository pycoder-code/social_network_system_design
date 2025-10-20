from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload/', views.upload_image, name='upload_image'),
    path('api/hash/<int:image_id>/', views.get_image_hash, name='get_image_hash'),
    path('api/duplicates/', views.find_duplicates, name='find_duplicates'),
    path('api/search/', views.search_by_hash, name='search_by_hash'),
    path('api/calculate-hash/', views.calculate_hash_from_file, name='calculate_hash_from_file'),
]