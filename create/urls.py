from django.urls import path
from . import views

urlpatterns = [
    # 其他URL模式...
    path('', views.create_research_result, name='create_research_result'),
    path('detail/<int:pk>/', views.research_result_detail, name='research_result_detail'),
    path('results_created_list/', views.results_created_list, name='results_created_list'),
    path('modify_result/<int:result_id>/', views.modify_result, name='modify_result'),

]