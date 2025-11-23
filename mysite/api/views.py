import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# ロジックをインポート (ドット付きであることを確認！)
from .logic import PasswordGenerator

@csrf_exempt
def generate_password_api(request):
    if request.method == 'POST':
        try:
            # 1. Flutterからのデータを受け取る
            data = json.loads(request.body)
            keyword = data.get('keyword')
            key_list = data.get('key_list')

            # 2. 完成した最強ロジックを実行！
            generator = PasswordGenerator()
            password = generator.generate_password(keyword, key_list)
            
            # 3. 結果をJSONで返す
            return JsonResponse({'status': 'success', 'password': password})

        except Exception as e:
            # エラー内容を返す
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'POST request required'}, status=405)