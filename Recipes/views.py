from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import HttpResponse
from django.http import JsonResponse
import requests
from dotenv import load_dotenv
import os
from ForkPlan.utils import handle_api_request, handle_exception, json_response

from Recipes.models import Recipes, Ingredient
from Inventory.models import Inventory
from ShoppingList.models import ShoppingList
from Recipes.serializers import RecipesSerializer

load_dotenv()
# Create your views here.
@csrf_exempt
def search_recipes(request):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": "pasta",
        "apiKey": os.getenv("SPOONACULAR_API_KEY"),
    }
    data, error = handle_api_request(url, params)
    if error:
        return json_response({"error": error}, status=500)
    return json_response(data)
    
@csrf_exempt
def get_recipe_by_id(request, recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": os.getenv("SPOONACULAR_API_KEY"),
    }
    data, error = handle_api_request(url, params)
    if error:
        return json_response({"error": error}, status=500)
    return json_response(data)
    
@csrf_exempt
def save_recipe(request):
    if request.method == "POST":
        try:
            recipe_data = JSONParser().parse(request)
            recipe, created = Recipes.objects.update_or_create(
                recipe_id=recipe_data['id'],
                defaults={
                    'title': recipe_data['title'],
                    'image': recipe_data['image'],
                    'instructions': recipe_data['instructions'],
                    'ingredients': []
                }
            )

            # Extract and save the ingredients data
            ingredients_data = recipe_data['extendedIngredients']
         
            for ingredient_data in ingredients_data:
                recipe.ingredients.append(
                    {'name': ingredient_data['name'],
                    'ingredient_id': ingredient_data['id'],
                    'image': ingredient_data.get('image', ""),
                    'amount': ingredient_data['amount'],
                    'unit': ingredient_data['unit']
                    }
                )
            recipe.save()
            return json_response({"message": "Recipe saved successfully"}, status=201)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)   

@csrf_exempt
def update_shopping_list(request, recipe_id):
    if request.method == "POST":
        try:
            recipe = Recipes.objects.get(recipe_id=recipe_id)
            for ingredient_data in recipe.ingredients:
                shopping_list_item, created = ShoppingList.objects.get_or_create(
                    ingredient=ingredient_data,
                    defaults={'quantity': ingredient_data['amount']}
                )
                if not created:
                    # If the ingredient is already in the shopping list, increase the quantity
                    shopping_list_item.quantity += ingredient_data.amount
                    shopping_list_item.save()
            
            return json_response({"message": "Shopping list updated successfully"}, status=200)
        except Recipes.DoesNotExist:
            return json_response({"error": "Recipe not found"}, status=404)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)

@csrf_exempt
def delete_recipe(request, recipe_id):
    if request.method == "DELETE":
        try:
            recipe = Recipes.objects.get(recipe_id=recipe_id)
            recipe.delete()
            return json_response({"message": "Recipe deleted successfully"})
        except Recipes.DoesNotExist:
            return json_response({"error": "Recipe not found"}, status=404)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)
    
@csrf_exempt
def get_all_recipes(request):
    if request.method == "GET":
        try:
            recipes = Recipes.objects.all()
            serializer = RecipesSerializer(recipes, many=True)
            return json_response(serializer.data)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)