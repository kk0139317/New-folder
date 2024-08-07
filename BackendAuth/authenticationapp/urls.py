from django.contrib import admin
from django.urls import path, include
from userpannel import views
from adminpannel import views as admin_views

urlpatterns = [
    path('createuser/', views.CreateUserView, name='createuser'),
    path('loginuser/', views.LoginUserView, name='loginuser'),
    path('check-auth/', views.check_auth_view, name='check-auth'),
    path('generate-images/', views.generate_images, name='generate-images'),
    path('prompts/<str:username>', views.get_user_prompts, name='get_user_prompts'),
    path('fetch-images/', views.fetch_images, name='fetch_images'),
    path('get_profile/<str:username>', views.get_profile, name='get_profile'),
    path('purchase-credit/', views.purchase_credit, name='purchase_credit'),
]
