"""
Data models defining necessities for package management.

Notes

1. This data was created to serve packages for the Fireworks Project, but 
is able to be a pure CommonJS package server.

2. For reference, comments have been copied from the Common JS package page:

    http://wiki.commonjs.org/wiki/Packages/1.1

3. Many of the multi-value fields (OS, CPU, etc.) have been specified as a 
simple text field. Breaking these out into separate, normalized models was too 
much.
"""

# Python Imports
import json
import os

# Django Imports
from django.conf import settings as SETTINGS
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local Imports
from repos.models import Repo
from tracking.models import ATrackingData

# Choices

# Models

class Contact(ATrackingData):
    """A contact person related to a package (maintainer, contributor)."""
    first_name = models.CharField(_("first name"), max_length=128, help_text=_("Contact's first name."))
    middle_name = models.CharField(_("middle name"), max_length=128, blank=True, null=True, help_text=_("Contact's middle name."))
    last_name = models.CharField(_("last name"), max_length=128, help_text=_("Contact's last name."))
    website = models.URLField(_("website"), blank=True,null=True, help_text=_("Website or blog for the contact."))
    email = models.EmailField(_("email"), blank=True,null=True, help_text=_("Email address of the contact."))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        """Return the full name of the contact."""
        return ' '.join([self.first_name, self.middle_name, self.last_name])

    def to_dict(self):
        """Return the contact's properties as a list.
        
        This is useful when building the contact into an external dictionary,
        as in:

            Author = Contact.objects.get(id=1)

            a = dict()
            a['author'] = Author.to_dict()
        """
        a = dict()
        a['name'] = self.full_name()
        if self.email:
            a['email'] = self.email
        if self.website:
            a['website'] = self.website
        return a

    def to_json(self):
        """Export the contact as canonical CommonJS maintainer or contributor info.
        Example:
        {
            "name": "Bill Bloggs",
            "email": "billblogs@bblogmedia.com",
            "web": "http://www.bblogmedia.com",
        }
        """
        return json.dumps(self.to_dict())

class Package(ATrackingData):
    """An individual package.
    
    Only general data is managed here. Any data that may change with the
    version of the package should not be included here.

    This is patterned after the Common JS definition of packages. See: 
    
    http://wiki.commonjs.org/wiki/Packages/1.1
    """

    title = models.CharField(_("title"), max_length=128, unique=True, help_text=_("Official title of the package."))
    name = models.SlugField(_("name"), max_length=128, unique=True, help_text=_('This must be a unique, lowercase alpha-numeric name without spaces. It may include "." or "_" or "-" characters.'))
    description = models.TextField(_("description"), help_text=_("A brief description of the package."))
    author = models.ForeignKey(Contact,verbose_name=_("author"), related_name="package_author", help_text=_("Original author of the package."))

    def __unicode__(self):
        return self.title

    def current_contributors(self):
        """Return a queryset of the current contributors."""
        Latest = self.versions.latest('added_date')
        return Latest.contributors.all()

    def current_maintainers(self):
        """Return a queryset of the current maintainers."""
        Latest = self.versions.latest('added_date')
        return Latest.maintainers.all()

    def get_absolute_url(self):
        # TODO: Implement permalink decorator.
        return "/packages/%s" %self.name

    def get_version_numbers(self):
        """Get a list of version numbers."""
        versions = list()
        for V in self.versions.all():
            versions.append(V.number)
        print versions
        return versions

    def get_version_numbers_as_links(self):
        """Get a list of version numbers as hyperlinks."""
        links = list()
        for i in self.get_version_numbers():
            links.append('<a href="%s/%s">%s</a>' %(self.get_absolute_url(),i,i))
        return links
    get_version_numbers_as_links.allow_tags = True

    def is_local(self):
        """Determine whether the package is local to this registry."""
        if os.path.exists('%s/data/packages/%s' %(SETTINGS.THIS_PATH,self.name)):
            return True
        return False

    def to_json(self):
        """Convert the data to canonical Common JS JSON suitable for a 
        package.json file.
        """
        a = dict()
        a['name'] = self.title
        a['version'] = self.latest_version_number()
        a['description'] = self.description
        
        return json.dumps(a)

    def latest_version_number(self):
        """Get the latest version number of the package."""
        try:
            Latest = Version.objects.latest('added_date')
            return Latest.number
        except Version.DoesNotExist:
            return None

class Version(ATrackingData):
    """Maintain package info for a specific version."""
    package = models.ForeignKey(Package, verbose_name=_("package"), related_name="versions", help_text=_("The package to which the version refers."))
    number = models.CharField(_("number"), max_length=16, help_text=_('A version string conforming to the Semantic Versioning requirements at http://semver.org/'))
    contributors = models.ManyToManyField(Contact, verbose_name=_("contributors"), blank=True, null=True, related_name="contributors", help_text=_("Package contributors."))
    maintainers = models.ManyToManyField(Contact, verbose_name=_("maintainers"), blank=True, null=True, related_name="maintainers", help_text=_("Package maintainers."))
    repositories = models.ManyToManyField(Repo, verbose_name=_("repositories"), related_name="repos")
    keywords = models.TextField(_("keywords"), blank=True, null=True, help_text=_("Any keywords associated with this version of the package."))
    is_builtin = models.NullBooleanField(_("is built-in"), help_text=_("Indicates the package is built in as a standard component of the underlying platform."))
    bug_url = models.URLField(_("bug url"), blank=True, null=True, help_text=_("URL where bugs may be submitted."))
    bug_email = models.EmailField(_("bug email"), blank=True, null=True, help_text=_("Email address to which bug reports may be sent."))
    website = models.URLField(_("website"), blank=True, null=True, help_text=_("URL of the package's website."))
    main = models.CharField(_("main"), max_length=64, blank=True, null=True, help_text=_("TBD"))
    directories_lib = models.CharField(_("directories lib"), max_length=64, blank=True, null=True, help_text=_("TBD"))

    class Meta:
        verbose_name = _("Package Version")
        verbose_name_plural = _("Package Versions")

    def __unicode__(self):
        return self.number

    def get_absolute_url(self):
        return "%s/%s" %(self.package.get_absolute_url(),self.number)

    def to_dict(self):
        """Return a dictionary representation of the version."""
        a = dict()
        return a

    def to_json(self):
        """Return a JSON representation of the version."""
        # http://code.google.com/p/jsonvalidator/
        pass
