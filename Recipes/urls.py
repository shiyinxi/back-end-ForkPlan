from django.urls import path
from . import views

urlpatterns=[
    path('recipes/', views.search_recipes, name='recipes'),
    path('recipes/<int:recipe_id>/', views.get_recipe_by_id, name='recipe_by_id'),
    path('recipes/save/', views.save_recipe, name='save_recipe'),
    path('recipes/delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('recipes/all/', views.get_all_recipes, name='all_recipes'),

]