from django.db import models
from django.utils import timezone
from employees.models import Employee
from clients.models import Client


class Job(models.Model):
    job_id = models.CharField(max_length=30, unique=True)
    sales_executive = models.ForeignKey(
        Employee, on_delete=models.PROTECT, null=True, blank=True, related_name='sales_executive_employees')
    event_name = models.CharField(max_length=255)
    event_venue = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)
    ingress_date = models.DateField(null=True, blank=True)
    ingress_time = models.TimeField(null=True, blank=True)
    egress_date = models.DateField(null=True, blank=True)
    egress_time = models.TimeField(null=True, blank=True)

    layout = models.ImageField(default='default.jpg', upload_to='layouts', help_text='Upload your layout here.')

    prepared_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, null=True, blank=True, related_name='preparer_employees')
    reviewed_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, null=True, blank=True, related_name='reviewer_employees')
    approved_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, null=True, blank=True, related_name='approver_employees')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.job_id}'