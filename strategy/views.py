import json
import os
import re
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Strategy,StrategyComment,StrategyReply,Picture,PictureType
from user.models import User
from django.utils.decorators import method_decorator
from tools.tools import make_token,check_vistor,login_check

# 获取我的文章页
def get_strategy_page(request, user):
    if request.method == 'GET':
        try:
            User.objects.get(username=user)
        except Exception as e:
            return HttpResponse(404)
        return render(request, 'strategy/strategy_list.html')

# 攻略主页
def get_strategyindex_page(request):
    if request.method == 'GET':
        return render(request, 'strategy/index.html')

# 攻略详情页
def get_detail_page(request, user):
    if request.method == 'GET':
        return render(request, 'strategy/details.html')

# 获取编写攻略的页面
def get_writestrategy_page(request):
    #if request.method == 'GET':
    return render(request, 'strategy/writestrategy.html')

# 攻略
class StrategyView(View):

    # 获得攻略信息
    def get(self, request, user):
        vistor = check_vistor(request)
        s_id = request.GET.get('s_id')
        print('获取攻略信息-------------',s_id)
        u = User.objects.get(username=user)

        # 判断是否是用户本人
        if vistor == user:
            if s_id:
                strategy = Strategy.objects.filter(id=s_id, is_delete=0)
                pre_strategy = Strategy.objects.filter(create_time__lt=strategy[0].create_time, userId=u,
                                                       is_delete=0).last()
                next_strategy = Strategy.objects.filter(create_time__gt=strategy[0].create_time, userId=u,
                                                        is_delete=0).first()

                if pre_strategy:
                    pre_strategy = {'id':pre_strategy.id, 'title':pre_strategy.title}
                else:
                    pre_strategy = ''

                if next_strategy:
                    next_strategy = {'id':next_strategy.id, 'title':next_strategy.title}
                else:
                    next_strategy = ''
                if not strategy:
                    res = {'code':10010, 'error': '攻略不存在'}
                    return JsonResponse(res)
                strategy[0].browse_nums+=1
                strategy[0].save()
                data,comment_count = get_strategy_dict(strategy)
                strategy[0].comments = int(comment_count)
                strategy[0].save()
                return JsonResponse({'code': 200, 'username':vistor,'data': data,
                                     'pre_strategy':pre_strategy,
                                     'next_strategy':next_strategy,
                                     'comment_count':comment_count})
            else:
                strategys = u.strategy_set.all().filter(is_delete=0)
                data,comment_count = get_strategy_dict(strategys)
                return JsonResponse({'code':200, 'username':vistor, 'data':data})
        else:
            if s_id:
                strategy = Strategy.objects.filter(id=s_id, is_delete=0, strategy_type='public')
                pre_strategy = Strategy.objects.filter(create_time__lt=strategy[0].create_time, userId=u,
                                                       is_delete=0, strategy_type='public').last()
                next_strategy = Strategy.objects.filter(create_time__gt=strategy[0].create_time, userId=u,
                                                        is_delete=0, strategy_type='public').first()

                if pre_strategy:
                    pre_strategy = {'id':pre_strategy.id, 'title':pre_strategy.title}
                else:
                    pre_strategy = ''

                if next_strategy:
                    next_strategy = {'id':next_strategy.id, 'title':next_strategy.title}
                else:
                    next_strategy = ''
                if not strategy:
                    res = {'code':10010, 'error': '攻略不存在'}
                    return JsonResponse(res)
                strategy[0].browse_nums += 1
                strategy[0].save()
                data,comment_count = get_strategy_dict(strategy)
                strategy[0].comments = int(comment_count)
                strategy[0].save()
                return JsonResponse({'code': 200, 'username':vistor,'data': data,
                                     'pre_strategy':pre_strategy,
                                     'next_strategy':next_strategy,
                                     'comment_count':comment_count})
            else:
                strategys = u.strategy_set.all().filter(strategy_type='public')
                data,comment_count = get_strategy_dict(strategys)
                return JsonResponse({'code': 200, 'username': vistor, 'data': data})

    # 编写攻略
    @method_decorator(login_check)
    def post(self, request, user):
        try:
            json_str = request.body
            json_obj = json.loads(json_str)

            # 获取信息
            title = json_obj['title']
            # coverImg =
            content_text = json_obj['content_text'][:200]
            content = json_obj['content']
            type = json_obj['type']
            # 用正则匹配出图片路径
            imgs = re.findall(r'src="(.*?)"',content)

            # 判断文章类型
            if type not in ['public','private']:
                res = {'code': 10010, 'error': '错误'}
                return JsonResponse(res)

            u = User.objects.get(username=request.myuser)
            # 插入数据
            strategy = Strategy.objects.create(title=title, strategy_type=type, introduce=content_text,content=content, userId=u)

            # 遍历上传的图片路径
            for imgpath in imgs:
                imgpath = imgpath.replace('/static/media/','')
                try:
                    # 当有该图片时,将该图片与攻略相关联
                    pic = Picture.objects.get(picture_path=imgpath, is_upload=0)
                    pic.strategyId = strategy
                    pic.is_upload = 1
                    pic.save()
                except Exception as e:
                    print(e)
            print(u.username)
            res = {'code':200, }
            return JsonResponse(res)
        except Exception as e:
            print(e)

    # 删除攻略
    @method_decorator(login_check)
    def delete(self, request, user):
        s_id = request.GET.get('s_id')
        u = User.objects.get(username=request.myuser)
        if s_id:
            strategy = u.strategy_set.all().filter(id=s_id)   # 获得指定攻略
            if strategy:
                strategy.delete()
                return JsonResponse({'code':200})

        return JsonResponse({'code':10011,'error':'删除失败'})


# 评论
class Message(View):
    def get(self):
        pass

    # 发评论
    @method_decorator(login_check)
    def post(self, request, user):
        json_str = request.body
        json_obj =json.loads(json_str)
        s_id = request.GET.get('s_id')
        content = json_obj['content']
        print('comment_id' in json_obj)
        print('-------------------')
        # 判断是评论还是回复
        if 'comment_id' in json_obj:
            try:
                comment_id = int(json_obj['comment_id'].replace('comment',''))
                user = request.myuser
                u = User.objects.get(username=user)
                comment = StrategyComment.objects.get(id=comment_id)
                if 'touser' in json_obj:
                    print('回复的回复')
                    u2 = User.objects.get(username=json_obj['touser'])
                    reply = StrategyReply.objects.create(comment=comment,content=content, good=0,replyuser=u,touser=u2)
                    res = {'code':200, 'data':{
                        'reply_id': reply.id, 'reply_content':reply.content,
                        'reply_send_time':reply.send_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'reply_user': reply.replyuser.username, 'reply_avatar': str(reply.replyuser.avatar),
                        'reply_touser':reply.touser.username
                    }}
                else:
                    reply = StrategyReply.objects.create(comment=comment, content=content, good=0, replyuser=u)
                    res = {'code':200, 'data':{
                        'reply_id': reply.id, 'reply_content':reply.content,
                        'reply_send_time':reply.send_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'reply_user': reply.replyuser.username, 'reply_avatar': str(reply.replyuser.avatar),
                        'reply_touser':reply.touser
                    }}
                comment.strategy.comments+=1
                comment.strategy.save()
                return JsonResponse(res)
            except Exception as e:
                print(e)

        if not s_id or not content:
            res = {'code':10011,'error':'评论错误'}
            return JsonResponse(res)
        user = request.myuser
        try:
            s = Strategy.objects.get(id=s_id)
            u = User.objects.get(username=user)
            s.comments += 1
            s.save()
        except Exception as e:
            res = {'code': 10012, 'error': '评论错误'}
            return JsonResponse(res)
        comment = StrategyComment.objects.create(strategy=s, content=content, user=u, good=0)

        return JsonResponse({'code':200, 'data':{'username':u.username,'content':content,'avatar':str(u.avatar),
                                                 'create_time':comment.send_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                 'comment_id':comment.id}})

# 上传攻略图片
def upload(request):
    u = check_vistor(request)
    print(u)
    if u==None:
        return
    print('上传攻略图片')
    print('上传图片的用户'+u)
    u = User.objects.get(username=u)
    p_type = PictureType.objects.get(picture_type=4)
    for name in request.FILES:
        img = request.FILES[name]

        print(img)
    p = Picture.objects.create(picturetype=p_type,picture_path=img,userId=u)
    return JsonResponse({"errno":0,"data":['/static/media/'+str(p.picture_path)]})

# 生成攻略数据字典
def get_strategy_dict(strategys):
    data = []
    for strategy in strategys:
        id = strategy.id
        title = strategy.title
        content = strategy.content
        create_time = strategy.create_time
        browse_nums = strategy.browse_nums
        collection = strategy.collection
        good = strategy.good
        comments = strategy.strategycomment_set.all()
        comment = []
        comment_count = strategy.strategycomment_set.count()
        if comments:
            comment,reply_count = get_comment_dict(comments)
            comment_count+=reply_count
        data.append({'id': id, 'title': title, 'content':content,'create_time': create_time.strftime("%Y-%m-%d %H:%M:%S"),
                     'browse_nums':browse_nums, 'collection':collection, 'good':good, 'comment':comment,
                     })

    return data,comment_count

# 生成评论数据字典
def get_comment_dict(comments):
    data = []
    reply_count = 0
    for c in comments:
        c_id = c.id
        c_send_time = c.send_time
        c_content = c.content
        c_user = c.user.username
        c_avatar = str(c.user.avatar)
        c_reply = c.strategycomment_id.all()
        c_count = c.strategycomment_id.count()
        replys = []
        if c_reply:
            replys = get_reply_dict(c_reply)
        reply_count += c_count

        data.append({'c_id': c_id, 'c_user': c_user, 'c_avatar': c_avatar, 'c_content': c_content,
                        'c_send_time': c_send_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'c_replys':replys,'c_count':c_count})
    return data,reply_count

# 生成回复数据字典
def get_reply_dict(replys):
    data = []
    for r in replys:
        r_id = r.id
        r_comment = r.comment.id
        r_content = r.content
        r_good = r.good
        r_replyuser = r.replyuser.username
        if r.touser:
            r_touser = r.touser.username
        else:
            r_touser = ''
        r_send_time = r.send_time
        data.append({'r_id': r_id, 'r_replyuser': r_replyuser, 'r_avatar': str(r.replyuser.avatar),
                     'r_content': r_content,'r_send_time': r_send_time.strftime("%Y-%m-%d %H:%M:%S"),
                      'r_comment':r_comment,'r_good':r_good,'r_touser': r_touser})

    return data