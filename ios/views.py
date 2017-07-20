from django.shortcuts import render

from apnsclient import Session, APNs, Message
import datetime
import os
from django.conf import settings

PATH_TO_CERT_FILE = os.path.join(settings.BASE_DIR, 'static') + '/ios/Certificate/Django_Notification_opensecret.pem'

def test_push(request):

    apns_token = "2b2cb83c5f430a76171bf605deda9cad1559a01956ebb07178280fc1752c886f"

    session = Session()
    print("\033[94m", "filepath = ", PATH_TO_CERT_FILE, "\033[0m")
    con = session.get_connection("push_sandbox", cert_file=PATH_TO_CERT_FILE)

    srv = APNs(con)

    message = Message([apns_token], payload={"aps": {"alert": "title"}, "extra_message": "message_content"})
    # alertとかの引数あるけどカスタム情報送りたいなら全部Payloadで投げたほうがいい

    try:
        res = srv.send(message)
    except:
        print
        "Can't connect to APNs, looks like network is down"
    else:
        # Check failures. Check codes in APNs reference docs.
        for token, reason in res.failed.items():
            code, errmsg = reason
            # according to APNs protocol the token reported here
            # is garbage (invalid or empty), stop using and remove it.
            print
            "Device failed: {0}, reason: {1}".format(token, errmsg)

        # Check failures not related to devices.
        for code, errmsg in res.errors:
            print
            "Error: {}".format(errmsg)

        # Check if there are tokens that can be retried
        if res.needs_retry():
            # repeat with retry_message or reschedule your task
            retry_message = res.retry()

    delta = datetime.timedelta(minutes=5)
    session.outdate(delta)
    session.shutdown()






    return render(request, 'ios/test_push.html')