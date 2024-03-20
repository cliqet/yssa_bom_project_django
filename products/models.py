from django.db import models

SETUP_TYPES = (
    ('Cluster', 'Cluster'),
    ('Perimeter', 'Perimeter'),
)

PRODUCT_NAMES = (
    ('Cluster 2x2 meters', 'Cluster 2x2 meters'),
    ('Cluster 2x3 meters', 'Cluster 2x3 meters'),
    ('Cluster 3x3 meters', 'Cluster 3x3 meters'),
    ('Cluster 3x4 meters', 'Cluster 3x4 meters'),
    ('Cluster 4x4 meters', 'Cluster 4x4 meters'),
    ('Perimeter 2x2 meters', 'Perimeter 2x2 meters'),
    ('Perimeter 2x3 meters', 'Perimeter 2x3 meters'),
    ('Perimeter 3x3 meters', 'Perimeter 3x3 meters'),
)

class Product(models.Model):
    class Meta:
       unique_together = ('setup_type', 'name')
    setup_type = models.CharField(max_length=255, choices=SETUP_TYPES)
    name = models.CharField(max_length=255, choices=PRODUCT_NAMES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'ID: {self.pk} - {self.setup_type} {self.name}'