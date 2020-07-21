import time
import jwt
from django.http import JsonResponse
import os
from django.conf import settings

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