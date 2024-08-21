from django.urls import re_path
from .views import page

urlpatterns = (
    re_path(r'^(?P<slug>[\w./-]+)/$', page, name='page'),
    re_path(r'^$', page, name='homepage'),
)
