# Generated by Django 5.2.1 on 2025-06-10 10:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_remove_complaint_failure_node_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='machines', to=settings.AUTH_USER_MODEL),
        ),
    ]
