# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-21 02:15
from __future__ import unicode_literals

from django.db import migrations, models
import monitor.models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20171216_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dream',
            name='image',
            field=models.ImageField(blank=True, default='#', max_length=255, null=True, upload_to=monitor.models.scramble_uploaded_filename),
        ),
    ]