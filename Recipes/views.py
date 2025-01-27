from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import HttpResponse
from django.http import JsonResponse
import requests
from dotenv import load_dotenv
import os

from Recipes.models import Recipes
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
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            receipes = response.json()
            return JsonResponse(receipes, safe=False)
        else:
            error_message = f"Error: Received status code {response.status_code}"
            print(error_message)
            return JsonResponse({"error": error_message}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        return JsonResponse({"error": error_message}, status=500)
    
@csrf_exempt
def get_recipe_by_id(request, recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": os.getenv("SPOONACULAR_API_KEY"),
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            recipe = response.json()
            return JsonResponse(recipe, safe=False)
        else:
            error_message = f"Error: Received status code {response.status_code}"
            print(error_message)
            return JsonResponse({"error": error_message}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        return JsonResponse({"error": error_message}, status=500)
    
@csrf_exempt
def save_recipe(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            serializer = RecipesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            return JsonResponse({"error": error_message}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

@csrf_exempt
def delete_recipe(request, recipe_id):
    if request.method == "DELETE":
        try:
            recipe = Recipes.objects.get(id=recipe_id)
            recipe.delete()
            return JsonResponse({"message": "Recipe deleted successfully"}, status=200)
        except Recipes.DoesNotExist:
            return JsonResponse({"error": "Recipe not found"}, status=404)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            return JsonResponse({"error": error_message}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    
@csrf_exempt
def get_all_recipes(request):
    if request.method == "GET":
        try:
            recipes = Recipes.objects.all()
            serializer = RecipesSerializer(recipes, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            return JsonResponse({"error": error_message}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)