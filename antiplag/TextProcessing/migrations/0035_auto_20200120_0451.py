# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-01-20 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextProcessing', '0034_auto_20200119_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='burrowed_content',
            field=models.TextField(default='{"": []}', verbose_name='Запозичений текст'),
        ),
    ]
