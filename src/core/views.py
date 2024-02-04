from django.http import HttpResponse
from .tasks import get_controller

def index(request):
    celery = get_controller()
    celery.send_task('test')
    return HttpResponse("Hello, world. You're at the polls index.")
