# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-01 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextProcessing', '0021_auto_20191201_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='areas',
        ),
        migrations.AlterField(
            model_name='text',
            name='content',
            field=models.TextField(verbose_name='Текст'),
        ),
    ]
