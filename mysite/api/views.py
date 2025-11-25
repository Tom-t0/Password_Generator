import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .logic import PasswordGenerator

@csrf_exempt
def generate_password_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            keyword = data.get('keyword')
            key_list = data.get('key_list')
            allowed_symbols = data.get('allowed_symbols', "")
            generator = PasswordGenerator()
            password = generator.generate_password(keyword, key_list, allowed_symbols)
            return JsonResponse({'status': 'success', 'password': password})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST request required'}, status=405)