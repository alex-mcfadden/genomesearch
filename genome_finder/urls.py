from django.urls import path
from . import views

urlpatterns = [
    path('align/', views.align_view, name='align'),
    path('get_jobs/', views.get_jobs_view, name='get_jobs'),
    path('get_job_status/', views.get_job_status_view, name='get_job_status')
]