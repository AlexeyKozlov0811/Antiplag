from django.db import models

# Create your models here.

class Text(models.Model):
    source = models.CharField(max_length=255, verbose_name = "Джерело")
    content = models.TextField(verbose_name = "Текст")

    def __str__(self):
        return 'Джерело - {0}'.format(self.source)

    def create(self, source, content):
        text = Text()
        text.source = source
        text.content = content
        text.save()
        return text

