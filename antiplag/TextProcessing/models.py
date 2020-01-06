from django.db import models
from django.utils import timezone
from .DataProcessing.Parser import *
from .DataProcessing.Shingling import *
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
        return 'Автор - {0}'.format(self.author) + ' Дата - {0}'.format(self.upload_date)

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

    def find_similar_in_web(self):
        SetOfUrls = find_text_urls(self.content)
        if SetOfUrls:
            for url in SetOfUrls:
                if not Text.objects.filter(source=url).exists():
                    web_text = Text()
                    web_text.source = url
                    web_text.content = get_content(url)
                    web_text.uniqueness = -1.0
                    if web_text.content != 0:
                        web_text.shingled_content = json.dumps(shingle_generation(canonize(web_text.content)))
                        web_text.save()
                    else:
                        del web_text

    def compare_with_database_texts(self):
        sources_id = []
        similar_parts = []
        shingle_dict = text_splitting(self.content)
        user_shingled_content = shingle_generation(canonize(self.content))
        self.shingled_content = json.dumps(user_shingled_content)

        for data_base_text in Text.objects.exclude(id=self.id).exclude(uniqueness=0.0):
            similar_part = comparation(user_shingled_content,
                                       json.loads(data_base_text.shingled_content))
            if similar_part:
                sources_id.append(data_base_text.id)
                similar_part = duplicate_clear(similar_parts, similar_part)
                similar_parts += similar_part

        try:
            self.sources = json.dumps(sources_id)
        except TypeError:
            self.sources = -1
        self.split_content(similar_areas_definition(shingle_dict, similar_parts))
        self.uniqueness = similarity_percentage_calculation(user_shingled_content, similar_parts)
        if self.uniqueness < 0:
            self.uniqueness = 0.0
        self.save()
