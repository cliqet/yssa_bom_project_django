# Generated by Django 5.0.3 on 2024-03-20 03:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=30, unique=True)),
                ('event_name', models.CharField(max_length=255)),
                ('event_venue', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('ingress_date', models.DateTimeField(auto_now_add=True)),
                ('ingress_time', models.TimeField(auto_now=True)),
                ('egress_date', models.DateTimeField(auto_now_add=True)),
                ('egress_time', models.TimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approver_employees', to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='clients.client')),
                ('prepared_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='preparer_employees', to=settings.AUTH_USER_MODEL)),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reviewer_employees', to=settings.AUTH_USER_MODEL)),
                ('sales_executive', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sales_executive_employees', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]