from celery import shared_task
from .models import Text


@shared_task
def check_uniqueness(user_text_id):
    user_text = Text.objects.get(id=user_text_id)
    user_text.find_similar_in_web()
    user_text.compare_with_database_texts()
    return 0


