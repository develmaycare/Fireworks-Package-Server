# Django settings for fwp-package-server project.

THIS_PATH = "/opt/src/fwp-package-server"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%s/data/server.db' %THIS_PATH,                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0qkjepg!rs378s6bl1!f1&bcprd&)jac1j-*%30e0_qz-#ns$a'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'application.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'application.context_processors.config',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/application/templates' %THIS_PATH,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'application.repos',
    'application.packages',
)

COPYRIGHT_OWNER = 'F.S. Davis'

"""
I have never liked the default static_media directory for lumping everything  
-- including user content -- into a single directory. I always create the following 
directories relative to the Django project, and these may be used to serve 
files (see below).
"""
ASSETS_PATH = "%s/assets" %THIS_PATH
CONTENT_PATH = "%s/content" %THIS_PATH
SCRIPTS_PATH = "%s/scripts" %THIS_PATH

"""
In debug mode, it is assumed that you have defined URL patterns using 
django.views.static.serve -- an example is:

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.ASSETS_PATH}),
    )

When in production, you may still use an Apache alias to refer to "/assets", or 
you may wish to host the files from another domain to improve load times.

In both cases, it is best to code your templates to use {{ASSETS_URL}} instead 
of the actual URL so as to make switching between development and production 
really easy. This does, however, require a context processor and the use of 
RequestContext (or better, use of direct_to_template).
"""
if DEBUG:
    ASSETS_URL = "/assets"
    CONTENT_URL = "/content"
    SCRIPTS_URL = "/scripts"
else:
    ASSETS_URL = "http://assets.example.com"
    CONTENT_URL = "http://content.example.com"
    SCRIPTS_URL = "http://scripts.example.com"



