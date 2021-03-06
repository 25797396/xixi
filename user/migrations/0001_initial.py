# Generated by Django 2.2.13 on 2020-07-15 14:17

from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=8, unique=True, verbose_name='用户名')),
                ('nickname', models.CharField(max_length=50, verbose_name='昵称')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('info', models.CharField(max_length=150, verbose_name='个人简介')),
                ('avatar', models.ImageField(null=True, upload_to=user.models.get_avatar_path)),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='注册日期')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow', to='user.User')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='user.User')),
            ],
            options={
                'db_table': 'follow',
            },
        ),
    ]
