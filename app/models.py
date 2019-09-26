from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.BooleanField(default=False)

    #def __init__(self, ):


class Text(models.Model):
    author = models.CharField(max_length=255, verbose_name="Автор", default="Unknown")
    source = models.CharField(max_length=255, verbose_name="Джерело")
    content = models.TextField(verbose_name="Текст")
    uniqueness = models.FloatField(default=0)

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