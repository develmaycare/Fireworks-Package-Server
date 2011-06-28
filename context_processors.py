"""
Custom context processors.
"""

# Python Imports
#import datetime

# Django Imports
from django.conf import settings

# Processors

## config
def config(request):
    """Inject certain settings into usable template tokens."""
    d = {}
    d['ASSETS_URL'] = settings.ASSETS_URL
    d['CONTENT_URL'] = settings.CONTENT_URL
    d['COPYRIGHT_OWNER'] = settings.COPYRIGHT_OWNER
    d['COPYRIGHT_URL'] = settings.COPYRIGHT_URL
    #d['COPYRIGHT_YEAR'] = datetime.datetime.now().strftime("%Y")
    d['COPYRIGHT_YEAR'] = settings.COPYRIGHT_YEAR
    d['ORGANIZATION_NAME'] = settings.ORGANIZATION_NAME
    d['SCRIPTS_URL'] = settings.SCRIPTS_URL
    return d
    

