from django.contrib import admin
from .models import Product
from utilities.models import ExportCsvMixin


LIST_PAGE_COUNT = 20


class ProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'setup_type', 'name',)
    ordering = ('id',)
    list_display_links = ['name']
    list_filter = ['setup_type', 'name']
    list_per_page = LIST_PAGE_COUNT
    actions = ['export_as_csv']


admin.site.register(Product, ProductAdmin)
