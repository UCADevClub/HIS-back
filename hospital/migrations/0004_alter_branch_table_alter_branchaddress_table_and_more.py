# Generated by Django 5.0.4 on 2024-05-28 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_alter_branch_address_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='branch',
            table='Branch',
        ),
        migrations.AlterModelTable(
            name='branchaddress',
            table='BranchAddress',
        ),
        migrations.AlterModelTable(
            name='branchphonenumber',
            table='BranchPhoneNumber',
        ),
        migrations.AlterModelTable(
            name='department',
            table='Department',
        ),
        migrations.AlterModelTable(
            name='hospital',
            table='Hospital',
        ),
    ]