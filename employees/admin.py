from django.contrib import admin
from .models import Department, EmployeePosition, Employee


LIST_PAGE_COUNT = 20


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'contact_no', 'department', 'employee_position',
        'is_active', 'is_staff', 'is_superuser',
    )
    ordering = ('id',)
    list_display_links = ['email']
    list_filter = ['department', 'employee_position', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    list_per_page = LIST_PAGE_COUNT


admin.site.register(Department)
admin.site.register(EmployeePosition)
admin.site.register(Employee, EmployeeAdmin)
