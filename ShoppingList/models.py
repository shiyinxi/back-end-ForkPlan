
from djongo import models
from Recipes.models import Ingredient

class ShoppingList(models.Model):
    ingredient = models.EmbeddedField(
        model_container=Ingredient
    )
    quantity = models.IntegerField()
