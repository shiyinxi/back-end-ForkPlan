from rest_framework import serializers
from Recipes.models import Recipes, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ingredient
        fields= ['ingredient_id', 'name', 'image']

class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    class Meta:
        model=Recipes
        fields= ['recipe_id', 'title', 'image', 'instructions', 'ingredients']


    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            ingredient = Ingredient(**ingredient_data)
            recipe.ingredients.append(ingredient)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.save()

        instance.ingredients.clear()
        for ingredient_data in ingredients_data:
            ingredient = Ingredient(**ingredient_data)
            instance.ingredients.append(ingredient)
        instance.save()

        return instance