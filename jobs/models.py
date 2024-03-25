import math
from typing import Self
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
    
    def create_bom(self, bom_model, computed_bom: dict):
        bom_model.objects.create(
            # Cluster
            cluster_post_2x2 = computed_bom.get('cluster_post_count_2x2'),
            cluster_post_2x3 = computed_bom.get('cluster_post_count_2x3'),
            cluster_post_3x3 = computed_bom.get('cluster_post_count_3x3'),
            cluster_post_3x4 = computed_bom.get('cluster_post_count_3x4'),
            cluster_post_4x4 = computed_bom.get('cluster_post_count_4x4'),

            cluster_panel_2x2 = computed_bom.get('cluster_panel_count_2x2'),
            cluster_panel_2x3 = computed_bom.get('cluster_panel_count_2x3'),
            cluster_panel_3x3 = computed_bom.get('cluster_panel_count_3x3'),
            cluster_panel_3x4 = computed_bom.get('cluster_panel_count_3x4'),
            cluster_panel_4x4 = computed_bom.get('cluster_panel_count_4x4'),

            cluster_beam_2x2 = computed_bom.get('cluster_beam_count_2x2'),
            cluster_beam_2x3 = computed_bom.get('cluster_beam_count_2x3'),
            cluster_beam_3x3 = computed_bom.get('cluster_beam_count_3x3'),
            cluster_beam_3x4 = computed_bom.get('cluster_beam_count_3x4'),
            cluster_beam_4x4 = computed_bom.get('cluster_beam_count_4x4'),

            cluster_facia_length_2x2 = computed_bom.get('cluster_facia_length_count_2x2'),
            cluster_facia_length_2x3 = computed_bom.get('cluster_facia_length_count_2x3'),
            cluster_facia_length_3x3 = computed_bom.get('cluster_facia_length_count_3x3'),
            cluster_facia_length_3x4 = computed_bom.get('cluster_facia_length_count_3x4'),
            cluster_facia_length_4x4 = computed_bom.get('cluster_facia_length_count_4x4'),

            cluster_facia_width_2x2 = computed_bom.get('cluster_facia_width_count_2x2'),
            cluster_facia_width_2x3 = computed_bom.get('cluster_facia_width_count_2x3'),
            cluster_facia_width_3x3 = computed_bom.get('cluster_facia_width_count_3x3'),
            cluster_facia_width_3x4 = computed_bom.get('cluster_facia_width_count_3x4'),
            cluster_facia_width_4x4 = computed_bom.get('cluster_facia_width_count_4x4'),

            cluster_corner_length_beam_2x2 = computed_bom.get('cluster_corner_length_beam_count_2x2'),
            cluster_corner_length_beam_2x3 = computed_bom.get('cluster_corner_length_beam_count_2x3'),
            cluster_corner_length_beam_3x3 = computed_bom.get('cluster_corner_length_beam_count_3x3'),
            cluster_corner_length_beam_3x4 = computed_bom.get('cluster_corner_length_beam_count_3x4'),
            cluster_corner_length_beam_4x4 = computed_bom.get('cluster_corner_length_beam_count_4x4'),

            cluster_corner_width_beam_2x2 = computed_bom.get('cluster_corner_width_beam_count_2x2'),
            cluster_corner_width_beam_2x3 = computed_bom.get('cluster_corner_width_beam_count_2x3'),
            cluster_corner_width_beam_3x3 = computed_bom.get('cluster_corner_width_beam_count_3x3'),
            cluster_corner_width_beam_3x4 = computed_bom.get('cluster_corner_width_beam_count_3x4'),
            cluster_corner_width_beam_4x4 = computed_bom.get('cluster_corner_width_beam_count_4x4'),

            # Perimeter
            perimeter_post_2x2 = computed_bom.get('perimeter_post_count_2x2'),
            perimeter_post_2x3 = computed_bom.get('perimeter_post_count_2x3'),
            perimeter_post_3x3 = computed_bom.get('perimeter_post_count_3x3'),

            perimeter_panel_2x2 = computed_bom.get('perimeter_panel_count_2x2'),
            perimeter_panel_2x3 = computed_bom.get('perimeter_panel_count_2x3'),
            perimeter_panel_3x3 = computed_bom.get('perimeter_panel_count_3x3'),

            perimeter_beam_2x2 = computed_bom.get('perimeter_beam_count_2x2'),
            perimeter_beam_2x3 = computed_bom.get('perimeter_beam_count_2x3'),
            perimeter_beam_3x3 = computed_bom.get('perimeter_beam_count_3x3'),

            perimeter_facia_length_2x2 = computed_bom.get('perimeter_facia_length_count_2x2'),
            perimeter_facia_length_2x3 = computed_bom.get('perimeter_facia_length_count_2x3'),
            perimeter_facia_length_3x3 = computed_bom.get('perimeter_facia_length_count_3x3'),

            perimeter_facia_width_2x2 = computed_bom.get('perimeter_facia_width_count_2x2'),
            perimeter_facia_width_2x3 = computed_bom.get('perimeter_facia_width_count_2x3'),
            perimeter_facia_width_3x3 = computed_bom.get('perimeter_facia_width_count_3x3'),

            perimeter_corner_length_beam_2x2 = computed_bom.get('perimeter_corner_length_beam_count_2x2'),
            perimeter_corner_length_beam_2x3 = computed_bom.get('perimeter_corner_length_beam_count_2x3'),
            perimeter_corner_length_beam_3x3 = computed_bom.get('perimeter_corner_length_beam_count_3x3'),

            perimeter_corner_width_beam_2x2 = computed_bom.get('perimeter_corner_width_beam_count_2x2'),
            perimeter_corner_width_beam_2x3 = computed_bom.get('perimeter_corner_width_beam_count_2x3'),
            perimeter_corner_width_beam_3x3 = computed_bom.get('perimeter_corner_width_beam_count_3x3'),
            
            total_posts = computed_bom.get('total_posts'),
            total_panels = computed_bom.get('total_panels'),
            total_beams = computed_bom.get('total_beams'),
            total_facia_lengths = computed_bom.get('total_facia_lengths'),
            total_facia_widths = computed_bom.get('total_facia_widths'),
            total_corner_length_beams = computed_bom.get('total_corner_length_beams'),
            total_corner_width_beams = computed_bom.get('total_corner_width_beams'),

            job=self
        )
        print('Successfully created BOM')

    def compute_bom(self, instance: Self) -> dict:
        # Define cluster base
        cluster_post_count_base_2x2 = 13
        cluster_post_count_base_2x3 = 15
        cluster_post_count_base_3x3 = 17
        cluster_post_count_base_3x4 = 19
        cluster_post_count_base_4x4 = 21

        cluster_panel_count_base_2x2 = 8
        cluster_panel_count_base_2x3 = 10
        cluster_panel_count_base_3x3 = 12
        cluster_panel_count_base_3x4 = 14
        cluster_panel_count_base_4x4 = 16

        cluster_beam_count_base_2x2 = 16
        cluster_beam_count_base_2x3 = 20
        cluster_beam_count_base_3x3 = 24
        cluster_beam_count_base_3x4 = 28
        cluster_beam_count_base_4x4 = 32

        cluster_facial_length_count_base = 4
        cluster_facial_width_count_base = 4
        cluster_corner_length_beam_count_base = 8
        cluster_corner_width_beam_count_base = 8

        contingency_factor = 1 + (instance.contingency / 100)

        # Compute for Cluster 2 x 2 ============================================================================
        cluster_post_count_beyond_min_booth_count_2x2 = {
            6: 19,
            8: 25,
            10: 31,
            12: 37
        }

        cluster_panel_count_beyond_min_booth_count_2x2 = {
            6: 14,
            8: 20,
            10: 26,
            12: 32
        }
        
        cluster_booth_count_2x2 = int(instance.cluster_booth_count_2x2)
        if cluster_booth_count_2x2 == 0:
            cluster_post_count_2x2 = 0
            cluster_panel_count_2x2 = 0
            cluster_beam_count_2x2 = 0
            cluster_facia_length_count_2x2 = 0
            cluster_facia_width_count_2x2 = 0
            cluster_corner_length_beam_count_2x2 = 0
            cluster_corner_width_beam_count_2x2 = 0
        elif cluster_booth_count_2x2 == 4:
            cluster_post_count_2x2 = cluster_post_count_base_2x2
            cluster_panel_count_2x2 = cluster_panel_count_base_2x2
            cluster_beam_count_2x2 = cluster_beam_count_base_2x2
            cluster_facia_length_count_2x2 = cluster_facial_length_count_base
            cluster_facia_width_count_2x2 = cluster_facial_width_count_base
            cluster_corner_length_beam_count_2x2 = cluster_corner_length_beam_count_base
            cluster_corner_width_beam_count_2x2 = cluster_corner_width_beam_count_base
        else:
            cluster_post_count_2x2 = cluster_post_count_beyond_min_booth_count_2x2[cluster_booth_count_2x2]
            cluster_panel_count_2x2 = cluster_panel_count_beyond_min_booth_count_2x2[cluster_booth_count_2x2]
            cluster_beam_count_2x2 = cluster_panel_count_2x2 * 2
            cluster_facia_length_count_2x2 = cluster_booth_count_2x2
            cluster_facia_width_count_2x2 = 4
            cluster_corner_length_beam_count_2x2 = cluster_facia_length_count_2x2 * 2
            cluster_corner_width_beam_count_2x2 = cluster_facia_width_count_2x2 * 2

        if cluster_booth_count_2x2 != 0 and instance.cluster_total_count_2x2 != 0:
            cluster_post_count_2x2 = math.ceil(cluster_post_count_2x2 * contingency_factor) * instance.cluster_total_count_2x2
            cluster_panel_count_2x2 = math.ceil(cluster_panel_count_2x2 * contingency_factor) * instance.cluster_total_count_2x2
            cluster_beam_count_2x2 = math.ceil(cluster_beam_count_2x2 * contingency_factor) * instance.cluster_total_count_2x2
            cluster_facia_length_count_2x2 = math.ceil(cluster_facia_length_count_2x2 * contingency_factor) * instance.cluster_total_count_2x2
            cluster_facia_width_count_2x2 = math.ceil(cluster_facia_width_count_2x2 * contingency_factor) * instance.cluster_total_count_2x2
            cluster_corner_length_beam_count_2x2 = math.ceil(cluster_corner_length_beam_count_2x2 * contingency_factor) * instance.cluster_total_count_2x2
            cluster_corner_width_beam_count_2x2 = math.ceil(cluster_corner_width_beam_count_2x2 * contingency_factor) * instance.cluster_total_count_2x2
        # End of compute for Cluster 2 x 2 ============================================================================

        
        # Compute for Cluster 2 x 3 ============================================================================
        cluster_post_count_beyond_min_booth_count_2x3 = {
            6: 22,
            8: 29,
            10: 36,
            12: 43
        }

        cluster_panel_count_beyond_min_booth_count_2x3 = {
            6: 17,
            8: 24,
            10: 31,
            12: 38
        }
        
        cluster_booth_count_2x3 = int(instance.cluster_booth_count_2x3)
        if cluster_booth_count_2x3 == 0:
            cluster_post_count_2x3 = 0
            cluster_panel_count_2x3 = 0
            cluster_beam_count_2x3 = 0
            cluster_facia_length_count_2x3 = 0
            cluster_facia_width_count_2x3 = 0
            cluster_corner_length_beam_count_2x3 = 0
            cluster_corner_width_beam_count_2x3 = 0
        elif cluster_booth_count_2x3 == 4:
            cluster_post_count_2x3 = cluster_post_count_base_2x3
            cluster_panel_count_2x3 = cluster_panel_count_base_2x3
            cluster_beam_count_2x3 = cluster_beam_count_base_2x3
            cluster_facia_length_count_2x3 = cluster_facial_length_count_base
            cluster_facia_width_count_2x3 = cluster_facial_width_count_base
            cluster_corner_length_beam_count_2x3 = cluster_corner_length_beam_count_base
            cluster_corner_width_beam_count_2x3 = cluster_corner_width_beam_count_base
        else:
            cluster_post_count_2x3 = cluster_post_count_beyond_min_booth_count_2x3[cluster_booth_count_2x3]
            cluster_panel_count_2x3 = cluster_panel_count_beyond_min_booth_count_2x3[cluster_booth_count_2x3]
            cluster_beam_count_2x3 = cluster_panel_count_2x3 * 2
            cluster_facia_length_count_2x3 = cluster_booth_count_2x3
            cluster_facia_width_count_2x3 = 4
            cluster_corner_length_beam_count_2x3 = cluster_facia_length_count_2x3 * 2
            cluster_corner_width_beam_count_2x3 = cluster_facia_width_count_2x3 * 2

        if cluster_booth_count_2x3 != 0 and instance.cluster_total_count_2x3 != 0:
            cluster_post_count_2x3 = math.ceil(cluster_post_count_2x3 * contingency_factor) * instance.cluster_total_count_2x3
            cluster_panel_count_2x3 = math.ceil(cluster_panel_count_2x3 * contingency_factor) * instance.cluster_total_count_2x3
            cluster_beam_count_2x3 = math.ceil(cluster_beam_count_2x3 * contingency_factor) * instance.cluster_total_count_2x3
            cluster_facia_length_count_2x3 = math.ceil(cluster_facia_length_count_2x3 * contingency_factor) * instance.cluster_total_count_2x3
            cluster_facia_width_count_2x3 = math.ceil(cluster_facia_width_count_2x3 * contingency_factor) * instance.cluster_total_count_2x3
            cluster_corner_length_beam_count_2x3 = math.ceil(cluster_corner_length_beam_count_2x3 * contingency_factor) * instance.cluster_total_count_2x3
            cluster_corner_width_beam_count_2x3 = math.ceil(cluster_corner_width_beam_count_2x3 * contingency_factor) * instance.cluster_total_count_2x3
        # End of compute for Cluster 2 x 3 ============================================================================

        
        # Compute for Cluster 3 x 3 ============================================================================
        cluster_post_count_beyond_min_booth_count_3x3 = {
            6: 26,
            8: 35,
            10: 44,
            12: 53
        }

        cluster_panel_count_beyond_min_booth_count_3x3 = {
            6: 21,
            8: 30,
            10: 39,
            12: 48
        }
        
        cluster_booth_count_3x3 = int(instance.cluster_booth_count_3x3)
        if cluster_booth_count_3x3 == 0:
            cluster_post_count_3x3 = 0
            cluster_panel_count_3x3 = 0
            cluster_beam_count_3x3 = 0
            cluster_facia_length_count_3x3 = 0
            cluster_facia_width_count_3x3 = 0
            cluster_corner_length_beam_count_3x3 = 0
            cluster_corner_width_beam_count_3x3 = 0
        elif cluster_booth_count_3x3 == 4:
            cluster_post_count_3x3 = cluster_post_count_base_3x3
            cluster_panel_count_3x3 = cluster_panel_count_base_3x3
            cluster_beam_count_3x3 = cluster_beam_count_base_3x3
            cluster_facia_length_count_3x3 = cluster_facial_length_count_base
            cluster_facia_width_count_3x3 = cluster_facial_width_count_base
            cluster_corner_length_beam_count_3x3 = cluster_corner_length_beam_count_base
            cluster_corner_width_beam_count_3x3 = cluster_corner_width_beam_count_base
        else:
            cluster_post_count_3x3 = cluster_post_count_beyond_min_booth_count_3x3[cluster_booth_count_3x3]
            cluster_panel_count_3x3 = cluster_panel_count_beyond_min_booth_count_3x3[cluster_booth_count_3x3]
            cluster_beam_count_3x3 = cluster_panel_count_3x3 * 2
            cluster_facia_length_count_3x3 = cluster_booth_count_3x3
            cluster_facia_width_count_3x3 = 4
            cluster_corner_length_beam_count_3x3 = cluster_facia_length_count_3x3 * 2
            cluster_corner_width_beam_count_3x3 = cluster_facia_width_count_3x3 * 2

        if cluster_booth_count_3x3 != 0 and instance.cluster_total_count_3x3 != 0:
            cluster_post_count_3x3 = math.ceil(cluster_post_count_3x3 * contingency_factor) * instance.cluster_total_count_3x3
            cluster_panel_count_3x3 = math.ceil(cluster_panel_count_3x3 * contingency_factor) * instance.cluster_total_count_3x3
            cluster_beam_count_3x3 = math.ceil(cluster_beam_count_3x3 * contingency_factor) * instance.cluster_total_count_3x3
            cluster_facia_length_count_3x3 = math.ceil(cluster_facia_length_count_3x3 * contingency_factor) * instance.cluster_total_count_3x3
            cluster_facia_width_count_3x3 = math.ceil(cluster_facia_width_count_3x3 * contingency_factor) * instance.cluster_total_count_3x3
            cluster_corner_length_beam_count_3x3 = math.ceil(cluster_corner_length_beam_count_3x3 * contingency_factor) * instance.cluster_total_count_3x3
            cluster_corner_width_beam_count_3x3 = math.ceil(cluster_corner_width_beam_count_3x3 * contingency_factor) * instance.cluster_total_count_3x3
        # End of compute for Cluster 3 x 3 ============================================================================

        
        # Compute for Cluster 3 x 4 ============================================================================
        cluster_post_count_beyond_min_booth_count_3x4 = {
            6: 29,
            8: 39,
            10: 49,
            12: 59
        }

        cluster_panel_count_beyond_min_booth_count_3x4 = {
            6: 24,
            8: 34,
            10: 44,
            12: 54
        }
        
        cluster_booth_count_3x4 = int(instance.cluster_booth_count_3x4)
        if cluster_booth_count_3x4 == 0:
            cluster_post_count_3x4 = 0
            cluster_panel_count_3x4 = 0
            cluster_beam_count_3x4 = 0
            cluster_facia_length_count_3x4 = 0
            cluster_facia_width_count_3x4 = 0
            cluster_corner_length_beam_count_3x4 = 0
            cluster_corner_width_beam_count_3x4 = 0
        elif cluster_booth_count_3x4 == 4:
            cluster_post_count_3x4 = cluster_post_count_base_3x4
            cluster_panel_count_3x4 = cluster_panel_count_base_3x4
            cluster_beam_count_3x4 = cluster_beam_count_base_3x4
            cluster_facia_length_count_3x4 = cluster_facial_length_count_base
            cluster_facia_width_count_3x4 = cluster_facial_width_count_base
            cluster_corner_length_beam_count_3x4 = cluster_corner_length_beam_count_base
            cluster_corner_width_beam_count_3x4 = cluster_corner_width_beam_count_base
        else:
            cluster_post_count_3x4 = cluster_post_count_beyond_min_booth_count_3x4[cluster_booth_count_3x4]
            cluster_panel_count_3x4 = cluster_panel_count_beyond_min_booth_count_3x4[cluster_booth_count_3x4]
            cluster_beam_count_3x4 = cluster_panel_count_3x4 * 2
            cluster_facia_length_count_3x4 = cluster_booth_count_3x4
            cluster_facia_width_count_3x4 = 4
            cluster_corner_length_beam_count_3x4 = cluster_facia_length_count_3x4 * 2
            cluster_corner_width_beam_count_3x4 = cluster_facia_width_count_3x4 * 2

        if cluster_booth_count_3x4 != 0 and instance.cluster_total_count_3x4 != 0:
            cluster_post_count_3x4 = math.ceil(cluster_post_count_3x4 * contingency_factor) * instance.cluster_total_count_3x4
            cluster_panel_count_3x4 = math.ceil(cluster_panel_count_3x4 * contingency_factor) * instance.cluster_total_count_3x4
            cluster_beam_count_3x4 = math.ceil(cluster_beam_count_3x4 * contingency_factor) * instance.cluster_total_count_3x4
            cluster_facia_length_count_3x4 = math.ceil(cluster_facia_length_count_3x4 * contingency_factor) * instance.cluster_total_count_3x4
            cluster_facia_width_count_3x4 = math.ceil(cluster_facia_width_count_3x4 * contingency_factor) * instance.cluster_total_count_3x4
            cluster_corner_length_beam_count_3x4 = math.ceil(cluster_corner_length_beam_count_3x4 * contingency_factor) * instance.cluster_total_count_3x4
            cluster_corner_width_beam_count_3x4 = math.ceil(cluster_corner_width_beam_count_3x4 * contingency_factor) * instance.cluster_total_count_3x4
        # End of compute for Cluster 3 x 4 ============================================================================

        
        # Compute for Cluster 4 x 4 ============================================================================
        cluster_post_count_beyond_min_booth_count_4x4 = {
            6: 33,
            8: 45,
            10: 57,
            12: 69
        }

        cluster_panel_count_beyond_min_booth_count_4x4 = {
            6: 28,
            8: 40,
            10: 52,
            12: 64
        }
        
        cluster_booth_count_4x4 = int(instance.cluster_booth_count_4x4)
        if cluster_booth_count_4x4 == 0:
            cluster_post_count_4x4 = 0
            cluster_panel_count_4x4 = 0
            cluster_beam_count_4x4 = 0
            cluster_facia_length_count_4x4 = 0
            cluster_facia_width_count_4x4 = 0
            cluster_corner_length_beam_count_4x4 = 0
            cluster_corner_width_beam_count_4x4 = 0
        elif cluster_booth_count_4x4 == 4:
            cluster_post_count_4x4 = cluster_post_count_base_4x4
            cluster_panel_count_4x4 = cluster_panel_count_base_4x4
            cluster_beam_count_4x4 = cluster_beam_count_base_4x4
            cluster_facia_length_count_4x4 = cluster_facial_length_count_base
            cluster_facia_width_count_4x4 = cluster_facial_width_count_base
            cluster_corner_length_beam_count_4x4 = cluster_corner_length_beam_count_base
            cluster_corner_width_beam_count_4x4 = cluster_corner_width_beam_count_base
        else:
            cluster_post_count_4x4 = cluster_post_count_beyond_min_booth_count_4x4[cluster_booth_count_4x4]
            cluster_panel_count_4x4 = cluster_panel_count_beyond_min_booth_count_4x4[cluster_booth_count_4x4]
            cluster_beam_count_4x4 = cluster_panel_count_4x4 * 2
            cluster_facia_length_count_4x4 = cluster_booth_count_4x4
            cluster_facia_width_count_4x4 = 4
            cluster_corner_length_beam_count_4x4 = cluster_facia_length_count_4x4 * 2
            cluster_corner_width_beam_count_4x4 = cluster_facia_width_count_4x4 * 2

        if cluster_booth_count_4x4 != 0 and instance.cluster_total_count_4x4 != 0:
            cluster_post_count_4x4 = math.ceil(cluster_post_count_4x4 * contingency_factor) * instance.cluster_total_count_4x4
            cluster_panel_count_4x4 = math.ceil(cluster_panel_count_4x4 * contingency_factor) * instance.cluster_total_count_4x4
            cluster_beam_count_4x4 = math.ceil(cluster_beam_count_4x4 * contingency_factor) * instance.cluster_total_count_4x4
            cluster_facia_length_count_4x4 = math.ceil(cluster_facia_length_count_4x4 * contingency_factor) * instance.cluster_total_count_4x4
            cluster_facia_width_count_4x4 = math.ceil(cluster_facia_width_count_4x4 * contingency_factor) * instance.cluster_total_count_4x4
            cluster_corner_length_beam_count_4x4 = math.ceil(cluster_corner_length_beam_count_4x4 * contingency_factor) * instance.cluster_total_count_4x4
            cluster_corner_width_beam_count_4x4 = math.ceil(cluster_corner_width_beam_count_4x4 * contingency_factor) * instance.cluster_total_count_4x4
        # End of compute for Cluster 4 x 4 ============================================================================

        # Define perimeter base
        perimeter_post_count_base_2x2 = 13
        perimeter_post_count_base_2x3 = 16
        perimeter_post_count_base_3x3 = 18

        perimeter_panel_count_base_2x2 = 10
        perimeter_panel_count_base_2x3 = 13
        perimeter_panel_count_base_3x3 = 15

        perimeter_beam_count_base_2x2 = 20
        perimeter_beam_count_base_2x3 = 26
        perimeter_beam_count_base_3x3 = 30

        perimeter_facial_length_count_base = 3
        perimeter_facial_width_count_base = 2
        perimeter_corner_length_beam_count_base = 6
        perimeter_corner_width_beam_count_base = 4

        
        # Compute for Perimeter 2 x 2 ============================================================================
        perimeter_post_count_beyond_min_booth_count_2x2 = {
            4: 17,
            5: 21,
            6: 25,
            7: 29,
            8: 33,
            9: 37,
            10: 41,
            11: 45,
            12: 49,
            13: 53,
            14: 57,
            15: 61,
            16: 65,
            17: 69,
            18: 73,
            19: 77,
            20: 81
        }

        perimeter_panel_count_beyond_min_booth_count_2x2 = {
            4: 14,
            5: 18,
            6: 22,
            7: 26,
            8: 30,
            9: 34,
            10: 38,
            11: 42,
            12: 46,
            13: 50,
            14: 54,
            15: 58,
            16: 62,
            17: 66,
            18: 70,
            19: 74,
            20: 78
        }
        
        perimeter_booth_count_2x2 = int(instance.perimeter_booth_count_2x2)
        if perimeter_booth_count_2x2 == 0:
            perimeter_post_count_2x2 = 0
            perimeter_panel_count_2x2 = 0
            perimeter_beam_count_2x2 = 0
            perimeter_facia_length_count_2x2 = 0
            perimeter_facia_width_count_2x2 = 0
            perimeter_corner_length_beam_count_2x2 = 0
            perimeter_corner_width_beam_count_2x2 = 0
        elif perimeter_booth_count_2x2 == 3:
            perimeter_post_count_2x2 = perimeter_post_count_base_2x2
            perimeter_panel_count_2x2 = perimeter_panel_count_base_2x2
            perimeter_beam_count_2x2 = perimeter_beam_count_base_2x2
            perimeter_facia_length_count_2x2 = perimeter_facial_length_count_base
            perimeter_facia_width_count_2x2 = perimeter_facial_width_count_base
            perimeter_corner_length_beam_count_2x2 = perimeter_corner_length_beam_count_base
            perimeter_corner_width_beam_count_2x2 = perimeter_corner_width_beam_count_base
        else:
            perimeter_post_count_2x2 = perimeter_post_count_beyond_min_booth_count_2x2[perimeter_booth_count_2x2]
            perimeter_panel_count_2x2 = perimeter_panel_count_beyond_min_booth_count_2x2[perimeter_booth_count_2x2]
            perimeter_beam_count_2x2 = perimeter_panel_count_2x2 * 2
            perimeter_facia_length_count_2x2 = perimeter_booth_count_2x2
            perimeter_facia_width_count_2x2 = 2
            perimeter_corner_length_beam_count_2x2 = perimeter_facia_length_count_2x2 * 2
            perimeter_corner_width_beam_count_2x2 = perimeter_facia_width_count_2x2 * 2

        if perimeter_booth_count_2x2 != 0 and instance.perimeter_total_count_2x2 != 0:
            perimeter_post_count_2x2 = math.ceil(perimeter_post_count_2x2 * contingency_factor) * instance.perimeter_total_count_2x2
            perimeter_panel_count_2x2 = math.ceil(perimeter_panel_count_2x2 * contingency_factor) * instance.perimeter_total_count_2x2
            perimeter_beam_count_2x2 = math.ceil(perimeter_beam_count_2x2 * contingency_factor) * instance.perimeter_total_count_2x2
            perimeter_facia_length_count_2x2 = math.ceil(perimeter_facia_length_count_2x2 * contingency_factor) * instance.perimeter_total_count_2x2
            perimeter_facia_width_count_2x2 = math.ceil(perimeter_facia_width_count_2x2 * contingency_factor) * instance.perimeter_total_count_2x2
            perimeter_corner_length_beam_count_2x2 = math.ceil(perimeter_corner_length_beam_count_2x2 * contingency_factor) * instance.perimeter_total_count_2x2
            perimeter_corner_width_beam_count_2x2 = math.ceil(perimeter_corner_width_beam_count_2x2 * contingency_factor) * instance.perimeter_total_count_2x2
        # End of compute for Perimeter 2 x 2 ============================================================================

        
        # Compute for Perimeter 2 x 3 ============================================================================
        perimeter_post_count_beyond_min_booth_count_2x3 = {
            4: 21,
            5: 26,
            6: 31,
            7: 36,
            8: 41,
            9: 46,
            10: 51,
            11: 56,
            12: 61,
            13: 66,
            14: 71,
            15: 76,
            16: 81,
            17: 86,
            18: 91,
            19: 96,
            20: 101
        }

        perimeter_panel_count_beyond_min_booth_count_2x3 = {
            4: 18,
            5: 23,
            6: 28,
            7: 33,
            8: 38,
            9: 43,
            10: 48,
            11: 53,
            12: 58,
            13: 63,
            14: 68,
            15: 73,
            16: 78,
            17: 83,
            18: 88,
            19: 93,
            20: 98
        }
        
        perimeter_booth_count_2x3 = int(instance.perimeter_booth_count_2x3)
        if perimeter_booth_count_2x3 == 0:
            perimeter_post_count_2x3 = 0
            perimeter_panel_count_2x3 = 0
            perimeter_beam_count_2x3 = 0
            perimeter_facia_length_count_2x3 = 0
            perimeter_facia_width_count_2x3 = 0
            perimeter_corner_length_beam_count_2x3 = 0
            perimeter_corner_width_beam_count_2x3 = 0
        elif perimeter_booth_count_2x3 == 3:
            perimeter_post_count_2x3 = perimeter_post_count_base_2x3
            perimeter_panel_count_2x3 = perimeter_panel_count_base_2x3
            perimeter_beam_count_2x3 = perimeter_beam_count_base_2x3
            perimeter_facia_length_count_2x3 = perimeter_facial_length_count_base
            perimeter_facia_width_count_2x3 = perimeter_facial_width_count_base
            perimeter_corner_length_beam_count_2x3 = perimeter_corner_length_beam_count_base
            perimeter_corner_width_beam_count_2x3 = perimeter_corner_width_beam_count_base
        else:
            perimeter_post_count_2x3 = perimeter_post_count_beyond_min_booth_count_2x3[perimeter_booth_count_2x3]
            perimeter_panel_count_2x3 = perimeter_panel_count_beyond_min_booth_count_2x3[perimeter_booth_count_2x3]
            perimeter_beam_count_2x3 = perimeter_panel_count_2x3 * 2
            perimeter_facia_length_count_2x3 = perimeter_booth_count_2x3
            perimeter_facia_width_count_2x3 = 2
            perimeter_corner_length_beam_count_2x3 = perimeter_facia_length_count_2x3 * 2
            perimeter_corner_width_beam_count_2x3 = perimeter_facia_width_count_2x3 * 2

        if perimeter_booth_count_2x3 != 0 and instance.perimeter_total_count_2x3 != 0:
            perimeter_post_count_2x3 = math.ceil(perimeter_post_count_2x3 * contingency_factor) * instance.perimeter_total_count_2x3
            perimeter_panel_count_2x3 = math.ceil(perimeter_panel_count_2x3 * contingency_factor) * instance.perimeter_total_count_2x3
            perimeter_beam_count_2x3 = math.ceil(perimeter_beam_count_2x3 * contingency_factor) * instance.perimeter_total_count_2x3
            perimeter_facia_length_count_2x3 = math.ceil(perimeter_facia_length_count_2x3 * contingency_factor) * instance.perimeter_total_count_2x3
            perimeter_facia_width_count_2x3 = math.ceil(perimeter_facia_width_count_2x3 * contingency_factor) * instance.perimeter_total_count_2x3
            perimeter_corner_length_beam_count_2x3 = math.ceil(perimeter_corner_length_beam_count_2x3 * contingency_factor) * instance.perimeter_total_count_2x3
            perimeter_corner_width_beam_count_2x3 = math.ceil(perimeter_corner_width_beam_count_2x3 * contingency_factor) * instance.perimeter_total_count_2x3
        # End of compute for Perimeter 2 x 3 ============================================================================

        
        # Compute for Perimeter 3 x 3 ============================================================================
        perimeter_post_count_beyond_min_booth_count_3x3 = {
            4: 24,
            5: 30,
            6: 36,
            7: 42,
            8: 48,
            9: 54,
            10: 60,
            11: 66,
            12: 72,
            13: 78,
            14: 84,
            15: 90,
            16: 96,
            17: 102,
            18: 108,
            19: 114,
            20: 120
        }

        perimeter_panel_count_beyond_min_booth_count_3x3 = {
            4: 21,
            5: 27,
            6: 33,
            7: 39,
            8: 45,
            9: 51,
            10: 57,
            11: 63,
            12: 69,
            13: 75,
            14: 81,
            15: 87,
            16: 93,
            17: 99,
            18: 105,
            19: 111,
            20: 117
        }
        
        perimeter_booth_count_3x3 = int(instance.perimeter_booth_count_3x3)
        if perimeter_booth_count_3x3 == 0:
            perimeter_post_count_3x3 = 0
            perimeter_panel_count_3x3 = 0
            perimeter_beam_count_3x3 = 0
            perimeter_facia_length_count_3x3 = 0
            perimeter_facia_width_count_3x3 = 0
            perimeter_corner_length_beam_count_3x3 = 0
            perimeter_corner_width_beam_count_3x3 = 0
        elif perimeter_booth_count_3x3 == 3:
            perimeter_post_count_3x3 = perimeter_post_count_base_3x3
            perimeter_panel_count_3x3 = perimeter_panel_count_base_3x3
            perimeter_beam_count_3x3 = perimeter_beam_count_base_3x3
            perimeter_facia_length_count_3x3 = perimeter_facial_length_count_base
            perimeter_facia_width_count_3x3 = perimeter_facial_width_count_base
            perimeter_corner_length_beam_count_3x3 = perimeter_corner_length_beam_count_base
            perimeter_corner_width_beam_count_3x3 = perimeter_corner_width_beam_count_base
        else:
            perimeter_post_count_3x3 = perimeter_post_count_beyond_min_booth_count_3x3[perimeter_booth_count_3x3]
            perimeter_panel_count_3x3 = perimeter_panel_count_beyond_min_booth_count_3x3[perimeter_booth_count_3x3]
            perimeter_beam_count_3x3 = perimeter_panel_count_3x3 * 2
            perimeter_facia_length_count_3x3 = perimeter_booth_count_3x3
            perimeter_facia_width_count_3x3 = 2
            perimeter_corner_length_beam_count_3x3 = perimeter_facia_length_count_3x3 * 2
            perimeter_corner_width_beam_count_3x3 = perimeter_facia_width_count_3x3 * 2

        if perimeter_booth_count_3x3 != 0 and instance.perimeter_total_count_3x3 != 0:
            perimeter_post_count_3x3 = math.ceil(perimeter_post_count_3x3 * contingency_factor) * instance.perimeter_total_count_3x3
            perimeter_panel_count_3x3 = math.ceil(perimeter_panel_count_3x3 * contingency_factor) * instance.perimeter_total_count_3x3
            perimeter_beam_count_3x3 = math.ceil(perimeter_beam_count_3x3 * contingency_factor) * instance.perimeter_total_count_3x3
            perimeter_facia_length_count_3x3 = math.ceil(perimeter_facia_length_count_3x3 * contingency_factor) * instance.perimeter_total_count_3x3
            perimeter_facia_width_count_3x3 = math.ceil(perimeter_facia_width_count_3x3 * contingency_factor) * instance.perimeter_total_count_3x3
            perimeter_corner_length_beam_count_3x3 = math.ceil(perimeter_corner_length_beam_count_3x3 * contingency_factor) * instance.perimeter_total_count_3x3
            perimeter_corner_width_beam_count_3x3 = math.ceil(perimeter_corner_width_beam_count_3x3 * contingency_factor) * instance.perimeter_total_count_3x3
        # End of compute for Perimeter 3 x 3 ============================================================================

        total_posts = (
            cluster_post_count_2x2 + 
            cluster_post_count_2x3 +
            cluster_post_count_3x3 +
            cluster_post_count_3x4 +
            cluster_post_count_4x4 +
            perimeter_post_count_2x2 + 
            perimeter_post_count_2x3 + 
            perimeter_post_count_3x3 
        )
        total_panels = (
            cluster_panel_count_2x2 + 
            cluster_panel_count_2x3 +
            cluster_panel_count_3x3 +
            cluster_panel_count_3x4 +
            cluster_panel_count_4x4 +
            perimeter_panel_count_2x2 + 
            perimeter_panel_count_2x3 + 
            perimeter_panel_count_3x3 
        )
        total_beams = (
            cluster_beam_count_2x2 + 
            cluster_beam_count_2x3 +
            cluster_beam_count_3x3 +
            cluster_beam_count_3x4 +
            cluster_beam_count_4x4 +
            perimeter_beam_count_2x2 + 
            perimeter_beam_count_2x3 + 
            perimeter_beam_count_3x3 
        )
        total_facia_lengths = (
            cluster_facia_length_count_2x2 + 
            cluster_facia_length_count_2x3 +
            cluster_facia_length_count_3x3 +
            cluster_facia_length_count_3x4 +
            cluster_facia_length_count_4x4 +
            perimeter_facia_length_count_2x2 + 
            perimeter_facia_length_count_2x3 + 
            perimeter_facia_length_count_3x3 
        )
        total_facia_widths = (
            cluster_facia_width_count_2x2 + 
            cluster_facia_width_count_2x3 +
            cluster_facia_width_count_3x3 +
            cluster_facia_width_count_3x4 +
            cluster_facia_width_count_4x4 +
            perimeter_facia_width_count_2x2 + 
            perimeter_facia_width_count_2x3 + 
            perimeter_facia_width_count_3x3 
        )
        total_corner_length_beams = (
            cluster_corner_length_beam_count_2x2 + 
            cluster_corner_length_beam_count_2x3 +
            cluster_corner_length_beam_count_3x3 +
            cluster_corner_length_beam_count_3x4 +
            cluster_corner_length_beam_count_4x4 +
            perimeter_corner_length_beam_count_2x2 + 
            perimeter_corner_length_beam_count_2x3 + 
            perimeter_corner_length_beam_count_3x3 
        )
        total_corner_width_beams = (
            cluster_corner_width_beam_count_2x2 + 
            cluster_corner_width_beam_count_2x3 +
            cluster_corner_width_beam_count_3x3 +
            cluster_corner_width_beam_count_3x4 +
            cluster_corner_width_beam_count_4x4 +
            perimeter_corner_width_beam_count_2x2 + 
            perimeter_corner_width_beam_count_2x3 + 
            perimeter_corner_width_beam_count_3x3 
        )

        return {
            # Cluster
            'cluster_post_count_2x2': cluster_post_count_2x2,
            'cluster_post_count_2x3': cluster_post_count_2x3,
            'cluster_post_count_3x3': cluster_post_count_3x3,
            'cluster_post_count_3x4': cluster_post_count_3x4,
            'cluster_post_count_4x4': cluster_post_count_4x4,

            'cluster_panel_count_2x2': cluster_panel_count_2x2,
            'cluster_panel_count_2x3': cluster_panel_count_2x3,
            'cluster_panel_count_3x3': cluster_panel_count_3x3,
            'cluster_panel_count_3x4': cluster_panel_count_3x4,
            'cluster_panel_count_4x4': cluster_panel_count_4x4,

            'cluster_beam_count_2x2': cluster_beam_count_2x2,
            'cluster_beam_count_2x3': cluster_beam_count_2x3,
            'cluster_beam_count_3x3': cluster_beam_count_3x3,
            'cluster_beam_count_3x4': cluster_beam_count_3x4,
            'cluster_beam_count_4x4': cluster_beam_count_4x4,

            'cluster_facia_length_count_2x2': cluster_facia_length_count_2x2,
            'cluster_facia_length_count_2x3': cluster_facia_length_count_2x3,
            'cluster_facia_length_count_3x3': cluster_facia_length_count_3x3,
            'cluster_facia_length_count_3x4': cluster_facia_length_count_3x4,
            'cluster_facia_length_count_4x4': cluster_facia_length_count_4x4,

            'cluster_facia_width_count_2x2': cluster_facia_width_count_2x2,
            'cluster_facia_width_count_2x3': cluster_facia_width_count_2x3,
            'cluster_facia_width_count_3x3': cluster_facia_width_count_3x3,
            'cluster_facia_width_count_3x4': cluster_facia_width_count_3x4,
            'cluster_facia_width_count_4x4': cluster_facia_width_count_4x4,

            'cluster_corner_length_beam_count_2x2': cluster_corner_length_beam_count_2x2,
            'cluster_corner_length_beam_count_2x3': cluster_corner_length_beam_count_2x3,
            'cluster_corner_length_beam_count_3x3': cluster_corner_length_beam_count_3x3,
            'cluster_corner_length_beam_count_3x4': cluster_corner_length_beam_count_3x4,
            'cluster_corner_length_beam_count_4x4': cluster_corner_length_beam_count_4x4,

            'cluster_corner_width_beam_count_2x2': cluster_corner_width_beam_count_2x2,
            'cluster_corner_width_beam_count_2x3': cluster_corner_width_beam_count_2x3,
            'cluster_corner_width_beam_count_3x3': cluster_corner_width_beam_count_3x3,
            'cluster_corner_width_beam_count_3x4': cluster_corner_width_beam_count_3x4,
            'cluster_corner_width_beam_count_4x4': cluster_corner_width_beam_count_4x4,

            # Perimeter
            'perimeter_post_count_2x2': perimeter_post_count_2x2,
            'perimeter_post_count_2x3': perimeter_post_count_2x3,
            'perimeter_post_count_3x3': perimeter_post_count_3x3,

            'perimeter_panel_count_2x2': perimeter_panel_count_2x2,
            'perimeter_panel_count_2x3': perimeter_panel_count_2x3,
            'perimeter_panel_count_3x3': perimeter_panel_count_3x3,

            'perimeter_beam_count_2x2': perimeter_beam_count_2x2,
            'perimeter_beam_count_2x3': perimeter_beam_count_2x3,
            'perimeter_beam_count_3x3': perimeter_beam_count_3x3,

            'perimeter_facia_length_count_2x2': perimeter_facia_length_count_2x2,
            'perimeter_facia_length_count_2x3': perimeter_facia_length_count_2x3,
            'perimeter_facia_length_count_3x3': perimeter_facia_length_count_3x3,

            'perimeter_facia_width_count_2x2': perimeter_facia_width_count_2x2,
            'perimeter_facia_width_count_2x3': perimeter_facia_width_count_2x3,
            'perimeter_facia_width_count_3x3': perimeter_facia_width_count_3x3,

            'perimeter_corner_length_beam_count_2x2': perimeter_corner_length_beam_count_2x2,
            'perimeter_corner_length_beam_count_2x3': perimeter_corner_length_beam_count_2x3,
            'perimeter_corner_length_beam_count_3x3': perimeter_corner_length_beam_count_3x3,

            'perimeter_corner_width_beam_count_2x2': perimeter_corner_width_beam_count_2x2,
            'perimeter_corner_width_beam_count_2x3': perimeter_corner_width_beam_count_2x3,
            'perimeter_corner_width_beam_count_3x3': perimeter_corner_width_beam_count_3x3,

            'total_posts': total_posts,
            'total_panels': total_panels,
            'total_beams': total_beams,
            'total_facia_lengths': total_facia_lengths,
            'total_facia_widths': total_facia_widths,
            'total_corner_length_beams': total_corner_length_beams,
            'total_corner_width_beams': total_corner_width_beams
        }

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the Job instance is being created

        computed_bom = self.compute_bom(self)

        super().save(*args, **kwargs)
        BomGeneration = apps.get_model('jobs', 'BomGeneration')

        if created:
            print('First time creating job instance', self.job_id)
            self.create_bom(BomGeneration, computed_bom)
        else:
            print('Job exists and is being edited and saved')
            try:
                existing_bom_generation = BomGeneration.objects.get(job=self)
            except:
                existing_bom_generation = None
                self.create_bom(BomGeneration, computed_bom)

            if existing_bom_generation:
                # Cluster
                existing_bom_generation.cluster_post_2x2 = computed_bom.get('cluster_post_count_2x2')
                existing_bom_generation.cluster_post_2x3 = computed_bom.get('cluster_post_count_2x3')
                existing_bom_generation.cluster_post_3x3 = computed_bom.get('cluster_post_count_3x3')
                existing_bom_generation.cluster_post_3x4 = computed_bom.get('cluster_post_count_3x4')
                existing_bom_generation.cluster_post_4x4 = computed_bom.get('cluster_post_count_4x4')

                existing_bom_generation.cluster_panel_2x2 = computed_bom.get('cluster_panel_count_2x2')
                existing_bom_generation.cluster_panel_2x3 = computed_bom.get('cluster_panel_count_2x3')
                existing_bom_generation.cluster_panel_3x3 = computed_bom.get('cluster_panel_count_3x3')
                existing_bom_generation.cluster_panel_3x4 = computed_bom.get('cluster_panel_count_3x4')
                existing_bom_generation.cluster_panel_4x4 = computed_bom.get('cluster_panel_count_4x4')

                existing_bom_generation.cluster_beam_2x2 = computed_bom.get('cluster_beam_count_2x2')
                existing_bom_generation.cluster_beam_2x3 = computed_bom.get('cluster_beam_count_2x3')
                existing_bom_generation.cluster_beam_3x3 = computed_bom.get('cluster_beam_count_3x3')
                existing_bom_generation.cluster_beam_3x4 = computed_bom.get('cluster_beam_count_3x4')
                existing_bom_generation.cluster_beam_4x4 = computed_bom.get('cluster_beam_count_4x4')

                existing_bom_generation.cluster_facia_length_2x2 = computed_bom.get('cluster_facia_length_count_2x2')
                existing_bom_generation.cluster_facia_length_2x3 = computed_bom.get('cluster_facia_length_count_2x3')
                existing_bom_generation.cluster_facia_length_3x3 = computed_bom.get('cluster_facia_length_count_3x3')
                existing_bom_generation.cluster_facia_length_3x4 = computed_bom.get('cluster_facia_length_count_3x4')
                existing_bom_generation.cluster_facia_length_4x4 = computed_bom.get('cluster_facia_length_count_4x4')

                existing_bom_generation.cluster_facia_width_2x2 = computed_bom.get('cluster_facia_width_count_2x2')
                existing_bom_generation.cluster_facia_width_2x3 = computed_bom.get('cluster_facia_width_count_2x3')
                existing_bom_generation.cluster_facia_width_3x3 = computed_bom.get('cluster_facia_width_count_3x3')
                existing_bom_generation.cluster_facia_width_3x4 = computed_bom.get('cluster_facia_width_count_3x4')
                existing_bom_generation.cluster_facia_width_4x4 = computed_bom.get('cluster_facia_width_count_4x4')

                existing_bom_generation.cluster_corner_length_beam_2x2 = computed_bom.get('cluster_corner_length_beam_count_2x2')
                existing_bom_generation.cluster_corner_length_beam_2x3 = computed_bom.get('cluster_corner_length_beam_count_2x3')
                existing_bom_generation.cluster_corner_length_beam_3x3 = computed_bom.get('cluster_corner_length_beam_count_3x3')
                existing_bom_generation.cluster_corner_length_beam_3x4 = computed_bom.get('cluster_corner_length_beam_count_3x4')
                existing_bom_generation.cluster_corner_length_beam_4x4 = computed_bom.get('cluster_corner_length_beam_count_4x4')

                existing_bom_generation.cluster_corner_width_beam_2x2 = computed_bom.get('cluster_corner_width_beam_count_2x2')
                existing_bom_generation.cluster_corner_width_beam_2x3 = computed_bom.get('cluster_corner_width_beam_count_2x3')
                existing_bom_generation.cluster_corner_width_beam_3x3 = computed_bom.get('cluster_corner_width_beam_count_3x3')
                existing_bom_generation.cluster_corner_width_beam_3x4 = computed_bom.get('cluster_corner_width_beam_count_3x4')
                existing_bom_generation.cluster_corner_width_beam_4x4 = computed_bom.get('cluster_corner_width_beam_count_4x4')

                # Perimeter
                existing_bom_generation.perimeter_post_2x2 = computed_bom.get('perimeter_post_count_2x2')
                existing_bom_generation.perimeter_post_2x3 = computed_bom.get('perimeter_post_count_2x3')
                existing_bom_generation.perimeter_post_3x3 = computed_bom.get('perimeter_post_count_3x3')

                existing_bom_generation.perimeter_panel_2x2 = computed_bom.get('perimeter_panel_count_2x2')
                existing_bom_generation.perimeter_panel_2x3 = computed_bom.get('perimeter_panel_count_2x3')
                existing_bom_generation.perimeter_panel_3x3 = computed_bom.get('perimeter_panel_count_3x3')

                existing_bom_generation.perimeter_beam_2x2 = computed_bom.get('perimeter_beam_count_2x2')
                existing_bom_generation.perimeter_beam_2x3 = computed_bom.get('perimeter_beam_count_2x3')
                existing_bom_generation.perimeter_beam_3x3 = computed_bom.get('perimeter_beam_count_3x3')

                existing_bom_generation.perimeter_facia_length_2x2 = computed_bom.get('perimeter_facia_length_count_2x2')
                existing_bom_generation.perimeter_facia_length_2x3 = computed_bom.get('perimeter_facia_length_count_2x3')
                existing_bom_generation.perimeter_facia_length_3x3 = computed_bom.get('perimeter_facia_length_count_3x3')

                existing_bom_generation.perimeter_facia_width_2x2 = computed_bom.get('perimeter_facia_width_count_2x2')
                existing_bom_generation.perimeter_facia_width_2x3 = computed_bom.get('perimeter_facia_width_count_2x3')
                existing_bom_generation.perimeter_facia_width_3x3 = computed_bom.get('perimeter_facia_width_count_3x3')

                existing_bom_generation.perimeter_corner_length_beam_2x2 = computed_bom.get('perimeter_corner_length_beam_count_2x2')
                existing_bom_generation.perimeter_corner_length_beam_2x3 = computed_bom.get('perimeter_corner_length_beam_count_2x3')
                existing_bom_generation.perimeter_corner_length_beam_3x3 = computed_bom.get('perimeter_corner_length_beam_count_3x3')

                existing_bom_generation.perimeter_corner_width_beam_2x2 = computed_bom.get('perimeter_corner_width_beam_count_2x2')
                existing_bom_generation.perimeter_corner_width_beam_2x3 = computed_bom.get('perimeter_corner_width_beam_count_2x3')
                existing_bom_generation.perimeter_corner_width_beam_3x3 = computed_bom.get('perimeter_corner_width_beam_count_3x3')

                existing_bom_generation.total_posts = computed_bom.get('total_posts')
                existing_bom_generation.total_panels = computed_bom.get('total_panels')
                existing_bom_generation.total_beams = computed_bom.get('total_beams')
                existing_bom_generation.total_facia_lengths = computed_bom.get('total_facia_lengths')
                existing_bom_generation.total_facia_widths = computed_bom.get('total_facia_widths')
                existing_bom_generation.total_corner_length_beams = computed_bom.get('total_corner_length_beams')
                existing_bom_generation.total_corner_width_beams = computed_bom.get('total_corner_width_beams')

                existing_bom_generation.save()

class BomGeneration(models.Model):
    class Meta:
        verbose_name = 'BOM Generation'
        verbose_name_plural = 'BOM Generations'

    job = models.ForeignKey(Job, on_delete=models.PROTECT, editable=False)

    # Cluster
    cluster_post_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    cluster_post_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    cluster_post_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')
    cluster_post_3x4 = models.IntegerField(default=0, editable=False, verbose_name='3 x 4')
    cluster_post_4x4 = models.IntegerField(default=0, editable=False, verbose_name='4 x 4')

    cluster_panel_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    cluster_panel_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    cluster_panel_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')
    cluster_panel_3x4 = models.IntegerField(default=0, editable=False, verbose_name='3 x 4')
    cluster_panel_4x4 = models.IntegerField(default=0, editable=False, verbose_name='4 x 4')

    cluster_beam_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    cluster_beam_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    cluster_beam_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')
    cluster_beam_3x4 = models.IntegerField(default=0, editable=False, verbose_name='3 x 4')
    cluster_beam_4x4 = models.IntegerField(default=0, editable=False, verbose_name='4 x 4')

    cluster_facia_length_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    cluster_facia_length_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    cluster_facia_length_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')
    cluster_facia_length_3x4 = models.IntegerField(default=0, editable=False, verbose_name='3 x 4')
    cluster_facia_length_4x4 = models.IntegerField(default=0, editable=False, verbose_name='4 x 4')

    cluster_facia_width_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    cluster_facia_width_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    cluster_facia_width_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')
    cluster_facia_width_3x4 = models.IntegerField(default=0, editable=False, verbose_name='3 x 4')
    cluster_facia_width_4x4 = models.IntegerField(default=0, editable=False, verbose_name='4 x 4')

    cluster_corner_length_beam_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    cluster_corner_length_beam_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    cluster_corner_length_beam_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')
    cluster_corner_length_beam_3x4 = models.IntegerField(default=0, editable=False, verbose_name='3 x 4')
    cluster_corner_length_beam_4x4 = models.IntegerField(default=0, editable=False, verbose_name='4 x 4')

    cluster_corner_width_beam_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    cluster_corner_width_beam_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    cluster_corner_width_beam_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')
    cluster_corner_width_beam_3x4 = models.IntegerField(default=0, editable=False, verbose_name='3 x 4')
    cluster_corner_width_beam_4x4 = models.IntegerField(default=0, editable=False, verbose_name='4 x 4')

    # Perimeter
    perimeter_post_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    perimeter_post_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    perimeter_post_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')

    perimeter_panel_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    perimeter_panel_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    perimeter_panel_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')

    perimeter_beam_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    perimeter_beam_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    perimeter_beam_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')

    perimeter_facia_length_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    perimeter_facia_length_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    perimeter_facia_length_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')

    perimeter_facia_width_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    perimeter_facia_width_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    perimeter_facia_width_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')

    perimeter_corner_length_beam_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    perimeter_corner_length_beam_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    perimeter_corner_length_beam_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')

    perimeter_corner_width_beam_2x2 = models.IntegerField(default=0, editable=False, verbose_name='2 x 2')
    perimeter_corner_width_beam_2x3 = models.IntegerField(default=0, editable=False, verbose_name='2 x 3')
    perimeter_corner_width_beam_3x3 = models.IntegerField(default=0, editable=False, verbose_name='3 x 3')

    total_posts = models.IntegerField(default=0, editable=False, verbose_name='Total Posts')
    total_panels = models.IntegerField(default=0, editable=False, verbose_name='Total Panels')
    total_beams = models.IntegerField(default=0, editable=False, verbose_name='Total Beams')
    total_facia_lengths = models.IntegerField(default=0, editable=False, verbose_name='Total Facia Lengths')
    total_facia_widths = models.IntegerField(default=0, editable=False, verbose_name='Total Facia Widths')
    total_corner_length_beams = models.IntegerField(default=0, editable=False, verbose_name='Total Corner Length Beams')
    total_corner_width_beams = models.IntegerField(default=0, editable=False, verbose_name='Total Corner Width Beams')

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

