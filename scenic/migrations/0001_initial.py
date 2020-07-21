# Generated by Django 2.2.13 on 2020-07-15 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('areaId', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('area', models.CharField(max_length=20, verbose_name='区名')),
            ],
            options={
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('cityId', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('city', models.CharField(max_length=20, verbose_name='城市名')),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('provinceId', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('province', models.CharField(max_length=20, verbose_name='省名')),
            ],
            options={
                'db_table': 'province',
            },
        ),
        migrations.CreateModel(
            name='ScenicType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenic_type', models.CharField(max_length=20, unique=True, verbose_name='景点类型')),
                ('is_delete', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'scenictype',
            },
        ),
        migrations.CreateModel(
            name='Scenic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='景点名称')),
                ('scenic_introduce', models.TextField(verbose_name='景点简介')),
                ('position', models.CharField(max_length=50, verbose_name='位置')),
                ('ticket', models.DecimalField(decimal_places=1, max_digits=7, verbose_name='门票')),
                ('popularity', models.IntegerField(verbose_name='人气')),
                ('is_delete', models.BooleanField(default=0)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.Area')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.City')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.Province')),
                ('scenicType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.ScenicType')),
            ],
            options={
                'db_table': 'scenic',
            },
        ),
        migrations.CreateModel(
            name='DeliciousFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='美食名字')),
                ('food_introduction', models.CharField(max_length=88, verbose_name='美食简介')),
                ('is_delete', models.BooleanField(default=0)),
                ('scenic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.Scenic')),
            ],
            options={
                'db_table': 'deliciousfood',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.Province'),
        ),
        migrations.AddField(
            model_name='area',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.City'),
        ),
    ]
