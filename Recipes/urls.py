from django.urls import path
from . import views

urlpatterns=[
    path('', views.search_recipes, name='recipes'),
    path('<int:recipe_id>/', views.get_recipe_by_id, name='recipe_by_id'),
    path('save/', views.save_recipe, name='save_recipe'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('all/', views.get_all_recipes, name='all_recipes'),
    path('shoppinglist/<int:item_id>', views.update_shopping_list, name='update_shopping_list')

]