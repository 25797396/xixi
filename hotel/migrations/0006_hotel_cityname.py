# Generated by Django 2.2.13 on 2020-07-29 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_auto_20200723_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='cityname',
            field=models.CharField(default=1, max_length=20, verbose_name='城市'),
            preserve_default=False,
        ),
    ]
