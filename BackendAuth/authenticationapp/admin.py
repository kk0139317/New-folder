from django.contrib import admin
from .models import ImageGeneration, GeneratedImage, MasterPrompt, SubPrompt
# Register your models here.

admin.site.register(ImageGeneration)
admin.site.register(GeneratedImage)
admin.site.register(MasterPrompt)
admin.site.register(SubPrompt)
