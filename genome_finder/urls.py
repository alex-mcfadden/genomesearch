from django.urls import path
from . import views

urlpatterns = [
    path('align/', views.align, name='align'),
]