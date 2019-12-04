from django.db import models
from django.utils import timezone
import json


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, verbose_name="Автор", default="Unknown")
    source = models.CharField(max_length=255, verbose_name="Джерело", default="Author")
    sources = models.TextField(default=-1, verbose_name="Джерела")
    content = models.TextField(verbose_name="Текст")
    shingled_content = models.TextField(null=True, verbose_name="Шинглований канонічний текст")
    uniqueness = models.FloatField(default=-1, verbose_name="Унікальність")
    upload_date = models.DateField(default=timezone.now, verbose_name="Дата завантаження")

    def __str__(self):
        return 'Джерело - {0}'.format(self.author)

    def split_content(self, burrowed_content):
        for content in burrowed_content:
            self.content = self.content.replace(content,
                                                "<a class=\"burrowed_content\" title=\"aaaaaaaa\">" + content + "</a>")

    def without_tags(self):
        without_tags = self.content.replace("<a class=\"burrowed_content\" title=\"aaaaaaaa\">", "")
        without_tags = without_tags.replace("</a>", "")
        return without_tags

    def get_sources(self):
        return json.loads(self.sources)
