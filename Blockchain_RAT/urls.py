from django.urls import path, include
from login import views

urlpatterns = [
    path('captcha/', include('captcha.urls')),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]
