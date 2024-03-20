from django.contrib import admin
from .models import Job
from .forms import JobForm


LIST_PAGE_COUNT = 20


class JobAdmin(admin.ModelAdmin):
    form = JobForm
    list_display = (
        'job_id', 'sales_executive', 'event_name', 'event_venue', 'start_date', 'end_date', 
        'client', 'ingress_date', 'ingress_time', 'egress_date', 'egress_time',
        'prepared_by', 'reviewed_by', 'approved_by',
    )
    ordering = ('id',)
    list_display_links = ['job_id']
    list_filter = ['client', 'start_date']
    search_fields = ['job_id', 'event_name', 'event_venue']
    list_per_page = LIST_PAGE_COUNT


admin.site.register(Job, JobAdmin)

admin.site.site_header = "MSD Admin"
admin.site.site_title = "MSD Admin Portal"
admin.site.index_title = "Welcome to MSD Admin Portal"

