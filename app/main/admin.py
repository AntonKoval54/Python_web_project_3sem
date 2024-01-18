from django.contrib import admin
from .models import SkillsContent
from .models import GeorgraphContent
from .models import VostrebContent
from .models import Image

@admin.register(SkillsContent)
class SkillsContentAdmin(admin.ModelAdmin):
    pass

@admin.register(GeorgraphContent)
class GeorgraphContentAdmin(admin.ModelAdmin):
    pass
@admin.register(VostrebContent)
class VostrebContentAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
# Register your models here.
