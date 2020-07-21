# Generated by Django 2.2.13 on 2020-07-15 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('scenic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='酒店名')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='价格')),
                ('position', models.CharField(max_length=50, verbose_name='位置')),
                ('is_delete', models.BooleanField(default=0)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.Area')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.City')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.Province')),
                ('scenic', models.ManyToManyField(to='scenic.Scenic')),
            ],
            options={
                'db_table': 'hotel',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='总价格')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=0)),
                ('hotel_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'order',
            },
        ),
    ]
