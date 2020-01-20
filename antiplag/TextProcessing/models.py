"""
Module contains Django ORM entities
"""
from django.db import models
from django.utils import timezone
import json


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, verbose_name="Автор", default="Unknown")
    source = models.CharField(max_length=255, verbose_name="Джерело", default="Author")
    sources = models.TextField(default=-1, verbose_name="Джерела")
    content = models.TextField(verbose_name="Текст")
    burrowed_content = models.TextField(default=json.dumps({"": []}), verbose_name="Запозичений текст")
    shingle_dict = models.TextField(default=json.dumps({"": ""}), verbose_name="Словник шинглів")
    uniqueness = models.FloatField(default=-1, verbose_name="Унікальність")
    upload_date = models.DateField(default=timezone.now, verbose_name="Дата завантаження")

    def __str__(self):
        return 'Автор - {0}'.format(self.author) + ' Дата - {0}'.format(self.upload_date)

    def hide_separators(self):
        without_separators = self.content.replace(" 1!_!_!1 ", "")
        without_separators = without_separators.replace(" 2!_!_!2 ", "")
        return without_separators

    def get_sources(self):
        return json.loads(self.sources)

