# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ...其他URL模式...
    path('download_file/<int:file_id>/', views.download_file, name='download_file'),
    # ...其他URL模式...
]