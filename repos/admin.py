# Django Imports

from django.contrib import admin

# Local Imports
from repos.models import Repo

# Inlines

# Model Admin

class RepoAdmin(admin.ModelAdmin):
    list_display = ('type','added_date','added_by','link','comment',)
    exclude = ('added_by','modified_by',)

    def save_model(self,request,obj,form,change):
        """Automatically add the added_by to the data."""
        if getattr(obj,'added_by',None) is None:
            obj.added_by = request.user
        obj.modified_by = request.user
        obj.save()

admin.site.register(Repo,RepoAdmin)