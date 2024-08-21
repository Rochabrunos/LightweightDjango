import sys
import os
from django.conf import settings

DEBUG= os.environ.get('DEBUG', 'on') == 'on',
SECRET_KEY= os.environ.get('SECRET_KEY', os.urandom(32)),
# ALLOWED_HOSTS= list(os.environ.get('ALLOWED_HOSTS', 'localhost,example.com').split(',')),
ALLOWED_HOSTS=[
    'localhost',
    '127.0.0.1',
]

BASE_DIR = os.path.dirname(__file__)
settings.configure(
    DEBUG= DEBUG,
    SECRET_KEY= SECRET_KEY,
    ALLOWED_HOSTS= ALLOWED_HOSTS,
    ROOT_URLCONF='sitebuilder.urls',
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=(
        'django.contrib.staticfiles', # {% static %} tag and collectstatic command
        # 'django.contrib.webdesign', # create placeholder text {% lorem %}
        'sitebuilder',
    ),
    STATIC_URL='/static/',
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
