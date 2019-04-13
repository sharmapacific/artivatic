from artivatic.celery import app as celery_app
from base.decorators import apiplexer


class Task:
    @staticmethod
    def send(name, args=(), kwargs={}, **opts):
        return celery_app.send_task(name, args, kwargs, **opts)


@apiplexer
class CeleryTask:
    api_settings = 'SEND_TASK_CELERY'
    methods = ('send',)
