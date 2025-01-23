from django.db import models

# Create your models here.

class Recipes(models.Model):
    RecipeId = models.IntegerField(primary_key=True)
    RecipeName = models.CharField(max_length=500)
    RecipeImage = models.CharField(max_length=500)


class Ingredients(models.Model):
    IngredientId = models.IntegerField(primary_key=True)
    IngredientName = models.CharField(max_length=500)
    IngredientImage = models.CharField(max_length=500)
