"""
Data models defining necessities for package management.

Notes

1. This data was created to serve packages for the Fireworks Project, but 
is able to be a pure CommonJS package server.

2. For reference, comments have been copied from the Common JS package page:

    http://wiki.commonjs.org/wiki/Packages/1.1

I've put these in "quotes" along with my own comments, if any.

3. Having now fleshed out the models, I wonder if a lot of this could be 
simplified by making certain fields multi-value with a separator. Do we 
really need a table for CPU!? Maybe this data could be validated on input
from a list of valid names.
"""

# Imports #
import os

from django.conf import settings as SETTINGS

from django.db import models

# Choices #

REPO_TYPES = (
    ('cvs','CVS'),
    ('git','Git'),
    ('svn','SVN'),
)

# Models #

class Contact(models.Model):
    """A contact person related to a package (maintainer, contributor)."""
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    website = models.URLField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)

    '''
    Probably need:
    added_by
    added_date
    modified_by
    modified_date
    '''

    def __unicode__(self):
        return "%s %s" %(self.first_name,self.last_name)

    def to_commonjs(self):
        """Export the contact as canonical CommonJS maintainer or contributor info.
        Example:
        {
            "name": "Bill Bloggs",
            "email": "billblogs@bblogmedia.com",
            "web": "http://www.bblogmedia.com",
        }
        """
        js = '{"name":"%s %s","' %(self.first_name,self.last_name)
        if self.email: js += '"email": "%s"' %(self.email)
        if self.website: js += '"web": "%s"' %(self.website)
        js += "}"
        return js

class Repo(models.Model):
    """A code repository of some sort."""
    type = models.CharField(max_length=64,choices=REPO_TYPES)
    url = models.URLField()
    path = models.CharField(max_length=1024,blank=True,null=True,help_text="Used to locate the repository if it does no reside at the root.")

    '''
    Probably need:
    added_by
    added_date
    modified_by
    modified_date
    '''

    def __unicode__(self):
        if not self.path: return self.url
        return "%s/%s" %(self.url,self.path)

    def to_commonjs(self):
        """Export repo info as CommonJS."""
        js = '{"type": "%s","url": "%s"' %(self.type,self.url)
        if (self.path): js += ',"path": "%s"' %(self.path)
        js += '}'
        return js

class Package(models.Model):
    """An individual package. This is patterned after the Common JS 
    definition of packages. See: 
    
    http://wiki.commonjs.org/wiki/Packages/1.1
    """

    """According to CommonJs, the title should be derived from the 
    description. I think there should be a unique title field apart 
    from the description.
    """
    title = models.CharField(max_length=128,unique=True,help_text="Official title of the package.")
    name = models.CharField(max_length=128,unique=True,help_text='This must be a unique, lowercase alpha-numeric name without spaces. It may include "." or "_" or "-" characters.')
    version = models.CharField(max_length=16,help_text='A version string conforming to the Semantic Versioning requirements at http://semver.org/')
    

    """
    "An Array of hashes each containing the details of a contributor. Format is 
    the same as for maintainer. By convention, the first contributor is the 
    original author of the package."

    But maybe we should have an author field connected to Contact?
    """
    contributors = models.ManyToManyField(Contact,related_name="package_contributors")

    """
    "Array of maintainers of the package. Each maintainer is a hash which must 
    have a "name" property and may optionally provide "email" and "web" 
    properties."
    """
    maintainers = models.ManyToManyField(Contact,related_name="package_maintainers")

    """
    "A brief description of the package. By convention, the first sentence (up 
    to the first .) should be usable as a package title in listings."

    I think there should probably be a title field. See comment on title().
    """
    description = models.TextField(help_text="A brief description of the package.")

    """
    "Array of repositories where the package can be located. Each repository 
    is a hash with properties for the "type" and "url" location of the 
    repository to clone/checkout the package. A "path" property may also be 
    specified to locate the package in the repository if it does not reside 
    at the root."

    Output example: 
    {"type": "git","url": "http://github.com/example.git", "path": "packages/mypackage"}
    """
    repositories = models.ManyToManyField(Repo)

   

    def __unicode__(self):
        return self.name

    def is_local(self):
        """Determine whether the package is local to this registry."""
        if os.path.exists('%s/data/packages/%s' %(SETTINGS.THIS_PATH,self.name)):
            return True
        return False

    def to_commonjs(self):
        """Convert the data canonical Common JS JSON worthy of a package.json 
        file. This is if we want to create a "true" package server that 
        supports Common JS.
        """
        js = '{"name":"%s","version":"%s","description":"%s",' %(self.name,self.version,self.description)

        js += '"maintainers": ['
        for Maintainer in self.maintainers.all():
            js += Maintainer.to_commonjs()
            js += ','
        js += '],'

        js += '"contributors": ['
        for Contributor in self.contributors.all():
            js += Contributor.to_commonjs()
            js += ','
        js += '],'

        js += '}'
        return js

