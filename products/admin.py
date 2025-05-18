from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image_preview']  # görünür sütunlar
    search_fields = ['name', 'description']  # arama çubuğunda aranabilir alanlar
    list_filter = ['price']  # sağ taraftaki filtreler
    readonly_fields = ['image_preview']  # sadece önizleme için

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="object-fit:contain;" />'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'