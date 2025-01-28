from django.contrib import admin
from .models import Recipes, Ingredient

# Register your models here.
admin.site.register(Recipes)
admin.site.register(Ingredient)