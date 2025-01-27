from rest_framework import serializers
from Recipes.models import Recipes, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ingredient
        fields=('__all__')

class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    class Meta:
        model=Recipes
        fields='__all__'


