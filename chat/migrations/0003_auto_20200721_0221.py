# Generated by Django 3.0.5 on 2020-07-20 20:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_admin'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='admin',
            new_name='staffmembers',
        ),
    ]