from django.db import models

# Create your models here.

class Recipes(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    instructions = models.TextField(default="")
    ingredients = models.TextField(default="")

    def __str__(self):
        return self.title

