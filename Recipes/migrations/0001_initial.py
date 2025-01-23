# Generated by Django 3.1.12 on 2025-01-23 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('IngredientId', models.IntegerField(primary_key=True, serialize=False)),
                ('IngredientName', models.CharField(max_length=500)),
                ('IngredientImage', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('RecipeId', models.IntegerField(primary_key=True, serialize=False)),
                ('RecipeName', models.CharField(max_length=500)),
                ('RecipeImage', models.CharField(max_length=500)),
            ],
        ),
    ]
