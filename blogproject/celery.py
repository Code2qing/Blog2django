"""
# @Time    : 2019-03-09 21:09
# @Author  : qingjl！！
# @FileName: celery.py
# @Software: PyCharm
"""
from __future__ import absolute_import
import os
from celery import Celery, platforms

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'blogproject.settings')
app = Celery("blogproject")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()
platforms.C_FORCE_ROOT = True
