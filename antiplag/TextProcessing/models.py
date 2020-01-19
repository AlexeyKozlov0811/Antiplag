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
    burrowed_content = models.TextField(default=json.dumps([{"": []}]), verbose_name="Запозичений текст")
    shingle_dict = models.TextField(default=json.dumps({"": ""}), verbose_name="Словник шинглів")
    uniqueness = models.FloatField(default=-1, verbose_name="Унікальність")
    upload_date = models.DateField(default=timezone.now, verbose_name="Дата завантаження")

    def __str__(self):
        return 'Автор - {0}'.format(self.author) + ' Дата - {0}'.format(self.upload_date)

    def separate_burrowed_content(self, main_burrowed_content, another_burrowed_content):
        burrowed_content = [{self.id: main_burrowed_content}] + another_burrowed_content
        self.burrowed_content = json.dumps(burrowed_content, ensure_ascii=False)
        # for content in burrowed_content:
        #     self.content = self.content.replace(content,
        #                                         " 1!_!_!1 " + content + " 2!_!_!2 ")

    def hide_separators(self):
        without_separators = self.content.replace(" 1!_!_!1 ", "")
        without_separators = without_separators.replace(" 2!_!_!2 ", "")
        return without_separators

    def get_sources(self):
        return json.loads(self.sources)

    def get_burrowed_content(self):
        return json.loads(self.burrowed_content)

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
                        web_text.shingle_dict = json.dumps(create_shingle_dictionary(web_text.content),
                                                           ensure_ascii=False)
                        web_text.save()
                    else:
                        del web_text

    def compare_with_database_texts(self):
        sources_id = []
        similar_parts = []
        database_text_similar_content = []
        user_text_shingle_dict = create_shingle_dictionary(self.content)
        self.shingle_dict = json.dumps(user_text_shingle_dict, ensure_ascii=False)

        user_text_shingled_content = list(user_text_shingle_dict.keys())

        for data_base_text in Text.objects.exclude(id=self.id).exclude(uniqueness=0.0):

            database_text_shingled_content = [int(item) for item in list(json.loads(data_base_text.shingle_dict).keys())]

            similar_part = comparation(user_text_shingled_content, database_text_shingled_content)

            if similar_part:
                sources_id.append(data_base_text.id)
                similar_part = duplicate_clear(similar_parts, similar_part)

                str_similar_part = [str(item) for item in similar_part]
                data_base_text_shingle_dict = json.loads(data_base_text.shingle_dict)
                data_base_similar_content = similar_areas_definition(data_base_text_shingle_dict, str_similar_part)
                database_text_similar_content.append({data_base_text.id: data_base_similar_content})

                similar_parts += similar_part

        try:
            self.sources = json.dumps(sources_id)
        except TypeError:
            self.sources = -1

        user_text_similar_content = similar_areas_definition(user_text_shingle_dict, similar_parts)
        self.separate_burrowed_content(user_text_similar_content, database_text_similar_content)
        self.uniqueness = similarity_percentage_calculation(user_text_shingled_content, similar_parts)
        if self.uniqueness < 0:
            self.uniqueness = 0.0
        self.save()
