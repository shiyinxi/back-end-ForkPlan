import requests
from django.http import JsonResponse

def handle_api_request(url, params):
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json(), None
        else:
            error_message = f"Error: Received status code {response.status_code}"
            print(error_message)
            return None, error_message
    except requests.exceptions.RequestException as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        return None, error_message
    
def handle_exception(e):
    error_message = f"Error: {str(e)}"
    print(error_message)
    return JsonResponse({"error": error_message}, status=500)

def json_response(data, status=200):
    return JsonResponse(data, safe=False, status=status)