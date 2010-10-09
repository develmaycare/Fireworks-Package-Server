"""
Various controllers for data I/O of the package server itself. This, too, is 
based upon the CommonJS standard.

See http://wiki.commonjs.org/wiki/Packages/Registry

To be compliant with CommonJS, two basic types of requests need to be handled:

1. Root - Return a list of packages in the registry. See index().

2. Package - Return info about a specific package in the registry. See 
package().

Note: A "package" request may be for the "package root url" or a "package
version url".
"""

# Imports #
from django.conf import settings as SETTINGS
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader


from decorators import html
from decorators import json
from models import *

# Supporting Functions #

def unsupported_accept_type(http_accept):
    """Return a "not acceptable" response when the accept type is not 
    supported; see notes on index() and package().
    """

    T = loader.get_template('unsupported_accept_type.json')

    tokens = {
        'accept_type': request.META['HTTP_ACCEPT'],
    }

    C = Context(tokens)

    if SETTINGS.DEBUG:
        return HttpResponse(T.render(C),status=406)
    else:
        return HttpResponse(T.render(C),mimetype="application/json",status=406)

# Views #

@html.index
@json.index
def index(request):
    """Respond to a root URL request by returning a list of packages in the 
    registry.

    The decorators actually do all the work, but if an unsupported Accept type 
    is sent, we need to handle it here by still sending a JSON response to 
    comply with the CommonJS standard. See HTTP Errors.
    """
    return unsupported_accept_type(request.META['HTTP_ACCEPT'])

@html.package
@json.package
def package(request,package_name,package_version=None):
    """Respond to a package root URL in the form of registry/<package_name>.

    As with index() above, the decorators do all the work, but if an unsupported 
    Accept type is sent, we need to handle it in the same way.
    """

    """Use this for testing:
    context = {
        'request': request,
        'output': 'Display package info: %s' %package_name,
    }
    if package_version is not None:
        context['output'] += ' (%s)' %package_version
    return render_to_response('testing.html',context)
    """

    return unsupported_accept_type(request.META['HTTP_ACCEPT'])

#@html.testing
#@json.testing
def testing(request):
    """A place to put quick tests."""

    #return unsupported_accept_type(request.META['HTTP_ACCEPT'])
    context = {
        'request': request,
        'output': 'This is a test.'
    }
    return render_to_response('testing.html',context)
