# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-30 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('TextProcessing', '0019_auto_20191130_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='upload_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата завантаження'),
        ),
    ]
