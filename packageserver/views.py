"""
Various controllers for data I/O of the package server itself. This, too, is 
based upon the CommonJS standard.

See http://wiki.commonjs.org/wiki/Packages/Registry
"""

# Imports #
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template import Context, RequestContext

from models import *

# Views #

def package(request,package_name,version_number=None):
    """Respond to a package root URL in the form of registry/<package_name>."""
    pass


