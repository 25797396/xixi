# Generated by Django 2.2.13 on 2020-07-29 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_hotel_cityname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=models.CharField(max_length=50, verbose_name='酒店名'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='position',
            field=models.CharField(max_length=100, verbose_name='位置'),
        ),
    ]
