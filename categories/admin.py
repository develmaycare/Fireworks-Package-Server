# Python Imports

# Django Imports
from django.contrib import admin

# Local Imports
from categories.models import Category, Package_Category

# Actions

# Inlines
# stackedinline TAB
# tabularinline TAB

# Model Admins
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    ordering = ('title',)

class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ('package','category',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Package_Category, PackageCategoryAdmin)

