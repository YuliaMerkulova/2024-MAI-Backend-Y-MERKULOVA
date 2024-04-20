from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Заглушка для GET-запроса
@csrf_exempt
def api_get(request):
    data = {
        'message': 'This is a GET request!'
    }
    return JsonResponse(data)

# Заглушка для POST-запроса
@csrf_exempt
def api_post(request):
    if request.method == 'POST':
        # Получение данных из POST-запроса (пример)
        request_data = request.POST.get('data', '')
        data = {
            'message': 'This is a POST request!',
            'received_data': request_data
        }
        return JsonResponse(data)
    else:
        data = {
            'error': 'Only POST method is allowed for this endpoint.'
        }
        return JsonResponse(data, status=405)

# Заглушка для PUT-запроса
@csrf_exempt
def api_put(request):
    if request.method == 'PUT':
        # Получение данных из PUT-запроса (пример)
        request_data = request.body.decode('utf-8')
        data = {
            'message': 'This is a PUT request!',
            'received_data': request_data
        }
        return JsonResponse(data)
    else:
        data = {
            'error': 'Only PUT method is allowed for this endpoint.'
        }
        return JsonResponse(data, status=405)

# Заглушка для DELETE-запроса
@csrf_exempt
def api_delete(request):
    if request.method == 'DELETE':
        data = {
            'message': 'This is a DELETE request!'
        }
        return JsonResponse(data)
    else:
        data = {
            'error': 'Only DELETE method is allowed for this endpoint.'
        }
        return JsonResponse(data, status=405)
