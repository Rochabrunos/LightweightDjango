import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse
from django.test.client import Client

# loop though the pages directory and collect all .html files that are located there
def get_pages():
    for name in os.listdir(settings.SITE_PAGES_DIRECTORY):
        if name.endswith('.html'):
            yield name[:-5]

class Command(BaseCommand):
    help = 'Build static site output.'

    def add_arguments(self, parser):
        parser.add_argument("files", nargs="+")
    def handle(self, *args, **options):
        """Request pages and build output."""
        # Check if any arguments are passed into the command
        if args:
            pages = options['files']
            available = list(get_pages())
            invalid = []
            for page in pages:
                if page not in available:
                    invalid.append(page)
                if invalid:
                    # if any of the names passed don't exist, then an error is rased
                    msg = 'Invalid pages: {}'.format(', '.join(invalid))
                    raise CommandError(msg)
        else:
            # Checks if output directory exists, and remove it to create a new one
            if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
                shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)
            os.mkdir(settings.SITE_OUTPUT_DIRECTORY)
            os.mkdir(settings.STATIC_ROOT)
            # Copy all of the site static resources into the STATIC_ROOT, which is configured to be inside the SITE_OUTPUT_DIRECTORY
        call_command('collectstatic', interactive=False, clear=True, verbosity=0)
        client = Client()

        for page in get_pages():
            url = reverse('page', kwargs={'slug': page})
            response = client.get(url)
            if page == 'index':
                output_dir = settings.SITE_OUTPUT_DIRECTORY
            else:
                output_dir = os.path.join(settings.SITE_OUTPUT_DIRECTORY, page)
                # Handle the cases where the directory already exists
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
            # Here, the template is rendered as static content
            with open(os.path.join(output_dir, 'index.html'), 'wb') as f:
                f.write(response.content)