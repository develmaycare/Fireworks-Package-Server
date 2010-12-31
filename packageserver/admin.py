# Imports #

from django.contrib import admin

from models import Category, Contact, Package, Ranking, Repo, Version

# Inlines #

class RankingInline(admin.TabularInline):
    model = Ranking
    extra = 1

class VersionInline(admin.TabularInline):
    model = Version
    extra = 1
    fields = ('number','contributors','maintainers','repositories','keywords',)

# Model Admin #

class PackageAdmin(admin.ModelAdmin):
    list_display = ('title','name','added_date','added_by','modified_date','modified_by','author',)
    exclude = ('added_by','modified_by',)
    inlines = [VersionInline,RankingInline,]
    prepopulated_fields = {'name':("title",)}

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

admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Package,PackageAdmin)
admin.site.register(Ranking)
admin.site.register(Repo,RepoAdmin)
admin.site.register(Version)
