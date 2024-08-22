import sys
import os
from django.conf import settings

DEBUG= os.environ.get('DEBUG', 'on') == 'on',
SECRET_KEY= os.environ.get('SECRET_KEY', os.urandom(32)),
# ALLOWED_HOSTS= list(os.environ.get('ALLOWED_HOSTS', 'localhost,example.com').split(',')),
ALLOWED_HOSTS=[
    'localhost',
    '127.0.0.1',
    'testserver',
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
        'sitebuilder',
    ),TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    }
    ],
    STATIC_URL='/static/',
    SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR, 'pages'),
    # Configures the output directory where the statically generated files will live
    SITE_OUTPUT_DIRECTORY=os.path.join(BASE_DIR, '_build'),
    # Here is where we enable static content to live in inside the _build directory
    STATIC_ROOT=os.path.join(BASE_DIR, '_build', 'static'),
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
