# In urls.py
from django.urls import path
from . import views

# In urls.py
urlpatterns = [
    path('',views.get_stats,name='stats_board'),

]