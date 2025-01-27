from django.db import models

# Create your models here.
class Ingredients(models.Model):
    IngredientId = models.IntegerField(primary_key=True)
    IngredientName = models.CharField(max_length=500)
    IngredientImage = models.CharField(max_length=500)