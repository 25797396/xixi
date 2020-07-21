from django.db import models
from scenic.models import Scenic
from scenic.models import Province,City,Area
from user.models import User

# 酒店
class Hotel(models.Model):
    name = models.CharField('酒店名', max_length=20)
    price = models.DecimalField('价格', decimal_places=2, max_digits=7)
    position = models.CharField('位置', max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=0)
    scenic = models.ManyToManyField(Scenic)         # 景点与酒店（多对多）

    class Meta:
        db_table = 'hotel'

# 预订订单
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    days = models.IntegerField(default=1)
    price = models.DecimalField('总价格', decimal_places=2, max_digits=7)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('修改时间', auto_now=True)

    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'order'