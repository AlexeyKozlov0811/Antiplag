# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-01 21:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TextProcessing', '0024_auto_20191201_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='areas',
        ),
    ]
