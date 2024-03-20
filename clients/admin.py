from django.contrib import admin
from .models import Client

LIST_PAGE_COUNT = 20


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'contact_person', 'contact_no', 'email_address')
    ordering = ('id',)
    list_display_links = ['company_name']
    search_fields = ['company_name']
    list_per_page = LIST_PAGE_COUNT


admin.site.register(Client, ClientAdmin)
