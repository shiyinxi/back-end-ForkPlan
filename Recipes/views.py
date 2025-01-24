from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import HttpResponse
from django.http import JsonResponse
import requests
from dotenv import load_dotenv
import os

from Recipes.models import Recipes,Ingredients
from Recipes.serializers import RecipesSerializer,IngredientsSerializer

load_dotenv()
# Create your views here.
@csrf_exempt
def searchRecipes(request):

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