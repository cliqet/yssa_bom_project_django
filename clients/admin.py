from django.contrib import admin
from .models import Client
from utilities.models import ExportCsvMixin

LIST_PAGE_COUNT = 20


class ClientAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'company_name', 'contact_person', 'contact_no', 'email_address')
    ordering = ('id',)
    list_display_links = ['company_name']
    search_fields = ['company_name']
    list_per_page = LIST_PAGE_COUNT
    actions = ['export_as_csv']


admin.site.register(Client, ClientAdmin)
