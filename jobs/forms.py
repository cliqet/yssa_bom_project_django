from django import forms
from django.db.models import Q
from employees.models import Employee
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the choices for the sales_executive field
        self.fields['sales_executive'].queryset = Employee.objects.filter(
            employee_position__employee_position_title='Sales Executive'
        )
        # Limit the choices for the prepared_by field
        self.fields['prepared_by'].queryset = Employee.objects.filter(
            employee_position__employee_position_title='Project Officer'
        )
        # Limit the choices for the reviewed_by field
        self.fields['reviewed_by'].queryset = Employee.objects.filter(
            employee_position__employee_position_title='Sales Executive'
        )
        # Limit the choices for the approved_by field
        self.fields['approved_by'].queryset = Employee.objects.filter(
            Q(employee_position__employee_position_title='Sales Executive') |
            Q(employee_position__employee_position_title='Purchasing')
        )