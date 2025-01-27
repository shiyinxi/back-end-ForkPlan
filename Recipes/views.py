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
            data = JSONParser().parse(request)
            serializer = RecipesSerializer(data=data)
            if serializer.is_valid():
                recipe = serializer.save()
                update_shopping_list(recipe)
                return json_response(serializer.data, status=201)
            return json_response(serializer.errors, status=400)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)

def update_shopping_list(recipe):
    for ingredient_data in recipe.ingredients:
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_data['name'], defaults={'quantity': ingredient_data['quantity']})
        if not Inventory.objects.filter(ingredient=ingredient).exists() and not ShoppingList.objects.filter(ingredient=ingredient).exists():
            ShoppingList.objects.create(ingredient=ingredient, quantity=ingredient_data['quantity'])

@csrf_exempt
def delete_recipe(request, recipe_id):
    if request.method == "DELETE":
        try:
            recipe = Recipes.objects.get(id=recipe_id)
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