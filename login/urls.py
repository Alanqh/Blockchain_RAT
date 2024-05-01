# login/urls.py(新建的文件)
from django.urls import path, include
from login import views
urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('confirm/', views.user_confirm,name='confirm'),
    path('user_profile/',views.user_profile,name= 'user_profile'),

]
