from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_inventory, name='get_inventory'),
    path('add/', views.add_ingredient_to_inventory, name='add_to_inventory'),
    path('delete/<int:item_id>/', views.delete_inventory_item, name='delete_from_inventory'),
    path('increase/<int:item_id>/', views.increase_inventory_quantity, name='increase_inventory_quantity'),
    path('decrease/<int:item_id>/', views.decrease_inventory_quantity, name='decrease_inventory_quantity'),
]