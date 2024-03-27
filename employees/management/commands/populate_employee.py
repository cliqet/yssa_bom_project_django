from django.core.management import BaseCommand
from employees.models import Employee, Department, EmployeePosition
from msdbom.settings import BASE_DIR, config

import os
import csv


class Command(BaseCommand):
    help = 'Create records from csv with python manage.py populate_employee <csv_file_name.csv>'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_name', type=str, help='The csv file name with .csv extension')

    def handle(self, *args, **kwargs):
        csv_file_name = kwargs['csv_file_name']

        with open(os.path.join(BASE_DIR, 'csv_files', csv_file_name), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            foreign_key_errors = []

            for index, row in enumerate(csv_reader):
                # skip the column headers
                if index == 0:
                    continue

                department = None
                if row[4] != '':
                    try:
                        department = Department.objects.get(department_name=row[4])
                    except:
                        foreign_key_errors.append(f'{row[4]} does not exist in department table for employee email {row[1]}')

                employee_position = None
                if row[5] != '':
                    try:
                        employee_position = EmployeePosition.objects.get(employee_position_title=row[5])
                    except:
                        foreign_key_errors.append(f'{row[5]} does not exist in employee position table for employee email {row[1]}')


                try:
                    employee = Employee.objects.create(
                        email=row[1],
                        first_name=row[2],
                        last_name=row[3],
                        department=department,
                        employee_position=employee_position,
                        contact_no=row[6],
                        is_active=True if row[9] == 'True' else False,
                        is_superuser=True if row[10] == 'True' else False,
                        is_staff=True if row[11] == 'True' else False
                    )
                    employee.set_password(config.get('application', {}).get('user_default_password'))
                    employee.save()
                    print(f'Saved record {row[0]} {row[1]}')
                except:
                    print(f'Error creating {row[0]} {row[1]}')
                    continue

        print('Finished populating employee table')
        if len(foreign_key_errors) > 0:
            print('ERROR: You have foreign key errors')
            print('================================================================')
            for error in foreign_key_errors:
                print('ERROR:', error)

