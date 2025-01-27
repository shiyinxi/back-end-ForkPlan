from django.urls import path
from . import views

urlpatterns=[
    path('', views.get_shopping_list, name='shopping_list'),
    path('inventory/<int:item_id>/', views.add_item_to_inventory, name='add_item_to_inventory'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('add/', views.add_item, name='add_item'),

]