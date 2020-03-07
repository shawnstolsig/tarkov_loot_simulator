from django.urls import path
from . import views

app_name = 'loot'
urlpatterns = [
    path('panel/', views.server_data_panel, name='panel'),
    path('load_containers/', views.load_containers, name='containers'),
    path('load_tables/', views.load_tables, name='tables'),
]
