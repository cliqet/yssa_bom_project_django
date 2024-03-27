from django.core.management import BaseCommand
from clients.models import Client
from msdbom.settings import BASE_DIR

import os
import csv


class Command(BaseCommand):
    help = 'Create records from csv with python manage.py populate_client <csv_file_name.csv>'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_name', type=str, help='The csv file name with .csv extension')

    def handle(self, *args, **kwargs):
        csv_file_name = kwargs['csv_file_name']

        with open(os.path.join(BASE_DIR, 'csv_files', csv_file_name), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            for row in csv_reader:
                try:
                    client = Client.objects.create(
                        company_name=row[1],
                        contact_person=row[2],
                        contact_no=row[3],
                        email_address=row[4]
                    )
                    client.save()
                    print(f'Saved record {row[0]} {row[1]}')
                except:
                    print(f'Error creating {row[0]} {row[1]}')
                    continue

        print('Finished populating client table')
