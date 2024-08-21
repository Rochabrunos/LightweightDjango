import sys
import os

from django.conf import settings

DEBUG= os.environ.get('DEBUG', 'on') == 'on',
SECRET_KEY= os.environ.get('SECRET_KEY', os.urandom(32)),
# ALLOWED_HOSTS= list(os.environ.get('ALLOWED_HOSTS', 'localhost,example.com').split(',')),
ALLOWED_HOSTS=[
    'localhost',
    'example.com',
]
BASE_DIR = os.path.dirname(__file__)

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
    INSTALLED_APPS=(
        'django.contrib.staticfiles', # {% static %} tag and collectstatic command
    ),
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
        },
    ],
    TEMPLATE_DIRS=(
        os.path.join(BASE_DIR, 'templates'),
    ),
    STATICFILES_DIRS=(
        os.path.join(BASE_DIR, 'static'),
    ),
    STATIC_URL='/static/',
)

from django import forms
from django.core.cache import cache
from io import BytesIO
from PIL import Image, ImageDraw

class ImageForm(forms.Form):
    """Form to validate requested placeholder image."""

    height = forms.IntegerField(min_value=1, max_value=4096)
    width = forms.IntegerField(min_value=1, max_value=4096)

    def generate(self, image_format='PNG'):
        """Generate an image of the given type and return as raw bytes"""
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '%s.%s.%s' % (width,height, image_format)
        content = cache.get(key)
        if content is None:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{} x {}'.format(width, height)
            _, _, textwidth, textheight = draw.textbbox((0, 0), text=text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill=(255,255,255))
            content = BytesIO()
            image.save(content, image_format)
            cache.set(key, content, 60*60)
        content.seek(0)
        return content
    
import hashlib
from django.urls import reverse
from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.wsgi import get_wsgi_application
from django.views.decorators.http import etag

def generate_etag(request, width, height):
    content = 'Placeholder: {0} x {1}'.format(width, height)
    return hashlib.sha512(content.encode('UTF-8')).hexdigest()

# Using etag decorator has the advantage of calculating the ETag prior to the view being called,
# which will also save on the processing time and resources.
@etag(generate_etag)
def placeholder(_, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    return HttpResponseBadRequest('Invalid Image Request')

def index(request):
    """Build an example URL by reversing the placeholder view, and passes it to the template context"""
    example = reverse(placeholder, kwargs={'width':50, 'height': 50})
    context = {
        'example': request.build_absolute_uri(example),
    }

    return render(request, template_name='home/home.html', context=context)

from django.urls import re_path

urlpatterns = (
    re_path(r'^$', index, name='homepage'),
    re_path(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)$', placeholder, name='placeholder')

)

# the Web Server Gateway Interface (WSGI) is the specification for how web servers communicate with application frameworks
application = get_wsgi_application()
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)