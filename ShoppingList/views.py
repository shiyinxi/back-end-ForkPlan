from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ShoppingList
from .serializers import ShoppingListSerializer
from ForkPlan.utils import handle_exception, json_response
from Inventory.models import Inventory
from Inventory.serializers import InventorySerializer
from rest_framework.parsers import JSONParser
from Recipes.models import Ingredient
from django.shortcuts import get_object_or_404

@csrf_exempt
def get_shopping_list(request):
    if request.method == "GET":
        try:
            shopping_list_items = ShoppingList.objects.all()
            serializer = ShoppingListSerializer(shopping_list_items, many=True)
            return json_response(serializer.data)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)
    
@csrf_exempt
def add_item_to_inventory(request, item_id):
    if request.method == "PUT":
        try:
            shopping_list_item = ShoppingList.objects.get(id=item_id)
            ingredient = shopping_list_item.ingredient
            quantity = shopping_list_item.quantity

            inventory_item, created = Inventory.objects.get_or_create(ingredient=ingredient, defaults={'quantity': quantity})
            if not created:
                inventory_item.quantity += quantity
                inventory_item.save()
            shopping_list_item.delete()

            serializer = InventorySerializer(inventory_item)
            return json_response(serializer.data, status=201)
        except ShoppingList.DoesNotExist:
            return json_response({"error": "Ingredient not found in shopping list"}, status=404)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)

@csrf_exempt
def delete_item(request, item_id):
    if request.method == "DELETE":
        try:
            shopping_list_item = ShoppingList.objects.get(id=item_id)
            shopping_list_item.delete()
            return json_response({"message": "Item deleted successfully"}, status=200)
        except ShoppingList.DoesNotExist:
            return json_response({"error": "Item not found"}, status=404)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)