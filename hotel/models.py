from django.db import models
from scenic.models import Scenic
from scenic.models import Province,City,Area
from user.models import User

# 酒店
class Hotel(models.Model):
    name = models.CharField('酒店名', max_length=50)
    cover_img = models.ImageField(upload_to='hotel', default=None)
    price = models.DecimalField('价格', decimal_places=2, max_digits=7)
    position = models.CharField('位置', max_length=100)
    cityname = models.CharField('城市', max_length=20)
    # province = models.ForeignKey(Province, on_delete=models.CASCADE, default=None)
    # city = models.ForeignKey(City, on_delete=models.CASCADE, default=None)
    # area = models.ForeignKey(Area, on_delete=models.CASCADE, default=None)
    is_delete = models.BooleanField(default=0)
    scenic = models.ManyToManyField(Scenic, default=None)         # 景点与酒店（多对多）

    class Meta:
        db_table = 'hotel'

# 预订订单
class Order(models.Model):
    order_id = models.CharField(max_length=20,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    days = models.IntegerField(default=1)
    price = models.DecimalField('总价格', decimal_places=2, max_digits=7)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('修改时间', auto_now=True)
    order_status = models.IntegerField(default=1)   # 1 待付款 2 成功 3 失败

    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'order'