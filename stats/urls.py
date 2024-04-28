# In urls.py
from django.urls import path
from . import views

# In urls.py
urlpatterns = [
    path('',views.index,name='stats_board'),
    # Other URL patterns...
    path('stats/total_research_results/', views.total_research_results, name='total_research_results'),
    path('stats/daily_research_output/', views.daily_research_output, name='daily_research_output'),
    path('stats/approval_rate/', views.approval_rate, name='approval_rate'),
    path('stats/research_type_ratio/', views.research_type_ratio, name='research_type_ratio'),
    path('stats/transaction_stats/', views.transaction_stats, name='transaction_stats'),
]