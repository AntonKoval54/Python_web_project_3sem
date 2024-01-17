from django.contrib import admin
from .models import VostrebContent
from .models import Image
@admin.register(VostrebContent)
class VostrebContent(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
# Register your models here.
