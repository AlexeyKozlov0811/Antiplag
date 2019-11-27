from django.db import models
from datetime import datetime


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, verbose_name="Автор", default="Unknown")
    source = models.CharField(max_length=255, verbose_name="Джерело", default="Author")
    content = models.TextField(verbose_name="Текст")
    shingled_content = models.TextField(null=True ,verbose_name="шинглований канонічний текст")
    uniqueness = models.FloatField(default=-1, verbose_name="Унікальність")
    upload_date = models.DateField(default=datetime.today(), verbose_name="Дата завантаження")

    def __str__(self):
        return 'Джерело - {0}'.format(self.author)
