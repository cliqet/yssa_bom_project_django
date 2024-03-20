from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Department, EmployeePosition, Employee


LIST_PAGE_COUNT = 20


class EmployeeAdmin(BaseUserAdmin):
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'contact_no', 'department', 'employee_position',
        'is_active', 'is_staff', 'is_superuser',
    )
    ordering = ('id',)
    list_display_links = ['email']
    list_filter = ['department', 'employee_position', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    list_per_page = LIST_PAGE_COUNT
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('User Information', {'fields': (
            'first_name',
            'last_name',
            'contact_no',
            'department',
            'employee_position'
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
    )

    # do not show superuser in list of users if current user is not a superuser
    def get_queryset(self, request):
        qs = super(EmployeeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)


admin.site.register(Department)
admin.site.register(EmployeePosition)
admin.site.register(Employee, EmployeeAdmin)
