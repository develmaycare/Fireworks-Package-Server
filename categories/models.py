# Python Imports

# Django Imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local Imports
from packages.models import Package

# Choices

# Models (Shift + I + "model" + TAB)

class Category(models.Model):
    """Categorization for packages."""
    title = models.CharField(max_length=128,unique=True)
    description = models.TextField(blank=True,null=True,help_text="Brief description of the category. Markdown is supported.")

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.title
    
    def total_packages(self):
        """Return the total number of packages under this category."""
        pass

class Package_Category(models.Model):
    """Connect packages with categories."""
    package = models.ForeignKey(Package, related_name="categories")
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name = _("Package Category")
        verbose_name_plural = _("Package Categories")

    def __unicode__(self):
        return self.category.title
