import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from tools.tools import login_check,MyAliPay
from .models import Hotel,Order
from user.models import User

def get_hotel_index_page(request):
    return render(request, 'hotel/index.html')

def get_hotel_detail_page(request):
    return render(request, 'hotel/detail.html')

# 获得酒店信息
def get_hotel_info(request):
    hotel_id = request.GET.get('hotel_id')
    page_id = request.GET.get('page_id')    # 页数

    if hotel_id:
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            name = hotel.name
            cover_img = str(hotel.cover_img)
            position = hotel.position
            price = hotel.price
            data={'name': name, 'cover_img': cover_img, 'position': position, 'price': price}
            return JsonResponse({'code':200, 'data':data})
        except Exception as e:
            print(e)
            return JsonResponse({'code':404})

    if page_id:
        page_id=0
    hotels = Hotel.objects.all()[page_id*20:20*(page_id+1)] # 每次取饿20条
    data= []
    for hotel in hotels:
        name = hotel.name
        cover_img = str(hotel.cover_img)
        position = hotel.position
        price = hotel.price
        data.append({'name':name, 'cover_img':cover_img, 'position':position, 'price':price})
    return JsonResponse({'code':200, 'data':data})

# 酒店订单
class HotelOrderView(View):

    # 获得订单信息
    @method_decorator(login_check)
    def get(self, request):
        username = request.myuser
        order_id = request.GET.get('order_id')
        user = User.objects.get(username=username)
        if order_id:
            try:
                order = Order.objects.get(user=user, id=order_id)
                hotel_name = order.hotel_name.name
                days = order.days
                price = order.price
                create_time = order.create_time
                modify_time = order.modify_time
                data={'username':user.username, 'hotel_name':hotel_name, 'days':days, 'price':price,
                      'create_time':create_time, 'modify_time':modify_time}

                return JsonResponse({'code':200,'data':data})
            except Exception as e:
                print(e)
                return JsonResponse({'code':404})

        orders = user.order_set.all()
        data=[]
        for order in orders:
            hotel_name = order.hotel_name.name
            days = order.days
            price = order.price
            create_time = order.create_time
            modify_time = order.modify_time
            data.append({'username': user.username, 'hotel_name': hotel_name, 'days': days, 'price': price,
                    'create_time': create_time, 'modify_time': modify_time})
        return JsonResponse({'code': 200, 'data': data})

    # 生成订单
    @method_decorator(login_check)
    def post(self, request, user):
        print(22222222222222)
        user = User.objects.get(username=request.myuser)
        json_str = request.body
        json_obj = json.loads(json_str)

        hotel_name = json_obj['hotel_name']
        hotel = Hotel.objects.filter(name=hotel_name)[0]
        if not hotel:
            return JsonResponse({'code': 404,'error':666})
        order_id = json_obj['order_id']
        days = json_obj['days']
        price = json_obj['price']

        try:
            Order.objects.create(order_id=order_id, user=user, price=price, hotel_name=hotel, days=days)
        except Exception as e:
            print(e)
            return JsonResponse({'code':404,'error':777})
        myalipay = MyAliPay()
        pay_url = myalipay.get_trade_url(order_id=order_id, amount=price)
        return JsonResponse({'code':200, 'pay_url': pay_url})


# 支付宝相关
class ResultView(MyAliPay):
    def get(self, request):
        # return url 支付完毕后 支付宝将用户重定向到该地址
        request_data = {k:request.GET[k] for k in request.GET.keys()}
        print('-'*50)
        print(request_data)
        sign = request_data.pop('sign')
        is_verify = self.get_verify_result(request_data, sign)

        if is_verify:
            # 数据合法
            order_id = request_data['out_trade_no']
            order = Order.objects.get(order_id=order_id)
            ORDER_STATUS = order.order_status
            if ORDER_STATUS == 2:
                # 状态由待付款变为已付款 由post完成
                return HttpResponse('支付成功')
            elif ORDER_STATUS == 1:
                # 备选方案
                # 主动向支付宝查询
                result =  self.get_trade_result(order_id)
                if result:

                    return HttpResponse('主动查询支付成功')
                else:
                    return HttpResponse('主动查询支付失败')
        else:
            # 请求有问题
            return HttpResponse('交钱失败')
        return HttpResponse("交钱成功")

    def post(self, request):
        # 支付完毕后,支付宝向notify_url 发送POST请求,并告知支付结果
        pass
