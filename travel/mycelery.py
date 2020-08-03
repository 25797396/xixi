from celery import Celery
from django.conf import settings
import os

# 添加环境变量, 告知celery 该追随谁
os.environ.setdefault('DJANGO_SETTINGS_MODULE','travel.settings')

celery = Celery('travel', broker='redis://127.0.0.1:6379/0')

# 告知celery 去应用目录下 寻找 任务函数
celery.autodiscover_tasks(settings.INSTALLED_APPS)