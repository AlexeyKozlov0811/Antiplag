# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-25 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=255, verbose_name='Джерело')),
                ('content', models.TextField(verbose_name='Текст')),
            ],
        ),
    ]
