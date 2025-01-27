from rest_framework import serializers
from .models import ShoppingList
from Recipes.serializers import IngredientSerializer

class ShoppingListSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = ShoppingList
        fields = '__all__'