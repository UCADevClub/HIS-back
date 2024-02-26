# Generated by Django 5.0 on 2024-02-25 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0002_alter_baseuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='base_user', to='user_authentication.address'),
        ),
    ]