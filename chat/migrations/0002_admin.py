# Generated by Django 3.0.5 on 2020-07-20 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('age', models.IntegerField()),
                ('rating', models.IntegerField()),
            ],
        ),
    ]
