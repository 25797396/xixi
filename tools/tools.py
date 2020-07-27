import time
import jwt
from django.http import JsonResponse, HttpResponse
import os
from django.conf import settings
from django.shortcuts import render
from alipay import AliPay


# 生成token
def make_token(username, expire=3600*24):

    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'username':username, 'exp':now+expire}

    return jwt.encode(payload,key, algorithm='HS256')

# 获得来访者
def check_vistor(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token, settings.JWT_TOKEN_KEY)
    except Exception as e:
        print('get_user jwt error %s' % (e))
        return None
    username = res['username']
    return username

# 登录校验
def login_check(func):
    def wrap(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        print('token:',token)
        print('username:',kwargs['user'])
        if not token:
            res = {'code': 10005,'error': '请先登录'}
            return JsonResponse(res)

        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithm='HS256')
            print('res:',res['username'])
            if kwargs['user'] == res['username']:
                request.myuser = res['username']
                return func(request, *args, **kwargs)
        except Exception as e:
            res = {'code': 10006, 'error': '请先登录'}
            return JsonResponse(res)

    return wrap

# 删除图片
def del_img(filepath):
    print(filepath)

    # 获得文件名
    imgname = filepath.split('/')[-1]
    # 判断是否是默认图片
    if imgname == 'default.jpg':
        print('默认图片不删除')
        return
    # 判断文件是否存在
    if os.path.exists(filepath):
        os.remove(filepath)
        print('删除成功'+filepath)
        return True
    print('文件不存在,删除失败')
    return False

app_private_key_string = open(settings.ALIPAY_KEY_DIR+'app_private_key.pem').read()
alipay_public_key_string = open(settings.ALIPAY_KEY_DIR+'alipay_public_key.pem').read()


class MyAliPay():
    # 定义支付相关方法
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            # 当前网站的RSA私钥
            app_private_key_string=app_private_key_string,
            # 支付宝公钥
            alipay_public_key_string=alipay_public_key_string,
            # 指明签名算法 RSA256
            sign_type='RSA2',
            # 指明为测试
            debug=True
        )

    def get_trade_url(self, order_id, amount):
        # 生成支付链接
        # order_id 订单号
        # amount 金额
        base_url = 'https://openapi.alipaydev.com/gateway.do'
        order_string = self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=amount,
            # 订单标题
            subject=order_id,
            # 用户支付完毕,支付宝将用户跳转到哪里去
            return_url=settings.ALIPAY_RETURN_URL,
            # 支付结果 post 请求地址
            notify_url=settings.ALIPAY_NOTIFY_URL,
        )

        return base_url + "?" + order_string

    def get_verify_result(self, data, sign):

        # 验签 - True 验签成功 False 失败
        return self.alipay.verify(data, sign)

    def get_trade_result(self, order_id):
        # 主动向支付宝发出请求,查询订单结果
        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        if result.get("trade_status") == 'TRADE_SUCCESS':
            return True
        return False

