from celery import shared_task
from .DataProcessing import Parser, Shingling
from .models import Text


@shared_task
def check_uniqueness(user_text_id):
    check_web(user_text_id)
    check_database(user_text_id)
    return 0


@shared_task
def check_web(user_text_id):
    user_text = Text.objects.get(id=user_text_id)
    SetOfUrls = Parser.find_text_urls(user_text.content)
    if SetOfUrls:
        for url in SetOfUrls:
            if not Text.objects.filter(source=url).exists():
                web_text = Text()
                web_text.source = url
                web_text.content = Parser.get_content(url)
                web_text.uniqueness = -1.0
                if web_text.content != "0":
                    web_text.save()
                else:
                    del web_text
        return 1
    else:
        return 0


@shared_task
def check_database(user_text_id):
    similar_parts = []
    user_text = Text.objects.get(id=user_text_id)
    shingle_dict = Shingling.shingle_generation(Shingling.canonize(user_text.content), 1)
    shingled_user_text = Shingling.shingle_generation(Shingling.canonize(user_text.content), 0)
    for data_base_text in Text.objects.exclude(id=user_text_id).exclude(uniqueness=0.0):
        shingled_db_text = Shingling.shingle_generation(Shingling.canonize(data_base_text.content), 0)
        similar_parts += (Shingling.comparation(shingled_user_text, shingled_db_text))
    user_text.uniqueness = Shingling.similarity_percentage_calculation(shingled_user_text, similar_parts)
    print(user_text.uniqueness)
    user_text.save()
    return 0
