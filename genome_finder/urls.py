from django.urls import path
from . import views

urlpatterns = [
    path('align/', views.align, name='align'),
    path('get_jobs/', views.get_jobs, name='get_jobs'),
    path('get_job_status/', views.get_job_status, name='get_job_status')
]