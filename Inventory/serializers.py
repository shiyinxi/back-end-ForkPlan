from rest_framework import serializers
from .models import Inventory
from Recipes.serializers import IngredientSerializer

class InventorySerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = Inventory
        fields = '__all__'