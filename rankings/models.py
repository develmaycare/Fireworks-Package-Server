# Python Imports

# Django Imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local Imports
from packages.models import Package, Version

# Choices

PACKAGE_RANKING_CHOICES = (
    (999,'Not Applicable'),
    (100,'Excellent'),
    (75,'Very Good'),
    (50,'Good'),
    (25,'Bad'),
    (0,'Very Bad'),
)

# Models (Shift + I + "model" + TAB)

## Ranking
class Package_Ranking(models.Model):
    """Maintain ranking info for a package."""
    package = models.ForeignKey(Package,related_name='rankings')
    version = models.ForeignKey(Version)
    email = models.EmailField(help_text="Email address of the person ranking the package.")
    date_added = models.DateField(auto_now_add=True)
    code_quality = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="Does it follow the style guide. What style guide?")
    security = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="Have you found a security problem?")
    implementation = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="How well does the package addresses the stated need?")
    stability = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="Does it crash a lot?")
    look_and_feel = models.IntegerField(choices=PACKAGE_RANKING_CHOICES,help_text="Is it pretty? Or u-g-l-y?")

    class Meta:
        verbose_name = _("Ranking")
        verbose_name_plural = _("Rankings")

    def __unicode__(self):
        return str(self.total())

    def total(self):
        """Return the total for all ranking factors."""
        factors = ['code_quality', 'security', 'implementation', 'stability', 'look_and_feel']
        total = 0
        for factor in factors:
            if hasattr(self, factor):
                value = getattr(self, factor, 0)
                if value == 999:
                    continue
                total += value
        return total


