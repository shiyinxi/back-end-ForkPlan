from django.shortcuts import render
from Inventory.models import Inventory
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Inventory.serializers import InventorySerializer
from ForkPlan.utils import handle_exception, json_response, handle_api_request
import requests
import os
from rest_framework.parsers import JSONParser

# Create your views here.
@csrf_exempt
def get_all_inventory(request):
    if request.method == "GET":
        try:
            inventory_items = Inventory.objects.all()
            serializer = InventorySerializer(inventory_items, many=True)
            return json_response(serializer.data)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)
    
@csrf_exempt
def delete_inventory_item(request, item_id):
    if request.method == "DELETE":
        try:
            # Find the inventory item by ingredient_id
            inventory_item = Inventory.objects.get(id=item_id)
            # Delete the inventory item
            inventory_item.delete()
            return json_response({"message": "Item deleted successfully"}, status=200)
        except Inventory.DoesNotExist:
            return json_response({"error": "Item not found"}, status=404)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)
    
@csrf_exempt
def add_ingredient_to_inventory(request):
    if request.method == "PUT":
        try:
            url = f"https://api.spoonacular.com/food/ingredients/search"
            params = {
                "apiKey": os.getenv("SPOONACULAR_API_KEY"),
                "query": "fish",
            }
            ingredient_data, error = handle_api_request(url, params)

            ingredient = {
                'ingredient_id': ingredient_data['results'][0]['id'],
                'name': ingredient_data['results'][0]['name'],
                'image': ingredient_data['results'][0].get('image', ''),
                'unit': ingredient_data['results'][0].get('unit',''),
                'amount': 0,
            }

            inventory_item = Inventory.objects.create(
                ingredient=ingredient,
                quantity=ingredient['amount']
            )

            serializer = InventorySerializer(inventory_item)
            return json_response(serializer.data, status=201)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)

@csrf_exempt
def increase_inventory_quantity(request, item_id):
    if request.method == "PUT":
        try:
            inventory_item = Inventory.objects.get(id=item_id)

            inventory_item.quantity += 1
            inventory_item.save()

            serializer = InventorySerializer(inventory_item)
            return json_response(serializer.data, status=200)
        except Inventory.DoesNotExist:
            return json_response({"error": "Item not found in inventory"}, status=404)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)
    
@csrf_exempt
def decrease_inventory_quantity(request, item_id):
    if request.method == "PUT":
        try:
            inventory_item = Inventory.objects.get(id=item_id)

            inventory_item.quantity -= 1
            if inventory_item.quantity < 0:
                inventory_item.quantity = 0
            inventory_item.save()

            serializer = InventorySerializer(inventory_item)
            return json_response(serializer.data, status=200)
        except Inventory.DoesNotExist:
            return json_response({"error": "Item not found in inventory"}, status=404)
        except Exception as e:
            return handle_exception(e)
    else:
        return json_response({"error": "Invalid HTTP method"}, status=405)