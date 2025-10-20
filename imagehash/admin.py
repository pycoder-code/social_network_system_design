from django.contrib import admin
from .models import ImageWithHash


@admin.register(ImageWithHash)
class ImageWithHashAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'image_hash', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'image_hash']
    readonly_fields = ['image_hash', 'created_at', 'image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-width: 100px; max-height: 100px;">'
        return "Нет изображения"
    image_preview.allow_tags = True
    image_preview.short_description = "Превью"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()