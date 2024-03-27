from django.core.management import BaseCommand
from employees.models import EmployeePosition
from msdbom.settings import BASE_DIR

import os
import csv


class Command(BaseCommand):
    help = 'Create records from csv with python manage.py populate_employee_position <csv_file_name.csv>'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_name', type=str, help='The csv file name with .csv extension')

    def handle(self, *args, **kwargs):
        csv_file_name = kwargs['csv_file_name']

        with open(os.path.join(BASE_DIR, 'csv_files', csv_file_name), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            for row in csv_reader:
                try:
                    employee_position = EmployeePosition.objects.create(
                        employee_position_title=row[1]
                    )
                    employee_position.save()
                    print(f'Saved {row[0]} {row[1]}')
                except:
                    print(f'Error creating {row[0]} {row[1]}')
                    continue

        print('Finished populating employee_position table')

