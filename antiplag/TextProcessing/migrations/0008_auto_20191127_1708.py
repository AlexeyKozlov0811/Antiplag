# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-27 15:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextProcessing', '0007_auto_20191127_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2019, 11, 27, 17, 8, 34, 571434), verbose_name='Дата завантаження'),
        ),
    ]
