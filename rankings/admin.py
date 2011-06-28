# Python Imports

# Django Imports
from django.contrib import admin

# Local Imports
from rankings.models import Package_Ranking

# Actions

# Inlines
# stackedinline TAB
# tabularinline TAB

# Model Admins
class PackageRankingAdmin(admin.ModelAdmin):
    list_display = ('package', 'version', 'date_added', 'code_quality', 'security', 'implementation', 'stability', 'look_and_feel', 'total',)
    ordering = ('date_added',)

admin.site.register(Package_Ranking, PackageRankingAdmin)

