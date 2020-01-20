from celery import shared_task
from .services.TextService import *
from .models import Text


@shared_task
def check_uniqueness(user_text_id):
    FindSimilarInWeb(user_text_id)
    CompareWithDatabaseTexts(user_text_id)
    return 0


