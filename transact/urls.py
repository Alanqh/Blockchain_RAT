# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='transact_results_display'),
    # ...其他URL模式...
    path('download_file/<int:file_id>/', views.download_file, name='download_file'),
    path('submit_result/<int:result_id>/', views.submit_result, name='submit_result'),
    path('transact_deal/',views.transact_deal,name='transact_deal'),
    path('transact_confirm/<int:result_id>/', views.transact_confirm, name='transact_confirm'),
    path('transact_records/',views.transact_records,name='transact_records'),
    path('bought_results/',views.bought_results,name='bought_results'),
    path('second_transact/<int:result_id>/',views.second_transact,name='transact_second'),

    # ...其他URL模式...
]