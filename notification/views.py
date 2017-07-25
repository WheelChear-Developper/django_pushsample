from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .form import CertFileUploadForm
from .models import DeviceToken
from .utils import send_notification, upload_certificate

import django.utils.timezone as timezone
import json

# 端末のDeviceTokenの登録更新
@csrf_exempt
def device_token_post(request):

    # API許可確キー
    apikey = 'ABCDEF123456'

    # post以外は、使えないようにする
    if request.method != 'POST':
        return HttpResponse(status=405)

    # パラメータチェック
    if apikey == request.POST.get("apikey"):
        if "device_token" in request.POST:
            if "device_type" in request.POST:
                if request.POST.get("device_type") == 'iOS':
                    # query_paramが指定されている場合の処理
                    device_token = request.POST.get("device_token")
                    device_type = request.POST.get("device_type")
                    print("\033[94m", "POST device_token = ", device_token, " device_type = ", device_type, "\033[0m")
                else:
                    if request.POST.get("device_type") == 'Android':
                        # query_paramが指定されている場合の処理
                        device_token = request.POST.get("device_token")
                        device_type = request.POST.get("device_type")
                        print("\033[94m", "POST device_token = ", device_token, " device_type = ", device_type, "\033[0m")
                    else:
                        # query_paramが指定されていない場合の処理
                        return JsonResponse({'error': 'Not device_type'}, status=400)
            else:
                # query_paramが指定されていない場合の処理
                return JsonResponse({'error': 'Not device_type'}, status=400)
        else:
            # query_paramが指定されていない場合の処理
            return JsonResponse({'error': 'Not device_token'}, status=400)
    else:
        # query_paramが指定されていない場合の処理
        return JsonResponse({'error': 'Not apikey'}, status=400)

    # 既存Devicetokenチェック
    token_check = False
    for token in DeviceToken.objects.all().order_by('id'):
        if token.device_token == device_token:
            token_check = True
            break

    if DeviceToken.objects.filter(device_token=device_token).count() != 0:
        token = DeviceToken.objects.get(device_token=device_token)
        token.device_type = device_type
        token.updatetime = timezone.now()
        token.save()
    else:
        token = DeviceToken()
        token.device_token = device_token
        token.device_type = device_type
        token.setdatetime = token.updatetime
        token.save()

    print("\033[94m", "SAVE user = ", token.user, ",device_token = ", token.device_token, "\033[0m")

    return JsonResponse({'result': 'success'}, status=200)


def send_notification_with_device_token(request, mode, device_token, execute=True):
    # mode: 0 or 1
    # 0: develop target
    # 1: product target

    if request.user is None or not request.user.is_superuser:
        return HttpResponse('Please login for admin user.', status=401)

    if int(mode) > 1:
        return HttpResponse('check your mode number(0 or 1).', status=400)

    message = 'This is test push notification.'
    if 'message' in request.GET:
        message = request.GET['message']

    try:
        device_token = DeviceToken.objects.get(device_token=device_token)
        if not execute:
            return HttpResponse('End process.', status=200)

        send_notification(message=message,
                          device_token=device_token.device_token,
                          use_sandbox=True if int(mode) == 0 else False)
        return HttpResponse('Successful sending.', status=200)
    except:
        return HttpResponse('Not found. Your device token.', status=404)


def cert_upload(request):
    if not request.user.is_superuser:
        return redirect('notification:login')

    if request.method == 'POST':
        form = CertFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            result = upload_certificate(request.FILES['cert_file'], target_mode=int(request.POST['target']))
            return render(request, 'upload.html', result)

        else:
            return render(request, 'upload.html', {'error': 'invalid'}, status=400)
    else:
        form = CertFileUploadForm()
        return render(request, 'upload.html', {'form': form})
