"""
Module contains Django ORM entities
"""
from django.conf import settings
from django.db import models
from django.utils import timezone
import json


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, verbose_name="Автор", default="Unknown", editable=settings.DEBUG)
    source = models.CharField(max_length=255, verbose_name="Джерело", default="Author", editable=settings.DEBUG)
    sources = models.TextField(default=-1, verbose_name="Джерела", editable=settings.DEBUG)
    content = models.TextField(verbose_name="Текст", editable=settings.DEBUG)
    burrowed_content = models.TextField(default=json.dumps({"": []}), verbose_name="Запозичений текст", editable=settings.DEBUG)
    shingle_dict = models.TextField(default=json.dumps({"": ""}), verbose_name="Словник шинглів", editable=settings.DEBUG)
    uniqueness = models.FloatField(default=-1, verbose_name="Унікальність", editable=settings.DEBUG)
    upload_date = models.DateField(default=timezone.now, verbose_name="Дата завантаження", editable=settings.DEBUG)

    def __str__(self):
        return 'id - {0}'.format(self.id) + ' Автор - {0}'.format(self.author) + ' Дата - {0}'.format(self.upload_date)

    def hide_separators(self):
        without_separators = self.content.replace(" 1!_!_!1 ", "")
        without_separators = without_separators.replace(" 2!_!_!2 ", "")
        return without_separators

    def get_sources(self):
        return json.loads(self.sources)

