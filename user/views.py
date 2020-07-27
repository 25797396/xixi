from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views import View
from django.utils.decorators import method_decorator
from tools.tools import make_token,check_vistor,login_check,del_img
from django.db.models import Q,Max
from .models import User
from strategy.models import Strategy
from hotel.models import Hotel
from scenic.models import Scenic
from tools.sms import YunTongXin
import hashlib
import jwt
import json
import random
import os

# 主页
def index(request):
    # 返回主页
    if request.method == 'GET':
        return render(request, 'index.html')

# 登录注册页
def loginview(request):
    return render(request, 'user/login.html')

# 登录注册子页面
def loginandregister(request):
    return render(request, 'user/index.html')

# 获得主页信息
def get_index_data(request):

    if request.method == 'GET':
        imgs = []
        for i in range(1,5):
            imgs.append('/static/media/lunbo/img_%d.jpg'%(i))
        return JsonResponse({'code':200, 'imgs':imgs})

# 注册
def register(request):
    if request.method == 'POST':
        # post: 注册功能
        # 获取json字符串并获取信息
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        nickname = json_obj['username']
        password = json_obj['password']
        password2 = json_obj['password2']
        email = json_obj['email']
        phone = json_obj['phone']
        info = ''
        sms_num = int(json_obj['code'])

        # 验证验证码
        cache_key = 'sms_%s' % (phone)
        if cache.get(cache_key) != sms_num:
            return JsonResponse({'code': 10255, 'error': '验证码错误'})

        # 查找数据库
        u = User.objects.filter(username=username)
        if u:
            return JsonResponse({'code':10001, 'error':'用户名已被使用'})

        if password != password2:
            return JsonResponse({'code': 10002, 'error': '两次密码不一致'})

        # 将密码用md5加密
        h = hashlib.md5()
        h.update(password.encode())
        h_password = h.hexdigest()
        print(h_password)

        # 向数据库插入数据
        try:
            User.objects.create(username=username,password=h_password, email=email, phone=phone, info=info,
                                nickname=nickname)
            res = {'code':200, }
        except Exception as e:
            print(e)
            res = {'code': 10002, 'error': '新建用户失败'}
        return JsonResponse(res)

    return JsonResponse({'code':10009,'error':'I need post'})

# 登录
def login(request):

    if request.method == 'POST':
        # post: 登录功能
        json_str = request.body
        json_obj = json.loads(json_str)

        username = json_obj['username']
        password = json_obj['password']
        print(username)

        # 查看是否有该用户
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print('error:没有用户')
            res = {'code':10004, "error":"用户名或密码错误"}
            return JsonResponse(res)

        # 校验密码
        u_password = user.password
        h = hashlib.md5()
        h.update(password.encode())
        h_password = h.hexdigest()
        if u_password != h_password:
            print('error：密码错误')
            res = {'code': 10004, "error": "用户名或密码错误"}
            return JsonResponse(res)

        # 登录成功,签发token
        token = make_token(username)
        res = {'code':200, 'username':username, 'data':{'token':token.decode()}}
        print('ok')
        return JsonResponse(res)

    return JsonResponse({'code':10009,'error':'I need post'})

# 用户信息
class UserInfo(View):

    # 返回用户信息页
    def get(self, request, user):
        try:
            u = User.objects.get(username=user)
        except:
            return HttpResponse(404)
        return render(request, 'user/info.html')

    # 获得用户信息
    def post(self, request, user):
        # 检查来访者
        vistor = check_vistor(request)
        try:
            print('获得'+user+'信息')
            u = User.objects.get(username=user)

        except Exception as e:
            res = {'code':10005,'error':'查无此人'}
            return JsonResponse(res)

        username = u.username
        nickname = u.nickname
        email = u.email
        info = u.info
        avatar = u.avatar

        # 判断头像是否存在,不存在设置默认头像并返回
        avatar_path = os.path.join(settings.BASE_DIR,'static/media',str(avatar))
        if not os.path.exists(avatar_path) or str(avatar)=='':
            u.avatar = 'user/avatar/default.jpg'
            u.save()
            avatar = u.avatar

        res = {'code':200, 'data':{'username':username, 'email':email, 'info': info, 'nickname':nickname, 'avatar': str(avatar),
                                   'vistor': vistor}}
        return JsonResponse(res)

    # 修改用户信息
    @method_decorator(login_check)
    def put(self, request, user):

        json_str = request.body
        json_obj = json.loads(json_str)
        print(11111111111111)
        nickname = json_obj['nickname']
        info = json_obj['info']
        try:
            u = User.objects.get(username=request.myuser)
        except Exception as e:
            return JsonResponse({'code':10009,'error':'失败'})
        u.nickname = nickname
        u.info = info
        u.save()
        return JsonResponse({'code':200})

# 搜索
def search(request):
    search_content = request.GET.get('search_content')

    data = {}
    # 用户
    users = User.objects.filter(username__icontains=search_content)
    if users:
        u = []
        for user in users:
            username = user.username
            avatar = str(user.avatar)
            u.append({'username':username, 'avatar':avatar})
        data['user'] = u

    # 攻略
    strategys = Strategy.objects.filter(Q(title__icontains=search_content)|Q(content__contains=search_content))
    if strategys:
        s = []
        for strategy in strategys:
            title = strategy.title
            introduce = strategy.introduce
            create_time = strategy.create_time

            s.append({'title':title, 'introduce':introduce, 'create_time':create_time})

        data['strategys'] = s
    # 酒店
    hotels = Hotel.objects.filter(Q(name__icontains=search_content)|Q(position__contains=search_content))
    if hotels:
        for hotel in hotels:
            pass

    # 风景
    scenics = Scenic.objects.filter(name__icontains=search_content)
    if scenics:
        for scenic in scenics:
            pass

    return JsonResponse(data)

# 推荐
def recommend(request, choice='all'):

    strategys = Strategy.objects.filter(is_delete=0, strategy_type='public').order_by('-browse_nums','-comments')[:4]
    s = []
    for strategy in strategys:
        id = strategy.id
        title = strategy.title
        create_time = strategy.create_time
        browse_nums = strategy.browse_nums
        comments = strategy.comments
        content = strategy.content
        introduce = strategy.introduce
        username = strategy.userId.username
        avatar = str(strategy.userId.avatar)
        s.append({'id':id,'avatar':avatar,'title':title, 'content':content,'create_time':create_time.strftime("%Y-%m-%d %H:%M:%S"),
                  'introduce':introduce,'username':username,'browse_nums':browse_nums, 'comments':comments})

    return JsonResponse({'code':200, 'strategys':s})

# 用户上传头像
@login_check
def upload_avatar(request, user):

    # 获取图片对象
    new_avatar = request.FILES.get('avatar')
    username = request.myuser

    # 获得要改变头像的用户
    u = User.objects.get(username=username)

    # 获得旧头像路径
    old_avatar = str(u.avatar)
    u.avatar = new_avatar
    u.save()

    # 生成旧头像绝对路径,并删除旧头像
    old_avatar_path = os.path.join(settings.BASE_DIR,'static','media',old_avatar)
    del_img(old_avatar_path)

    print('用户：'+u.username+'---上传头像成功')
    return JsonResponse({'code':200})

# 获得导航栏状态
def is_login(request):
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)

        token = json_obj['t_token']
        username = json_obj['t_user']

        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithm='HS256')
        except Exception as e:
            print('--check login error %s' % (e))
            result = {'code': 10007}
            return JsonResponse(result)
        if res['username'] == username:
            result = {'code': 200, 'username': res['username']}
            return JsonResponse(result)

# 发送验证码
def sms_view(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    phone = json_obj['phone']

    cache_key = 'sms_%s'%(phone)
    if cache.get(cache_key):
        return JsonResponse({'code':10112, 'error':'请勿重复点击'})

    code= random.randint(1000,9999)
    cache.set(cache_key,code,65)

    # TODO 发送
    # 同步
    # x = YunTongXin(settings.SMS_ACCOUNT_ID, settings.SMS_ACCOUNT_TOKEN,
    #                settings.SMS_APP_ID, settings.SMS_TEMPLATE_ID)
    # res = x.run(phone, code)
    # print('---send result is %s'%(res))

    # 异步 -- celery
    # send_sms.delay(phone, code)

    # 测试使用
    print('---验证码为 %s' % (code))

    return JsonResponse({'code':200,})