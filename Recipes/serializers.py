from rest_framework import serializers
from Recipes.models import Recipes

class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recipes
        fields='__all__'
