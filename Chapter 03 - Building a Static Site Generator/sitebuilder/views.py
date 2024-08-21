import os 

from django.conf import settings
from django.http import Http404, HttpResponse
from django.template import Template
from django.utils._os import safe_join

def get_page_or_404(name):
    """Return page content as a Django template object or raise 404 error."""
    try:
        # safe_join returns the template's filename, absolute version of the final path
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
    except ValueError:
        raise Http404('Page Not Found')
    else:
        if not os.path.exists(file_path):
            raise Http404('Page Not Found')
    # Opens each file and instanciate a new Django template object
    with open(file_path, 'r') as f:
        page = Template(f.read())
    
    return page

def page(request, slug='index'):
    """Render the requested page if found."""
    file_name = '{}.hmtl'.format(slug)
    page = get_page_or_404(file_name)
    context = {
        'slug': slug,
        'page': page,
    }

    return HttpResponse(page.render(context, request))