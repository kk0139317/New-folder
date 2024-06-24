from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('createuser/', views.CreateUserView, name='createuser'),
    path('loginuser/', views.LoginUserView, name='loginuser'),
     path('check-auth/', views.check_auth_view, name='check-auth'),
]
