# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-27 14:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextProcessing', '0004_auto_20191127_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2019, 11, 27, 16, 51, 2, 392385), verbose_name='Дата завантаження'),
        ),
    ]
