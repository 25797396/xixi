import json
import re
import math
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Strategy,StrategyComment,StrategyReply,Picture,PictureType
from user.models import User
from django.utils.decorators import method_decorator
from tools.tools import make_token,check_vistor,login_check,travel_cache
from tools.blfilter import PyBloomFilter
from django.core.cache import cache

# 获取我的文章页
def get_strategy_page(request, user):
    if request.method == 'GET':
        try:
            User.objects.get(username=user)
        except Exception as e:
            return HttpResponse(404)
        return render(request, 'strategy/strategy_list.html')

# 攻略主页
def get_strategyindex_page(request, page_id):
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
    @method_decorator(travel_cache())
    def get(self, request, user):
        vistor = check_vistor(request)
        s_id = request.GET.get('s_id')

        print('获取攻略信息-------------',s_id)
        u = User.objects.get(username=user)

        # 判断是否是用户本人
        if vistor == user:
            # 判断是否是获得指定攻略
            if s_id:
                if int(s_id)<=0:
                    return JsonResponse({'code':404})
                strategy = Strategy.objects.filter(id=s_id, is_delete=0)
                # 该攻略上一条数据
                pre_strategy = Strategy.objects.filter(create_time__lt=strategy[0].create_time, userId=u,
                                                       is_delete=0).last()
                # 该攻略下一条数据
                next_strategy = Strategy.objects.filter(create_time__gt=strategy[0].create_time, userId=u,
                                                        is_delete=0).first()
                # 判断是否存在上下条数据
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
                return JsonResponse({'code': 200, 'username':vistor,'data': data,'author':u.username,
                                     'pre_strategy':pre_strategy,
                                     'next_strategy':next_strategy,
                                     'comment_count':comment_count})
            else:

                strategys = u.strategy_set.all().filter(is_delete=0)
                data = get_strategy_dict(strategys, get='all')
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
                return JsonResponse({'code': 200, 'username':vistor,'data': data,'author':u.username,
                                     'pre_strategy':pre_strategy,
                                     'next_strategy':next_strategy,
                                     'comment_count':comment_count})
            else:
                strategys = u.strategy_set.all().filter(strategy_type='public')
                data = get_strategy_dict(strategys, get='all')
                return JsonResponse({'code': 200, 'username': vistor, 'data': data, 'author':u.username})

    # 编写攻略
    @method_decorator(login_check)
    def post(self, request, user):
        try:
            json_str = request.body
            json_obj = json.loads(json_str)

            # 获取信息
            title = json_obj['title']
            # coverImg =
            content_text = json_obj['content_text'][:180]
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
            # 布隆过滤器
            bf = PyBloomFilter()
            bf.add('travel_topic_cache_%s?s_id=%s'%(u.username,strategy.id))
            bf.add('travel_topic_cache_/strategy/strategy/%s'%(u.username))
            cache.delete('travel_topic_cache_/strategy/strategy/%s'%(u.username))   # 删除缓存
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

    # def clear_topic_caches(self, request):
    #     all_path = request.get_full_path()
    #     all_key_p = ['topic_cache_self', 'topic_cache']
    #     all_keys = []
    #     for key_p in all_key_p:
    #         for key_h in ['','?category=tec', '?category=no-tec']:
    #             all_keys.append(key_p+all_path+key_h)
    #
    #     for del_key in all_keys:
    #         cache.delete(del_key)

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
                s = Strategy.objects.get(id=s_id)
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
                cache_key = 'travel_topic_cache_%s' % (s.userId.username+'?s_id='+s_id)
                cache.delete(cache_key)
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
        cache_key = 'travel_topic_cache_%s' % (s.userId.username + '?s_id=' + s_id)
        cache.delete(cache_key)
        return JsonResponse({'code':200, 'data':{'username':u.username,'content':content,'avatar':str(u.avatar),
                                                 'create_time':comment.send_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                 'comment_id':comment.id}})

# 获得攻略主页信息
def get_index_info(request):

    page_id = request.GET.get('page_id')

    # 分页查询
    if page_id:
        cache_key = 'strategy_index_' + page_id
        page_id = int(page_id)
        if page_id>100:
            return HttpResponse(404)

        res = cache.get(cache_key)
        res_sum_page = cache.get('sum_page')
        if res_sum_page:
            sum_page = res_sum_page
        else:
            sum_page = math.ceil(Strategy.objects.count()/5)
            cache.set('sum_page',sum_page)
        if res:
            print('---有攻略主页缓存，返回缓存---')
            return res
        else:
            print('---无攻略主页缓存，查数据库，并存缓存---')
            strategys = Strategy.objects.filter(is_delete=0)[5 * (page_id - 1):5 * page_id]
            if strategys:
                data = get_strategy_dict(strategys, get='all')
                res = JsonResponse({'code': 200, 'data': data, 'sum_page': sum_page, 'current_page':page_id})
                cache.set(cache_key, res, 60)
                return res
            else:
                cache.set(cache_key, res, 30)
                return HttpResponse(404)


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
def get_strategy_dict(strategys, get='one'):
    data = []
    # 多个攻略
    if len(strategys)>1 and get=='all':
        for strategy in strategys:
            id = strategy.id
            title = strategy.title
            author = strategy.userId.username
            avatar = str(strategy.userId.avatar)
            # content = strategy.content
            browse_nums = strategy.browse_nums
            collection = strategy.collection
            good = strategy.good
            introduce = strategy.introduce
            create_time = strategy.create_time
            comments = strategy.strategycomment_set.all()
            comment_count = strategy.strategycomment_set.count()
            if comments:
                for comment in comments:
                    reply_count = comment.strategycomment_id.count()
                    comment_count += reply_count
            data.append(
                {'id': id, 'title': title, 'create_time': create_time.strftime("%Y-%m-%d %H:%M:%S"),
                 'browse_nums': browse_nums, 'collection': collection, 'good': good, 'comment_count': comment_count,
                 'introduce':introduce,'author':author, 'avatar':avatar
                 })

        return data

    # 指定攻略
    else:
        strategy = strategys[0]
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

