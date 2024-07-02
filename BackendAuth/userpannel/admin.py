from django.contrib import admin
from .models import UserImageGeneration, UserGeneratedImage, UserMasterPrompt, UserSubPrompt, ProfileDetail
# Register your models here.

admin.site.register(UserImageGeneration) # Register GeneratedImage model with Django admin dashboardImageGeneration)
admin.site.register(UserGeneratedImage)
admin.site.register(UserMasterPrompt)
admin.site.register(UserSubPrompt)
admin.site.register(ProfileDetail)