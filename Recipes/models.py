from djongo import models

# Create your models here.


class Ingredient(models.Model):
   
    ingredient_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    unit = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)

    # def __str__(self):
    #     return self.name
    
    def to_dict(self):
        return {
            "ingredient_id": self.ingredient_id,
            "name": self.name,
            "image": self.image,
            "unit": self.unit,
            "amount": self.amount
        }

class Recipes(models.Model):

    recipe_id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    instructions = models.TextField(default="")
    ingredients = models.ArrayField(
        model_container=Ingredient,
        default=list,
)

    def __str__(self):
        return self.title

