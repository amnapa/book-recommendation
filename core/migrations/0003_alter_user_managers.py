# Generated by Django 5.0.7 on 2024-07-24 20:27

import core.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_email'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', core.managers.CustomUserManager()),
            ],
        ),
    ]
