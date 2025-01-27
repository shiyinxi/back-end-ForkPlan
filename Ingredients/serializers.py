from rest_framework import serializers
from Ingredients.models import Ingredients

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ingredients
        fields=('IngredientId','IngredientName','IngredientImage')