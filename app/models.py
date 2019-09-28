from django.db import models
from datetime import datetime


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, verbose_name="Автор", default="Unknown")
    source = models.CharField(max_length=255, verbose_name="Джерело")
    content = models.TextField(verbose_name="Текст")
    uniqueness = models.FloatField(default=0, verbose_name="Унікальність")
    upload_date = models.DateField(default=datetime.today(), verbose_name="Дата завантаження")

    def __str__(self):
        return 'Джерело - {0}'.format(self.author)

    # def __init__(self, source, content, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.source = source
    #     self.content = content
    #     # self.save()

    # def set_uniqueness(self, uniqueness):
    #     self.uniqueness = uniqueness
    #     self.save()
