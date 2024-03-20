from django import forms
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