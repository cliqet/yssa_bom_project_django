from django.db import models
from django.apps import apps
from employees.models import Employee
from clients.models import Client


CLUSTER_BOOTH_TOTAL_COUNT_CHOICES = (
    ('0', '0'),
    ('4', '4'),
    ('6', '6'),
    ('8', '8'),
    ('10', '10'),
    ('12', '12'),
)

PERIMETER_BOOTH_TOTAL_COUNT_CHOICES = (
    ('0', '0'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
)


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

    cluster_booth_count_2x2 = models.CharField(
        default='0',
        max_length=2, 
        choices=CLUSTER_BOOTH_TOTAL_COUNT_CHOICES,
        verbose_name='Booth Count: 2 x 2 meters')
    cluster_total_count_2x2 = models.IntegerField(default=0, verbose_name='Total Count: 2 x 2 meters')
    
    cluster_booth_count_2x3 = models.CharField(
        default='0',
        max_length=2, 
        choices=CLUSTER_BOOTH_TOTAL_COUNT_CHOICES,
        verbose_name='Booth Count: 2 x 3 meters')
    cluster_total_count_2x3 = models.IntegerField(default=0, verbose_name='Total Count: 2 x 3 meters')
    
    cluster_booth_count_3x3 = models.CharField(
        default='0',
        max_length=2, 
        choices=CLUSTER_BOOTH_TOTAL_COUNT_CHOICES,
        verbose_name='Booth Count: 3 x 3 meters')
    cluster_total_count_3x3 = models.IntegerField(default=0, verbose_name='Total Count: 3 x 3 meters')    

    cluster_booth_count_3x4 = models.CharField(
        default='0',
        max_length=2, 
        choices=CLUSTER_BOOTH_TOTAL_COUNT_CHOICES,
        verbose_name='Booth Count: 3 x 4 meters')
    cluster_total_count_3x4 = models.IntegerField(default=0, verbose_name='Total Count: 3 x 4 meters')

    cluster_booth_count_4x4 = models.CharField(
        default='0',
        max_length=2, 
        choices=CLUSTER_BOOTH_TOTAL_COUNT_CHOICES,
        verbose_name='Booth Count: 4 x 4 meters')
    cluster_total_count_4x4 = models.IntegerField(default=0, verbose_name='Total Count: 4 x 4 meters')

    perimeter_booth_count_2x2 = models.CharField(
        default='0',
        max_length=2, 
        choices=PERIMETER_BOOTH_TOTAL_COUNT_CHOICES,
        verbose_name='Booth Count: 2 x 2 meters')
    perimeter_total_count_2x2 = models.IntegerField(default=0, verbose_name='Total Count: 2 x 2 meters')

    perimeter_booth_count_2x3 = models.CharField(
        default='0',
        max_length=2, 
        choices=PERIMETER_BOOTH_TOTAL_COUNT_CHOICES,
        verbose_name='Booth Count: 2 x 3 meters')
    perimeter_total_count_2x3 = models.IntegerField(default=0, verbose_name='Total Count: 2 x 3 meters')

    perimeter_booth_count_3x3 = models.CharField(
        default='0',
        max_length=2, 
        choices=PERIMETER_BOOTH_TOTAL_COUNT_CHOICES,
        verbose_name='Booth Count: 3 x 3 meters')
    perimeter_total_count_3x3 = models.IntegerField(default=0, verbose_name='Total Count: 3 x 3 meters')

    contingency = models.IntegerField(default=0, help_text='E.g. Enter 10 for 10%')

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
    
    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the Job instance is being created

        super().save(*args, **kwargs)
        BomGeneration = apps.get_model('jobs', 'BomGeneration')

        if created:
            BomGeneration.objects.create(
                post=1,
                panel=2,
                beam=3,
                facia_length=4,
                facia_width=5,
                corner_length_beam=6,
                corner_width_beam=7,
                job=self
            )
        else:
            existing_bom_generation = BomGeneration.objects.get(job=self)
            if existing_bom_generation:
                existing_bom_generation.post = 3
                existing_bom_generation.panel = 3
                existing_bom_generation.beam = 3
                existing_bom_generation.facia_length = 3
                existing_bom_generation.facia_width = 3
                existing_bom_generation.corner_length_beam = 3
                existing_bom_generation.corner_width_beam = 3

                existing_bom_generation.save()

class BomGeneration(models.Model):
    class Meta:
        verbose_name = 'BOM Generation'
        verbose_name_plural = 'BOM Generations'
        
    job = models.ForeignKey(Job, on_delete=models.PROTECT, editable=False)
    post = models.IntegerField(editable=False)
    panel = models.IntegerField(editable=False)
    beam = models.IntegerField(editable=False)
    facia_length = models.IntegerField(editable=False)
    facia_width = models.IntegerField(editable=False)
    corner_length_beam = models.IntegerField(editable=False)
    corner_width_beam = models.IntegerField(editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'BOM for Job ID: {self.job}'
    
    @property
    def event_name(self):
        return f'{self.job.event_name}'
    
    @property
    def event_venue(self):
        return f'{self.job.event_venue}'
    
    @property
    def start_date(self):
        return f'{self.job.start_date}'
    
    @property
    def end_date(self):
        return f'{self.job.end_date}'

    @property
    def client(self):
        return f'{self.job.client}'
    
    @property
    def ingress_date(self):
        return f'{self.job.ingress_date}'
    
    @property
    def ingress_time(self):
        return f'{self.job.ingress_time}'
    
    @property
    def egress_date(self):
        return f'{self.job.egress_date}'
    
    @property
    def egress_time(self):
        return f'{self.job.egress_time}'
    
    @property
    def sales_executive(self):
        return f'{self.job.sales_executive}'
    
    @property
    def prepared_by(self):
        return f'{self.job.prepared_by}'
    
    @property
    def reviewed_by(self):
        return f'{self.job.reviewed_by}'
    
    @property
    def approved_by(self):
        return f'{self.job.approved_by}'

