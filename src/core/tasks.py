from celery import Celery


def get_controller():
    if hasattr(get_controller, 'instance'):
        return get_controller.instance
    else:
        celery = Celery()
        celery.conf.broker_url = 'redis://redis:6379/0'
        get_controller.instance = celery
        return celery
