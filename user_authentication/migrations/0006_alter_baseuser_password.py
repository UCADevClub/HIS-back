# Generated by Django 5.0 on 2024-02-25 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0005_alter_baseuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
