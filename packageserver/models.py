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
        js = '{"name":"%s","' %(self.first_name,self.last_name)
        if self.email: js += '"email": "%s"' %(self.email)
        if self.website: js += '"web": "%s"' %(self.website)
        js += "}"
        return js

class Cpu(models.Model):
    """Maintain CPU requirements for the target system.
    From the CommonJS spec:
    
    "Array of supported CPU architectures. If absent or set to the empty set, 
    the package makes no platform assumptions. The set of valid cpu names 
    includes: arm, mips, ppc, sparc, x86, x86_64.
    """
    title = models.CharField(max_length=128,unique=True,help_text="Official title.")
    name = models.CharField(max_length=64,unique=True,help_text="Short (canonical) name.")

    def __unicode__(self):
        return self.title

class Directory(models.Model):
    """Maintain the "directories" portion of the CommonJS spec."""
    name = models.CharField(max_length=128,help_text="The common name for the directory.")
    path = models.CharField(max_length=128,help_text="Path to the directory within the package.")
    description = models.TextField(blank=True,null=True,help_text="Brief description, especially if it's unusual.")

    class Meta:
        verbose_name_plural = "Directories"

    def __unicode__(self):
        return self.name

    def to_commonjs(self):
        """Convert the directory info to canonical CommonJS output."""
        return '"%s": "%s",' %(self.name,self.path)

class JavaScript_Engine(models.Model):
    """Maintain supported JavaScript engines for the target system.

    From the CommonJS spec:

    "Array of supported JavaScript engines. If absent or set to the empty set, 
    the package makes no platform assumptions. The set of valid engine names 
    includes: ejs, flusspferd, gpsee, jsc, spidermonkey, narwhal, node, rhino, 
    v8."
    """
    title = models.CharField(max_length=128,unique=True,help_text="Official title.")
    name = models.CharField(max_length=64,unique=True,help_text="Short (canonical) name.")
    class Meta:
        verbose_name = "JavaScript Engine"
        verbose_name_plural = "JavaScript Engines"

    def __unicode__(self):
        return self.title
 
class License(models.Model):
    """License under which a package is released."""
    title = models.CharField(max_length=128,help_text="Official name of the license.")
    abbreviation = models.CharField(max_length=64,help_text="Abbreviation or short name for the license.")
    url = models.URLField()

    def __unicode__(self):
        return self.title

    def to_commonjs(self):
        """Export license info as canonical CommonJS.
        Example:
        {
            "type": "GPLv2",
            "url": "http://www.example.com/licenses/gpl.html",
        }
        """
        return '{"type": "%s","url": "%s"}' %(self.abbreviation,self.url)

class Operating_System(models.Model):
    """Maintain operating system info for target system requirements.
    See Package.requirements.

    The CommonJS spec describes this as:

    "Array of supported operating systems. If absent or set to the empty set, 
    the package makes no platform assumptions. The set of valid os names 
    includes: aix, freebsd, linux, macos, solaris, vxworks, windows.
    "

    Since the field is multi-value, a simple foreign key does not work; a 
    many to many relationship is required.
    """
    title = models.CharField(max_length=128,unique=True,help_text="Official title.")
    name = models.CharField(max_length=64,unique=True,help_text="Short (canonical) name.")
    class Meta:
        verbose_name = "Operating System"
        verbose_name_plural = "Operating Systems"

    def __unicode__(self):
        return self.title

class Repo(models.Model):
    """A code repository of some sort."""
    type = models.CharField(max_length=64,choices=REPO_TYPES)
    url = models.URLField()
    path = models.CharField(max_length=1024,blank=True,null=True,help_text="Used to locate the repository if it does no reside at the root.")

    def __unicode__(self):
        if not self.path: return self.url
        return "%s/%s" %(self.url,self.path)

    def to_commonjs(self):
        """Export repo info as CommonJS."""
        js = '{"type": "%s","url": "%s"' %(self.type,self.url)
        if (self.path): js += ',"path": "%s"' %(self.path)
        js += '}'
        return js

class Script(models.Model):
    """Define scripts used by the package. See note at Package.scripts.
    """
    name = models.CharField(max_length=64,unique=True,help_text="Common name of the script.")
    path = models.CharField(max_length=256,help_text="File name or path of the script.")

    def __unicode__(self):
        return self.title

class Specification(models.Model):
    """Connect a package with one or more specifications. Used by the 
    "implements" portion of CommonJS. See note at Package.implements.
    """
    title = models.CharField(max_length=128,unique=True,help_text="Official title.")
    name = models.CharField(max_length=64,unique=True,help_text="The CommonJS wiki name or an arbitrary URL for the specification.")

    def __unicode__(self):
        return self.title

class System_Requirement(models.Model):
    """Connect a package with various system requirements, such as 
    operating system, CPU, etc.
    """
    os = models.ManyToManyField(Operating_System,blank=True,null=True)
    cpu = models.ManyToManyField(Cpu,blank=True,null=True)
    engines = models.ManyToManyField(JavaScript_Engine,blank=True,null=True)

    class Meta:
        verbose_name = "System Requirement"
        verbose_name_plural = "System Requirements"

    def __unicode__(self):
        return "NA"

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
    "Array of licenses under which the package is provided. This property is 
    not legally binding and does not necessarily mean your package is 
    licensed under the terms you define in this property. Each license is a 
    hash with a "type" property specifying the type of license and a url 
    property linking to the actual text. If the license is one of the official 
    open source licenses the official license name or its abbreviation may be 
    explicated with the "type" property. If an abbreviation is provided 
    (in parentheses), the abbreviation must be used."

    See http://www.opensource.org/licenses/alphabetical
    """
    licenses = models.ManyToManyField(License)

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
    
    """
    "Hash of prerequisite packages on which this package depends in order to 
    install and run. Each dependency defines the lowest compatible 
    MAJOR[.MINOR[.PATCH]] dependency versions (only one per MAJOR version) 
    with which the package has been tested and is assured to work. The 
    version may be a simple version string (see the version property for 
    acceptable forms), or it may be a hash group of dependencies which define 
    a set of options, any one of which satisfies the dependency. The ordering 
    of the group is significant and earlier entries have higher priority."

    I've set this up to refer to packages defined within the package server, 
    but the example appears to show more generic dependencies such as SSL
    version.

    Also, based on the volume of info required for a Package, it may not 
    make sense for this to be self-referencing.
    """
    dependencies = models.ManyToManyField('self',blank=True,null=True)

    """
    "An Array of string keywords to assist users searching for the package in 
    catalogs."

    I'm thinking of using the tagging package for Django.
    """
    keywords = models.TextField(blank=True,null=True)

    """
    "One of the following must also be in the package description file in 
    order for it to be valid.

    main - module that must be loaded when require(name) is called. Definition 
    must be relative to the package description file.

    directories.lib - directory of modules to be loaded under the packages 
    namespace. require(name/subfilename) must return modules from this 
    directory. Definition must be relative to the package description file."

    @todo We'll probably need to implement a check in the admin save_model() 
    method to make sure one or the other of these exists.
    """
    main = models.CharField(max_length=64,blank=True,null=True)
    directories_lib = models.CharField(max_length=64,blank=True,null=True)

    """
    "URL for submitting bugs. Can be mailto or http."

    Or both, based on the example. Maybe this should be organized into another 
    table? Good grief, we have so many already.
    """
    bug_url = models.URLField(blank=True,null=True,help_text="URL for submitting bugs.")
    bug_email = models.EmailField(blank=True,null=True,help_text="Email address for submitting bugs.")

    """
    "URL string for the package web site."

    I don't really like "homepage" as a field name, either.
    """
    website = models.URLField(blank=True,null=True,help_text="URL of the package's website.")

    """
    The CommonJS spec includes a number of fields that seems as though they 
    should have been organized into a "system requirements" field. I'm still 
    thinking about how to implement this in a sensible way. If we eventually 
    use GAE, perhaps there is a better way to do this using "no sql".

    For now, I'm abstracting these out to separate tables, allowing each 
    Package to connect to a single entity for "requirements", and this 
    entity handles the possible multi-value relationships. See 
    System_Requirement and the Cpu class for an example.
    """
    requirements = models.ForeignKey(System_Requirement)
    
    """
    "Boolean value indicating the package is built in as a standard component 
    of the underlying platform."
    """
    is_builtin = models.BooleanField(help_text="Indicates the package is built in as a standard component of the underlying platform.")

    """
    "Object hash of package directories. Typical directories include "lib", 
    "src", "doc", "jars", "test" and "bin". Package manager tools must use 
    these directory definitions to find various package components."
    """
    directories = models.ManyToManyField(Directory)

    """
    "Array of relevant CommonJS specifications this package supports. A 
    specification identifier is the WikiName of the specification prefixed by 
    "CommonJS/". Arbitrary URLs may also be specified to indicate support for 
    externally published specifications."
    """
    implements = models.ManyToManyField(Specification)

    """
    "Object hash of scripts used in managing the package. A package manager 
    tool may use these scripts to install, build, test or uninstall the 
    package."
    """
    scripts = models.ManyToManyField(Script)

    """
    "Object hash of identifiers for conditional replacements of top level 
    properties."

    """
    #overlay = ?

    """
    "Hash of package checksums. This checksum is used by package manager tools 
    to verify the integrity of a package."
    """
    #checksums = ?

    def __unicode__(self):
        return self.name

    def to_commonjs(self):
        """Convert the data canonical Common JS JSON worthy of a package.json 
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

