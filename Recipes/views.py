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
import json

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
def search_ingredient_by_name(ingredient_name):
    url = f"https://api.spoonacular.com/food/ingredients/search"
    params = {
        "apiKey": os.getenv("SPOONACULAR_API_KEY"),
        "query": ingredient_name,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None, response.json().get('message', 'Error fetching ingredient')
    return response.json(), None

    
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
            data = json.loads(request.body)
          
            ingredients = data.get('ingredients', [])
            print(ingredients)
            for ingredient_data in ingredients:
                name = ingredient_data.get('ingredient')
                print(name)
                ingredient_data, error = search_ingredient_by_name(name)
                if error:
                    return json_response({"error": error}, status=500)
                print('ingredient_data:', json.dumps(ingredient_data, indent=2))
                if 'results' not in ingredient_data or not ingredient_data['results']:
                    return json_response({"error": "No results found for ingredient"}, status=404)
                ingredient = ingredient_data['results'][0]
                
                print('ingredient:',ingredient)
                ingredient_dict = {
                    'ingredient_id': ingredient['id'],
                    'name': name,
                    'image': f"https://img.spoonacular.com/ingredients_100x100/{ingredient['image']}",
                    'amount': 1,
                    'unit': ingredient.get('unit', ''),
                }
               
                ingredient_obj = Ingredient(**ingredient_dict)
                print("ingredient_obj:", ingredient_obj, type(ingredient_obj))

                for item in ShoppingList.objects.all():
                    if item.ingredient['ingredient_id'] == ingredient_dict['ingredient_id']:
                        shopping_list_item = item
                        break

                if shopping_list_item is None:
          
                    shopping_list_item = ShoppingList.objects.create(
                        ingredient=ingredient_dict,
                        quantity=ingredient_dict['amount']
                    )
                else:
                    # If the ingredient is already in the shopping list, increase the quantity
                    shopping_list_item.quantity += ingredient_dict['amount']
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