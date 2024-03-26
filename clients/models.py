from django.db import models


class Client(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    contact_person = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=50, blank=True, null=True)
    email_address = models.EmailField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'ID: {self.pk} - {self.company_name}'
