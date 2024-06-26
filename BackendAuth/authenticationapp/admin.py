from django.contrib import admin
from .models import ImageGeneration, GeneratedImage
# Register your models here.

admin.site.register(ImageGeneration)
admin.site.register(GeneratedImage)
