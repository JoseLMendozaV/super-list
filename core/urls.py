from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-item/', views.add_item, name='add_item'),
    path('add-list/', views.add_list, name='add_list'), # Nueva ruta
]