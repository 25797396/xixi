import sys
sys.path.append('../')
from django.conf import settings
from django.core.mail import send_mail
from travel.mycelery import celery
from tools.sms import YunTongXin

@celery.task
def sendMail(mail):
    msg = '服务器运行良好'
    send_mail(
        subject='修改密码',
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[mail]

    )
    print('发送邮件成功')

@celery.task
def sendSms(phone, code):
    x = YunTongXin(settings.SMS_ACCOUNT_ID, settings.SMS_ACCOUNT_TOKEN,
                   settings.SMS_APP_ID, settings.SMS_TEMPLATE_ID)
    res = x.run(phone, code)
    return res
    print('发送验证码成功')