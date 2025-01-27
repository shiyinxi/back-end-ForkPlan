from djongo import models

# Create your models here.


class Ingredient(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500)
    image = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Recipes(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    instructions = models.TextField(default="")
    ingredients = models.ArrayField(model_container=Ingredient)

    def __str__(self):
        return self.title

