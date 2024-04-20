from django.urls import path
from . import views

urlpatterns = [
    # 其他URL模式...
    path('', views.create_research_result, name='create_research_result'),
    path('detail/<int:pk>/', views.research_result_detail, name='research_result_detail'),

]