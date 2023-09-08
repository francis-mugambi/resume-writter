from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.templates, name='templates'),
    path('<str:str>/edit', views.template, name='template'),
]
