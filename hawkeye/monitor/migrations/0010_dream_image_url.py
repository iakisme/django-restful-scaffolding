# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-23 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0009_remove_dream_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='dream',
            name='image_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
