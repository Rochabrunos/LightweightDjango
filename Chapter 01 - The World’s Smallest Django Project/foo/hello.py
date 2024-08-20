import sys
import os

from django.conf import settings


settings.configure(
    DEBUG= os.environ.get('DEBUG', 'on') == 'on',
    SECRET_KEY= os.environ.get('SECRET_KEY', os.urandom(32)),
    ALLOWED_HOSTS= os.environ.get('ALLOWED_HOSTS', 'localhost').split(','),
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

from django.urls import re_path
from django.http import HttpResponse
from django.core.wsgi import get_wsgi_application

def index(request):
    return HttpResponse('Hello World!')

urlpatterns = (
    re_path(r'^$', index),
)

# the Web Server Gateway Interface (WSGI) is the specification for how web servers communicate with application frameworks
application = get_wsgi_application()
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)