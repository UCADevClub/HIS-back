# Generated by Django 5.0.4 on 2024-06-12 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='branchadministrator',
            table='BranchAdministrator',
        ),
        migrations.AlterModelTable(
            name='doctor',
            table='Doctor',
        ),
        migrations.AlterModelTable(
            name='hospitaladministrator',
            table='HospitalAdministrator',
        ),
        migrations.AlterModelTable(
            name='patientmanager',
            table='PatientManager',
        ),
        migrations.AlterModelTable(
            name='speciality',
            table='Speciality',
        ),
    ]
