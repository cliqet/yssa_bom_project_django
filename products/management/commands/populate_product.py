from django.core.management import BaseCommand
from products.models import Product
from msdbom.settings import BASE_DIR

import os
import csv


class Command(BaseCommand):
    help = 'Create records from csv with python manage.py populate_product <csv_file_name.csv>'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_name', type=str, help='The csv file name with .csv extension')

    def handle(self, *args, **kwargs):
        csv_file_name = kwargs['csv_file_name']

        with open(os.path.join(BASE_DIR, 'csv_files', csv_file_name), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            for index, row in enumerate(csv_reader):
                # skip the column headers
                if index == 0:
                    continue
                
                try:
                    product = Product.objects.create(
                        setup_type=row[1],
                        name=row[2],
                        description=row[3]
                    )
                    product.save()
                    print(f'Saved record {row[0]} {row[1]}')
                except:
                    print(f'Error creating {row[0]} {row[1]}')
                    continue

        print('Finished populating product table')
