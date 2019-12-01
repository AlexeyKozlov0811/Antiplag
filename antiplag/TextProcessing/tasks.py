from celery import shared_task
from .DataProcessing.Parser import *
from .DataProcessing.Shingling import *
from .models import Text
import json


@shared_task
def check_uniqueness(user_text_id):
    check_web(user_text_id)
    check_database(user_text_id)
    return 0


@shared_task
def check_web(user_text_id):
    user_text = Text.objects.get(id=user_text_id)
    SetOfUrls = find_text_urls(user_text.content)
    if SetOfUrls:
        for url in SetOfUrls:
            if not Text.objects.filter(source=url).exists():
                web_text = Text()
                web_text.source = url
                web_text.content = get_content(url)
                web_text.uniqueness = -1.0
                if web_text.content != 0:
                    web_text.shingled_content = json.dumps(shingle_generation(canonize(web_text.content), 0))
                    web_text.save()
                else:
                    del web_text
        return 1
    else:
        return 0


@shared_task
def check_database(user_text_id):
    sources_id = []
    similar_parts = []
    user_text = Text.objects.get(id=user_text_id)
    user_shingled_content = shingle_generation(canonize(user_text.content), 0)
    user_text.shingled_content = json.dumps(user_shingled_content)

    for data_base_text in Text.objects.exclude(id=user_text_id).exclude(uniqueness=0.0):
        similar_part = comparation(user_shingled_content,
                                   json.loads(data_base_text.shingled_content))
        if similar_part:
            sources_id.append(data_base_text.id)
            similar_part = duplicate_clear(similar_parts, similar_part)
            similar_parts += similar_part
            # similar_parts.append(".")

    # similar_parts.remove(".")
    user_text.uniqueness = similarity_percentage_calculation(user_shingled_content, similar_parts)
    if user_text.uniqueness < 0:
        user_text.uniqueness = 0.0
    print(sources_id)
    user_text.save()
    return 0

