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

# Imports #
import os

from django.conf import settings as SETTINGS
from django.contrib.admin.models import User
from django.db import models

# Choices #

REPO_TYPES = (
    ('cvs','CVS'),
    ('git','Git'),
    ('svn','SVN'),
)

PACKAGE_RANKING_CHOICES = (
    (999,'Not Applicable'),
    (100,'Excellent'),
    (75,'Very Good'),
    (50,'Good'),
    (25,'Bad'),
    (0,'Very Bad'),
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
    comment = models.TextField(blank=True,null=True,help_text="Any useful info on the repo.")
    added_by = models.ForeignKey(User,blank=True,null=True,related_name='repo_added_by')
    added_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    modified_by = models.ForeignKey(User,blank=True,null=True,related_name='repo_modified_by')

    def __unicode__(self):
        if not self.path: return self.url
        return "%s/%s" %(self.url,self.path)

    def link(self):
        """Get the hyperlink to the Repo."""
        return '<a href="%s/%s">%s/%s</a>' %(self.url,self.path,self.url,self.path)
    link.allow_tags = True

    def to_commonjs(self):
        """Export repo info as CommonJS."""
        js = '{"type": "%s","url": "%s"' %(self.type,self.url)
        if (self.path): js += ',"path": "%s"' %(self.path)
        js += '}'
        return js


class Package_Version(models.Model):
    """Maintain package info for a specific version."""

    number = models.CharField(max_length=16,help_text='A version string conforming to the Semantic Versioning requirements at http://semver.org/')
    contributors = models.ManyToManyField(Contact,blank=True,related_name="package_contributors")
    maintainers = models.ManyToManyField(Contact,blank=True,related_name="package_maintainers")
    repositories = models.ManyToManyField(Repo)
    keywords = models.TextField(blank=True,null=True)
    is_builtin = models.BooleanField(help_text="Indicates the package is built in as a standard component of the underlying platform.")
    bug_url = models.URLField(blank=True,null=True,help_text="URL for submitting bugs.")
    bug_email = models.EmailField(blank=True,null=True,help_text="Email address for submitting bugs.")
    website = models.URLField(blank=True,null=True,help_text="URL of the package's website.")
    main = models.CharField(max_length=64,blank=True,null=True)
    directories_lib = models.CharField(max_length=64,blank=True,null=True)

    """
    @question Not sure how to handle this? The CommonJS example includes 
    generic dependencies such as webkit and SSL, but a registry must have 
    the ability to determine and locate other packages upon which the current 
    package depends.
    dependencies = models.ManyToManyField('self',blank=True,null=True)
    """

    """
    "licenses": [
        {
            "type": "GPLv2",
            "url": "http://www.example.com/licenses/gpl.html",
        }
    ]
    """
    licenses = models.TextField(blank=True,null=True)

    os = models.TextField(blank=True,null=True,help_text='Array of supported operating systems. If absent or set to the empty set, the package makes no platform assumptions. The set of valid os names includes: Valid example: ["aix", "freebsd", "linux", "macos", "solaris", "vxworks", "windows"]')

    cpu = models.TextField(blank=True,null=True,help_text='Array of supported CPU architectures. If absent or set to the empty set, the package makes no platform assumptions. The set of valid cpu names includes: ["arm", "mips", "ppc", "sparc", "x86", "x86_64"]')

    engine = models.TextField(blank=True,null=True,help_text='Array of supported JavaScript engines. If absent or set to the empty set, the package makes no platform assumptions. The set of valid engine names includes: ["ejs", "flusspferd", "gpsee", "jsc", "spidermonkey", "narwhal", "node", "rhino, "v8"]')

    """
    Object hash of package directories. Typical directories include "lib", "src", "doc", "jars", "test" and "bin". Package manager tools must use these directory definitions to find various package components.
    "directories": {
       "lib": "src/lib",
       "bin": "local/binaries",
       "jars": "java" 
    } 
    """
    directories = models.TextField(blank=True,null=True)

    implements = models.TextField(blank=True,null=True,help_text='Array of relevant CommonJS specifications this package supports. A specification identifier is the WikiName of the specification prefixed by "CommonJS/". Arbitrary URLs may also be specified to indicate support for externally published specifications.  ["CommonJS/Modules/1.0", "CommonJS/JSGI/1.0"]')

    """
    Object hash of scripts used in managing the package. A package manager tool may use these scripts to install, build, test or uninstall the package. For example:

    "scripts": {
       "install": "install.js",
       "uninstall": "uninstall.js",
       "build": "build.js",
       "doc": "make-doc.js",
       "test": "test.js",
    }
    """
    scripts = models.TextField(blank=True,null=True)

    """
    @question How is overlay used? Spec says:

        Object hash of identifiers for conditional replacements of top level 
        properties.

        "overlay": {
           "node" : {"dependencies":[...]},
           "npm"  : {"scripts":{"install":"./npm-install.sh"}
         }

    overlay = ?
    """

    """
    @question How should this be implemented? Info from spec:

        Hash of package checksums. This checksum is used by package manager tools 
        to verify the integrity of a package.

        {"md5": "841959b03e98c92d938cdeade9e0784d"}
    
    checksums = 
    """

    class Meta:
        verbose_name = "Package Version"
        verbose_name_plural = "Package Versions"

    def __unicode__(self):
        return self.number

class Package(models.Model):
    """An individual package. This is patterned after the Common JS 
    definition of packages. See: 
    
    http://wiki.commonjs.org/wiki/Packages/1.1
    """

    title = models.CharField(max_length=128,unique=True,help_text="Official title of the package.")
    name = models.CharField(max_length=128,unique=True,help_text='This must be a unique, lowercase alpha-numeric name without spaces. It may include "." or "_" or "-" characters.')
    description = models.TextField(help_text="A brief description of the package.")
    versions = models.ManyToManyField(Package_Version)
    author = models.ForeignKey(Contact,related_name="package_author",help_text="Original author of the package.")
    added_by = models.ForeignKey(User,blank=True,null=True,related_name='package_added_by')
    added_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    modified_by = models.ForeignKey(User,blank=True,null=True,related_name='package_modified_by')
    versions = models.ManyToManyField(Package_Version)

    def __unicode__(self):
        return self.name

    def is_local(self):
        """Determine whether the package is local to this registry."""
        if os.path.exists('%s/data/packages/%s' %(SETTINGS.THIS_PATH,self.name)):
            return True
        return False

    def to_commonjs(self):
        """Convert the data to canonical Common JS JSON worthy of a package.json 
        file. This is if we want to create a "true" package server that 
        supports Common JS.
        """
        js = '{"name":"%s","version":"%s","description":"%s",' %(self.name,self.version,self.description)
        if self.keywords: js += '"keywords": [%s],' %self.keywords

        js += '"maintainers": ['
        for Maintainer in self.maintainers:
            js += Maintainer.to_commonjs()
            js += ','
        js += '],'

        js += '"contributors": ['
        for Contributor in self.contributors:
            js += Contributor.to_commonjs()
            js += ','
        js += '],'

        js += '"bugs": {"mail": "%s","web": "%s"},'

        js += '"licenses": ['
        for License in self.licenses:
            js += License.to_commonjs()
            js + ','
        js += '],'

        js += '"repositories": ['
        for Repo in self.repositories:
            js += Repo.to_commonjs()
            js += ','
        js += '],'

        js += '"dependencies": {'
        for Dependency in self.dependencies:
            js += '"%s":"%s",' %(Dependency.name,Dependency.version)
        js += '},'

        if self.implements:
            js += '"implements": [' 
            for Spec in self.implements:
                js += '"%s",' %Spec.name
            js += '],'

        if self.requirements:
            if self.requirements.os:
                js += '"os": ['
                for r in self.requirements.os:
                    js += '"%s",' %r.name
                js += '],'
            if self.requirements.cpu:
                js += '"cpu": ['
                for r in self.requirements.cpu:
                    js += '"%s",' %r.name
                js += '],'
            if self.requirements.engines:
                js += '"engine": ['
                for r in self.requirements.engines:
                    js += '"%s",' %r.name
                js += '],'

        if self.scripts:
            js += '"scripts": {'
            for Script in self.Scripts:
                js += '"%s": "%s",' %(Script.name,Script.path)
            js += '},' 

        if self.directories:
            js += '"scripts": {'
            for Dir in self.Dir:
                js += '"%s": "%s",' %(Dir.name,Dir.path)
            js += '},' 

        # This closes the JSON output.
        js += '}'

        return js

class Package_Ranking(models.Model):
    """Initial stab at maintaining package ranking data."""
    package = models.ForeignKey(Package)
    version = models.ForeignKey(Package_Version)
    email = models.EmailField(help_text="Email address of the person ranking the package.")
    added_date = models.DateField(auto_now_add=True)
    code_quality = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="Does it follow the style guide. What style guide?")
    security = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="Have you found a security problem?")
    implementation = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="How well does the package addresses the stated need?")
    stability = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="Does it crash a lot?")
    look_and_feel = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="Is it pretty? Or u-g-l-y?")

    class Meta:
        verbose_name = "Package Ranking"
        verbose_name_plural = "Package Rankings"

    def __unicode__(self):
        return "%s %s" %(self.package,self.version)

