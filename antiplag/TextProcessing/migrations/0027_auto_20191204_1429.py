# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-04 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextProcessing', '0026_auto_20191204_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='sources',
            field=models.TextField(default=-1, verbose_name='Джерела'),
        ),
    ]
