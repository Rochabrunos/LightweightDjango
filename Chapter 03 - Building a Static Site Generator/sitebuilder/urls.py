from django.urls import re_path
from .views import page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^(?P<slug>[\w./-]+)/$', page, name='page'),
    re_path(r'^$', page, name='homepage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
