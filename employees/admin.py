from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Department, EmployeePosition, Employee
from .forms import UserCreationForm, UserChangeForm
from utilities.models import ExportCsvMixin

LIST_PAGE_COUNT = 20


class DepartmentAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'department_name')
    ordering = ('id',)
    list_display_links = ['department_name']
    search_fields = ['department_name']
    list_per_page = LIST_PAGE_COUNT
    actions = ['export_as_csv']


class EmployeePositionAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'employee_position_title')
    ordering = ('id',)
    list_display_links = ['employee_position_title']
    search_fields = ['employee_position_title']
    list_per_page = LIST_PAGE_COUNT
    actions = ['export_as_csv']


class EmployeeAdmin(BaseUserAdmin, ExportCsvMixin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'id', 'email', 'first_name', 'last_name', 'contact_no', 'department', 'employee_position',
        'is_active', 'is_staff', 'is_superuser',
    )
    ordering = ('id',)
    list_display_links = ['email']
    list_filter = ['department', 'employee_position', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    list_per_page = LIST_PAGE_COUNT
    actions = ['export_as_csv']

    # Ensures that password field does not appear as plaintext
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password',)}),
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

    # Handle adding error when email is used as username since BaseUserAdmin
    # is looking for username
    add_fieldsets = (
        ('User Credentials', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        # Check if the user is a superuser
        if not request.user.is_superuser:
            # Remove the 'is_superuser' field from the fieldsets
            fieldsets = [
                (fieldset[0], {'fields': tuple(field for field in fieldset[1]['fields'] if field != 'is_superuser')})
                for fieldset in fieldsets
            ]

        return fieldsets

    # do not show superuser in list of users if current user is not a superuser
    def get_queryset(self, request):
        qs = super(EmployeeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)


admin.site.register(Department, DepartmentAdmin)
admin.site.register(EmployeePosition, EmployeePositionAdmin)
admin.site.register(Employee, EmployeeAdmin)
