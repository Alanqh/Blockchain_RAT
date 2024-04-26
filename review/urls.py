from django.urls import path, include
from review import views
urlpatterns = [
    path('', views.index, name='review_apply'),
    path('submit_result/<int:result_id>/', views.submit_result, name='submit_result'),
    path('review_deal/', views.review_deal, name='review_deal'),
    path('review_result_confirm/<int:result_id>/', views.review_result_confirm, name='review_result_confirm'),


]