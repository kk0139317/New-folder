from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('createuser/', views.CreateUserView, name='createuser'),
    path('loginuser/', views.LoginUserView, name='loginuser'),
    path('check-auth/', views.check_auth_view, name='check-auth'),
    path('generate-images/', views.generate_images, name='generate-images'),
    path('prompts/<str:username>', views.get_user_prompts, name='get_user_prompts'),
    path('fetch-images/', views.fetch_images, name='fetch_images'),
]
