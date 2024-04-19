# login/urls.py(新建的文件)
from django.urls import path, include
from login import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('confirm/', views.user_confirm,name='confirm'),

]
