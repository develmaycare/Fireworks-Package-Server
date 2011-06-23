"""
Custom context processors.
"""

# Python Imports
import datetime

# Django Imports
from django.conf import settings

# Processors

## config
def config(request):
    """Inject certain settings into usable template tokens."""
    d = {}
    d['ASSETS_URL'] = settings.ASSETS_URL
    d['CONTENT_URL'] = settings.CONTENT_URL
    d['COPYRIGHT_YEAR'] = datetime.datetime.now().strftime("%Y")
    d['COPYRIGHT_OWNER'] = settings.COPYRIGHT_OWNER
    d['SCRIPTS_URL'] = settings.SCRIPTS_URL
    return d
    

