"""
Provide common tracking data.
"""

# Python Imports

# Django Imports
from django.contrib.admin.models import User
from django.db import models

# Local Imports

# Choices

REPO_TYPES = (
    ('cvs','CVS'),
    ('git','Git'),
    ('hg', 'Mercurial'),
    ('svn','Subversion'),
)

# Abstract Models

class ATrackingData(models.Model):
    """Base tracking data."""

    added_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_added_by")
    added_date = models.DateField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified_by")
    modified_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True

# Models
