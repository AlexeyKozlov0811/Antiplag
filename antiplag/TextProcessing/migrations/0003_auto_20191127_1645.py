# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-27 14:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextProcessing', '0002_auto_20191127_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2019, 11, 27, 16, 45, 28, 681990), verbose_name='Дата завантаження'),
        ),
    ]