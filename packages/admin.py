# Imports #

from django.contrib.auth.models import User
from django.contrib import admin

#from models import Category, Contact, Package, Ranking, Repo, Version
from models import Contact, Package, Version

# Inlines #

class VersionInline(admin.TabularInline):
    model = Version
    extra = 1
    fields = ('number','contributors','maintainers','repositories','keywords',)

# Model Admin #

class PackageAdmin(admin.ModelAdmin):
    list_display = ('title','name','added_date','added_by','modified_date','modified_by','author',)
    exclude = ('added_by','modified_by',)
    #inlines = [VersionInline,RankingInline,]
    inlines = [VersionInline,]
    prepopulated_fields = {'name':("title",)}

    def save_model(self, request, obj, form, change):
        """Automatically add the added_by and modified_by to the data."""
        try:
            getattr(obj, 'added_by', None)
        except User.DoesNotExist:
            obj.added_by = request.user
        obj.modified_by = request.user
        obj.save()

admin.site.register(Contact)
admin.site.register(Package,PackageAdmin)
admin.site.register(Version)
