from django.contrib import admin
from .models import Product


LIST_PAGE_COUNT = 20


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'setup_type', 'name',)
    ordering = ('id',)
    list_display_links = ['name']
    list_filter = ['setup_type', 'name']
    list_per_page = LIST_PAGE_COUNT


admin.site.register(Product, ProductAdmin)
