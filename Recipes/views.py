from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import HttpResponse

from Recipes.models import Recipes,Ingredients
from Recipes.serializers import RecipesSerializer,IngredientsSerializer

# Create your views here.
@csrf_exempt
def searchRecipes(request):
    return HttpResponse("Hello World!")