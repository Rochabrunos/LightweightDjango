import sys
import os

from django.conf import settings

DEBUG= os.environ.get('DEBUG', 'on') == 'on',
SECRET_KEY= os.environ.get('SECRET_KEY', os.urandom(32)),
ALLOWED_HOSTS= os.environ.get('ALLOWED_HOSTS', 'localhost').split(','),

settings.configure(
    DEBUG= DEBUG,
    SECRET_KEY= SECRET_KEY,
    ALLOWED_HOSTS= ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

from django import forms
from io import BytesIO
from PIL import Image

class ImageForm(forms.Form):
    """Form to validate requested placeholder image."""

    height = forms.IntegerField(min_value=1, max_value=4096)
    width = forms.IntegerField(min_value=1, max_value=4096)

    def generate(self, image_format='PNG'):
        """Generate an image of the given type and return as raw bytes"""
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        image = Image.new('RGB', (width, height))
        content = BytesIO()
        image.save(content, image_format)
        content.seek(0)
        return content

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.wsgi import get_wsgi_application

def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png', status=200)
    return HttpResponseBadRequest('Invalid Image Request')

def index(request):
    return HttpResponse('Hello World!')

from django.urls import re_path

urlpatterns = (
    re_path(r'^$', index, name='homepage'),
    re_path(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder')

)

# the Web Server Gateway Interface (WSGI) is the specification for how web servers communicate with application frameworks
application = get_wsgi_application()
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)