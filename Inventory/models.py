from django.db import models
from Recipes.models import Ingredient
from djongo import models

# Create your models here.
class Inventory(models.Model):
    ingredient = models.EmbeddedField(
        model_container=Ingredient
    )
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return self.ingredient.name