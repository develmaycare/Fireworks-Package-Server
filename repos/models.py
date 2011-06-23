"""
Repo models define the outer structure for both local and distributed package 
management.
"""

# Python Imports
import json

# Django Imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local Imports
from tracking.models import ATrackingData

# Choices

REPO_TYPES = (
    ('cvs','CVS'),
    ('git','Git'),
    ('hg', 'Mercurial'),
    ('local', 'Localhost'),
    ('svn','Subversion'),
)

# Models

## Repo
class Repo(ATrackingData):
    """A code repository of some sort."""
    type = models.CharField(_("type"), max_length=64,choices=REPO_TYPES, help_text=_("Type of repo."))
    url = models.URLField(_("url"), help_text=_("URL of the repo without the trailing slash."))
    path = models.CharField(_("path"), max_length=1024,blank=True,null=True,help_text=_("Used to locate the repository if it does no reside at the root."))
    comment = models.TextField(_("comment"), blank=True,null=True,help_text=_("Any useful info on the repo."))

    class Meta:
        verbose_name = _("Repository")
        verbose_name_plural = _("Repositories")

    def __unicode__(self):
        if not self.path: 
            return self.url
        return "%s/%s" %(self.url,self.path)

    def link(self):
        """Get the hyperlink to the Repo."""
        return '<a href="%s/%s">%s/%s</a>' %(self.url,self.path,self.url,self.path)
    link.allow_tags = True

    def to_dict(self):
        """Export the repo as a dictionary."""
        a = dict()
        a['type'] = self.type
        a['url'] = self.url
        if self.path:
            a['path'] = self.path
        return a 

    def to_json(self):
        """Convert repo data to a package.json format."""
        return json.dumps(self.to_dict())

    def total_packages(self):
        """Return a count of the packages associated with the repo."""
        pass
