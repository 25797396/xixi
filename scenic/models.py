from django.db import models

# 省
class Province(models.Model):
    provinceId = models.IntegerField('id', primary_key=True)
    province = models.CharField('省名',max_length=20)

    class Meta:
        db_table = 'province'

# 市
class City(models.Model):
    cityId = models.IntegerField('id', primary_key=True)
    city = models.CharField('城市名', max_length=20)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        db_table = 'city'

# 区
class Area(models.Model):
    areaId = models.IntegerField('id', primary_key=True)
    area = models.CharField('区名', max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        db_table = 'area'


# 景点类型
class ScenicType(models.Model):
    scenic_type = models.CharField('景点类型', unique=True, max_length=20)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'scenictype'

# 景点
class Scenic(models.Model):
    name = models.CharField('景点名称', max_length=20)
    scenicType = models.ForeignKey(ScenicType, on_delete=models.CASCADE)
    scenic_introduce = models.TextField('景点简介')
    position = models.CharField('位置', max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    ticket = models.DecimalField('门票', decimal_places=1, max_digits=7)
    popularity = models.IntegerField('人气')
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'scenic'

# 美食
class DeliciousFood(models.Model):
    scenic = models.ForeignKey(Scenic, on_delete=models.CASCADE)
    name = models.CharField('美食名字', max_length=20)
    food_introduction = models.CharField('美食简介', max_length=88)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'deliciousfood'