
from djongo import models
from Recipes.models import Ingredient

class ShoppingList(models.Model):
    ingredient = models.EmbeddedField(
        model_container=Ingredient
    )
    quantity = models.IntegerField()

    def __str__(self):
        return self.ingredient.name