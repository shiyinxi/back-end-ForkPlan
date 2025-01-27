
from djongo import models
from Recipes.models import Ingredient

class ShoppingList(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return self.ingredient.name