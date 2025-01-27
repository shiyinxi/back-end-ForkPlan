from django.db import models
from Recipes.models import Ingredient

# Create your models here.
class Inventory(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return self.ingredient.name