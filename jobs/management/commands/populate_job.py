from django.core.management import BaseCommand
from employees.models import Employee
from jobs.models import Job
from clients.models import Client
from msdbom.settings import BASE_DIR, config

import os
import csv


class Command(BaseCommand):
    help = 'Create records from csv with python manage.py populate_job <csv_file_name.csv>'

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

                sales_executive = None
                if row[2] != '':
                    try:
                        id_text, name = row[2].split(' - ')
                        _, id = id_text.split(': ')
                        sales_executive = Employee.objects.get(id=int(id))
                    except:
                        foreign_key_errors.append(f'{row[2]} does not exist in employee table for job {row[1]}')

                client = None
                if row[7] != '':
                    try:
                        id_text, company_name = row[7].split(' - ')
                        client = Client.objects.get(company_name=company_name)
                    except:
                        foreign_key_errors.append(f'{row[7]} does not exist in client table for job {row[1]}')

                prepared_by = None
                if row[30] != '':
                    try:
                        id_text, name = row[30].split(' - ')
                        _, id = id_text.split(': ')
                        prepared_by = Employee.objects.get(id=int(id))
                    except:
                        foreign_key_errors.append(f'{row[30]} does not exist in employee table for job {row[1]}')

                reviewed_by = None
                if row[31] != '':
                    try:
                        id_text, name = row[31].split(' - ')
                        _, id = id_text.split(': ')
                        reviewed_by = Employee.objects.get(id=int(id))
                    except:
                        foreign_key_errors.append(f'{row[31]} does not exist in employee table for job {row[1]}')

                approved_by = None
                if row[32] != '':
                    try:
                        id_text, name = row[32].split(' - ')
                        _, id = id_text.split(': ')
                        approved_by = Employee.objects.get(id=int(id))
                    except:
                        foreign_key_errors.append(f'{row[32]} does not exist in employee table for job {row[1]}')

                try:
                    job = Job.objects.create(
                        job_id=row[1],
                        sales_executive=sales_executive,
                        event_name=row[3],
                        event_venue=row[4],
                        start_date=row[5],
                        end_date=row[6],
                        client=client,
                        ingress_date=row[8],
                        ingress_time=row[9],
                        egress_date=row[10],
                        egress_time=row[11],
                        cluster_booth_count_2x2=row[13] if row[13] != '' else '0',
                        cluster_total_count_2x2=row[14] if row[14] != '' else '0',
                        cluster_booth_count_2x3=row[15] if row[15] != '' else '0',
                        cluster_total_count_2x3=row[16] if row[16] != '' else '0',
                        cluster_booth_count_3x3=row[17] if row[17] != '' else '0',
                        cluster_total_count_3x3=row[18] if row[18] != '' else '0',
                        cluster_booth_count_3x4=row[19] if row[19] != '' else '0',
                        cluster_total_count_3x4=row[20] if row[20] != '' else '0',
                        cluster_booth_count_4x4=row[21] if row[21] != '' else '0',
                        cluster_total_count_4x4=row[22] if row[22] != '' else '0',
                        perimeter_booth_count_2x2=row[23] if row[23] != '' else '0',
                        perimeter_total_count_2x2=row[24] if row[24] != '' else '0',
                        perimeter_booth_count_2x3=row[25] if row[25] != '' else '0',
                        perimeter_total_count_2x3=row[26] if row[26] != '' else '0',
                        perimeter_booth_count_3x3=row[27] if row[27] != '' else '0',
                        perimeter_total_count_3x3=row[28] if row[28] != '' else '0',
                        contingency=int(row[29]) if row[29] != '' else 0,
                        prepared_by=prepared_by,
                        reviewed_by=reviewed_by,
                        approved_by=approved_by
                    )
                    job.save()
                    print(f'Saved record {row[0]} {row[1]}')
                except:
                    print(f'Error creating {row[0]} {row[1]}')
                    continue

        print('Finished populating job table')
        if len(foreign_key_errors) > 0:
            print('ERROR: You have foreign key errors')
            print('================================================================')
            for error in foreign_key_errors:
                print('ERROR:', error)

