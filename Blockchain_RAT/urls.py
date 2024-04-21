from django.urls import path, include
from login import views

urlpatterns = [
    path('', views.index, name = 'index'),  # 空路由，即http://
    path('captcha/', include('captcha.urls')),
    path('create/', include('create.urls')),  # 包含create应用的URL配置
    path('login/', include('login.urls')),
    path('transact/', include('transact.urls')),
    path('review/', include('review.urls')),  # 包含review应用的URL配置

    # 包含login应用的URL配置
]

