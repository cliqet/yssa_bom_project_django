from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Job, BomGeneration
from employees.models import Employee
from .forms import JobForm


LIST_PAGE_COUNT = 20


class SalesExecutiveFilter(SimpleListFilter):
    """
        Filter used in admin to show only sales executives in filter options for 
        sales_executive which are still Employee objects
    """
    title = 'Sales Executives'
    parameter_name = 'sales_executive'

    def lookups(self, request, model_admin):
        sales_executives = Employee.objects.filter(
            employee_position__employee_position_title='Sales Executive'
        ).distinct()
        return [(se.id, str(se)) for se in sales_executives]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sales_executive__id=self.value())


class JobAdmin(admin.ModelAdmin):
    form = JobForm
    list_display = (
        'job_id', 'sales_executive', 'event_name', 'event_venue', 'start_date', 'end_date', 
        'client', 'ingress_date', 'ingress_time', 'egress_date', 'egress_time',
        'prepared_by', 'reviewed_by', 'approved_by',
    )
    ordering = ('id',)
    list_display_links = ['job_id']
    list_filter = ['client', 'start_date', SalesExecutiveFilter]
    search_fields = ['job_id', 'event_name', 'event_venue']
    list_per_page = LIST_PAGE_COUNT

    readonly_fields = ['created_at']

    fieldsets = (
        ('Job Information', {'fields': ('job_id', 'sales_executive', 'created_at')}),
        ('Event Details', {'fields': (
            'event_name',
            'event_venue',
            'start_date',
            'end_date'
        )}),
        ('Client Details', {'fields': ('client',)}),
        ('Setup Schedule', {'fields': (
            'ingress_date',
            'ingress_time',
            'egress_date',
            'egress_time'
        )}),
        ('Cluster Booth Requirements', {'fields': (
            ('cluster_booth_count_2x2', 'cluster_total_count_2x2'),
            ('cluster_booth_count_2x3', 'cluster_total_count_2x3'),
            ('cluster_booth_count_3x3', 'cluster_total_count_3x3'),
            ('cluster_booth_count_3x4', 'cluster_total_count_3x4'),
            ('cluster_booth_count_4x4', 'cluster_total_count_4x4'),
        )}),
        ('Perimeter Booth Requirements', {'fields': (
            ('perimeter_booth_count_2x2', 'perimeter_total_count_2x2'),
            ('perimeter_booth_count_2x3', 'perimeter_total_count_2x3'),
            ('perimeter_booth_count_3x3', 'perimeter_total_count_3x3'),
        )}),
        ('Other Information', {'fields': ('contingency',)}),
        ('Processing Information', {'fields': (
            'prepared_by',
            'reviewed_by',
            'approved_by'
        )}),
    )


class BomGenerationAdmin(admin.ModelAdmin):
    list_display = (
        'job', 'created_at'
    )
    ordering = ('id', 'created_at')
    list_display_links = ['job']
    search_fields = ['job__job_id']
    list_per_page = LIST_PAGE_COUNT

    fieldsets = (
        ('Job Information', {'fields': ('job', 'sales_executive', 'created_at')}),
        ('Cluster Post', {'fields': (
            'cluster_post_2x2', 'cluster_post_2x3', 'cluster_post_3x3',
            'cluster_post_3x4', 'cluster_post_4x4'
        )}),
        ('Cluster Panel', {'fields': (
            'cluster_panel_2x2', 'cluster_panel_2x3', 'cluster_panel_3x3',
            'cluster_panel_3x4', 'cluster_panel_4x4'
        )}),
        ('Cluster Beam', {'fields': (
            'cluster_beam_2x2', 'cluster_beam_2x3', 'cluster_beam_3x3',
            'cluster_beam_3x4', 'cluster_beam_4x4'
        )}),
        ('Cluster Facia Length', {'fields': (
            'cluster_facia_length_2x2', 'cluster_facia_length_2x3', 'cluster_facia_length_3x3',
            'cluster_facia_length_3x4', 'cluster_facia_length_4x4'
        )}),
        ('Cluster Facia Width', {'fields': (
            'cluster_facia_width_2x2', 'cluster_facia_width_2x3', 'cluster_facia_width_3x3',
            'cluster_facia_width_3x4', 'cluster_facia_width_4x4'
        )}),
        ('Cluster Corner Length Beam', {'fields': (
            'cluster_corner_length_beam_2x2', 'cluster_corner_length_beam_2x3', 'cluster_corner_length_beam_3x3',
            'cluster_corner_length_beam_3x4', 'cluster_corner_length_beam_4x4'
        )}),
        ('Cluster Corner Width Beam', {'fields': (
            'cluster_corner_width_beam_2x2', 'cluster_corner_width_beam_2x3', 'cluster_corner_width_beam_3x3',
            'cluster_corner_width_beam_3x4', 'cluster_corner_width_beam_4x4'
        )}),
        ('Perimeter Post', {'fields': (
            'perimeter_post_2x2', 'perimeter_post_2x3', 'perimeter_post_3x3'
        )}),
        ('Perimeter Panel', {'fields': (
            'perimeter_panel_2x2', 'perimeter_panel_2x3', 'perimeter_panel_3x3'
        )}),
        ('Perimeter Beam', {'fields': (
            'perimeter_beam_2x2', 'perimeter_beam_2x3', 'perimeter_beam_3x3'
        )}),
        ('Perimeter Facia Length', {'fields': (
            'perimeter_facia_length_2x2', 'perimeter_facia_length_2x3', 'perimeter_facia_length_3x3'
        )}),
        ('Perimeter Facia Width', {'fields': (
            'perimeter_facia_width_2x2', 'perimeter_facia_width_2x3', 'perimeter_facia_width_3x3'
        )}),
        ('Perimeter Corner Length Beam', {'fields': (
            'perimeter_corner_length_beam_2x2', 'perimeter_corner_length_beam_2x3', 'perimeter_corner_length_beam_3x3'
        )}),
        ('Perimeter Corner Width Beam', {'fields': (
            'perimeter_corner_width_beam_2x2', 'perimeter_corner_width_beam_2x3', 'perimeter_corner_width_beam_3x3'
        )}),
        ('Item Summary', {'fields': (
            'total_posts',
            'total_panels',
            'total_beams',
            'total_facia_lengths',
            'total_facia_widths',
            'total_corner_length_beams',
            'total_corner_width_beams'
        )}),
        ('Event Details', {'fields': (
            'event_name', 'event_venue', 'start_date', 'end_date'
        )}),
        ('Client Details', {'fields': ('client',)}),
        ('Setup Schedule', {'fields': (
            'ingress_date', 'ingress_time', 'egress_date', 'egress_time'
        )}),
        ('Processing Information', {'fields': (
            'prepared_by',
            'reviewed_by',
            'approved_by'
        )}),
    )

    # readonly_fields = [field.name for field in BomGeneration._meta.get_fields()]
    readonly_fields = [
        'job',
        
        'cluster_post_2x2', 'cluster_post_2x3', 'cluster_post_3x3', 'cluster_post_3x4', 'cluster_post_4x4', 
        'cluster_panel_2x2', 'cluster_panel_2x3', 'cluster_panel_3x3', 'cluster_panel_3x4', 'cluster_panel_4x4',
        'cluster_beam_2x2', 'cluster_beam_2x3', 'cluster_beam_3x3', 'cluster_beam_3x4', 'cluster_beam_4x4',
        'cluster_facia_length_2x2', 'cluster_facia_length_2x3', 'cluster_facia_length_3x3', 'cluster_facia_length_3x4', 'cluster_facia_length_4x4',
        'cluster_facia_width_2x2', 'cluster_facia_width_2x3', 'cluster_facia_width_3x3', 'cluster_facia_width_3x4', 'cluster_facia_width_4x4',
        'cluster_corner_length_beam_2x2', 'cluster_corner_length_beam_2x3', 'cluster_corner_length_beam_3x3', 'cluster_corner_length_beam_3x4', 'cluster_corner_length_beam_4x4',
        'cluster_corner_width_beam_2x2', 'cluster_corner_width_beam_2x3', 'cluster_corner_width_beam_3x3', 'cluster_corner_width_beam_3x4', 'cluster_corner_width_beam_4x4',
        
        'perimeter_post_2x2', 'perimeter_post_2x3', 'perimeter_post_3x3',
        'perimeter_panel_2x2', 'perimeter_panel_2x3', 'perimeter_panel_3x3',
        'perimeter_beam_2x2', 'perimeter_beam_2x3', 'perimeter_beam_3x3', 
        'perimeter_facia_length_2x2', 'perimeter_facia_length_2x3', 'perimeter_facia_length_3x3',
        'perimeter_facia_width_2x2', 'perimeter_facia_width_2x3', 'perimeter_facia_width_3x3',
        'perimeter_corner_length_beam_2x2', 'perimeter_corner_length_beam_2x3', 'perimeter_corner_length_beam_3x3',
        'perimeter_corner_width_beam_2x2', 'perimeter_corner_width_beam_2x3', 'perimeter_corner_width_beam_3x3',

        'total_posts', 'total_panels', 'total_beams', 'total_facia_lengths',
        'total_facia_widths', 'total_corner_length_beams', 'total_corner_width_beams',

        'event_name', 'event_venue', 'start_date', 'end_date',
        'client', 'ingress_date', 'ingress_time', 'egress_date', 'egress_time',
        'sales_executive', 'prepared_by', 'reviewed_by', 'approved_by', 'created_at'
    ]

    # Show all fields as read only when viewing details
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields
        return []
    
    # Disable add
    def has_add_permission(self, request, obj=None):
        return False
    
    # Disable delete
    # def has_delete_permission(self, request, obj=None):
    #     return False

    # Disable save
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(BomGenerationAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

admin.site.register(Job, JobAdmin)
admin.site.register(BomGeneration, BomGenerationAdmin)

admin.site.site_header = "MSD Admin"
admin.site.site_title = "MSD Admin Portal"
admin.site.index_title = "Welcome to MSD Admin Portal"

