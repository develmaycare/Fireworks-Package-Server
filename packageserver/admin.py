# Imports #

from django.contrib import admin

from models import Contact, Package, Package_Version, Package_Ranking, Repo

# Model Admin #

class PackageAdmin(admin.ModelAdmin):
    list_display = ('title','name','added_date','added_by','modified_date','modified_by','author',)
    exclude = ('added_by','modified_by',)

    def save_model(self,request,obj,form,change):
        """Automatically add the added_by to the data."""
        if getattr(obj,'added_by',None) is None:
            obj.added_by = request.user
        obj.modified_by = request.user
        obj.save()

class RepoAdmin(admin.ModelAdmin):
    list_display = ('type','added_date','added_by','link','comment',)
    exclude = ('added_by','modified_by',)

    def save_model(self,request,obj,form,change):
        """Automatically add the added_by to the data."""
        if getattr(obj,'added_by',None) is None:
            obj.added_by = request.user
        obj.modified_by = request.user
        obj.save()

admin.site.register(Contact)
admin.site.register(Package,PackageAdmin)
admin.site.register(Package_Version)
admin.site.register(Package_Ranking)
admin.site.register(Repo,RepoAdmin)
