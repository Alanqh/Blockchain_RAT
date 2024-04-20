from django.urls import path, include
from login import views

urlpatterns = [
    path('', views.index, name = 'index'),  # 空路由，即http://
    path('captcha/', include('captcha.urls')),
    path('create/', include('create.urls')),  # 包含create应用的URL配置
    path('login/', include('login.urls')),
    path('transact/', include('transact.urls')),

    # 包含login应用的URL配置
]

