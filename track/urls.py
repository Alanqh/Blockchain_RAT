from django.urls import path
from . import views

urlpatterns = [
    # 其他URL模式...
    path('', views.index, name='index'),
    path('start_tracking/<int:research_id>/', views.start_tracking, name='start_tracking'),
    path('stop_tracking/<int:research_id>/', views.stop_tracking, name='stop_tracking'),
    path('track_list/', views.my_tracked_research, name='track_list'),
    path('track_details/<int:research_id>/', views.track_details, name='track_details'),
]