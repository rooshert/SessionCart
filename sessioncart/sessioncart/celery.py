import os
from celery import Celery
from django.conf import settings

# установили переменную DJANGO_SETTINGS_MODULE для программы командной строки Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sessioncart.settings')

celery_app = Celery('sessioncart')

'''
    Наконец, мы говорим Celery автоматически обнаруживать
    асинхронные задачи для приложений, перечисленных в параметрах INSTALLED_APPS.
    Celery будет искать файл tasks.py в каждом каталоге
    приложения для загрузки определенных в нем асинхронных задач.
'''
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
