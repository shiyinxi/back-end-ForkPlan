from rest_framework import serializers
from Recipes.models import Recipes, Ingredients

class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recipes
        fields=('RecipeId','RecipeName','RecipeImage')

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ingredients
        fields=('IngredientId','IngredientName','IngredientImage')