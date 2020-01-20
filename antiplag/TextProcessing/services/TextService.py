"""
Module contains business-logic responsible for operating and extraction data from data base
"""

import json
from typing import List, Dict, Tuple

from .Parser import *
from .Shingling import *
from ..models import Text


# function creates text in database and returns its id in database
def CreateText(content: str, author: str = "Unknown") -> int:
    text = Text()
    text.author = author
    text.content = content
    text.save()
    return text.id


# function returns text content by id
def GetTextContent(text_id: int) -> str:
    text = Text.objects.get(id=text_id)
    return text.content


# function returns text burrowed content by main text id and second text id(if needed)
def GetTextBurrowedContent(main_text_id: int, second_text_id: int = -1) -> str:
    main_text = Text.objects.get(id=main_text_id)
    text_burrowed_content = json.loads(main_text.burrowed_content)
    if second_text_id == -1:
        return text_burrowed_content.get(str(main_text_id))
    else:
        return text_burrowed_content.get(str(second_text_id))


# function separates burrowed content and its source in another database field
def SeparateBurrowedContent(text_id: int, main_burrowed_content: List[str],
                            another_burrowed_content: Dict[int, List[str]]) -> None:
    text = Text.objects.get(id=text_id)
    burrowed_content = {text.id: main_burrowed_content}
    burrowed_content.update(another_burrowed_content)
    text.burrowed_content = json.dumps(burrowed_content, ensure_ascii=False)
    # for content in burrowed_content:
    #     self.content = self.content.replace(content,
    #                                         " 1!_!_!1 " + content + " 2!_!_!2 ")
    text.save()


# function finds and adds texts with content similar to text content by id
def FindSimilarInWeb(text_id: int) -> None:
    text = Text.objects.get(id=text_id)
    SetOfUrls = FindTextUrls(text.content)
    if SetOfUrls:
        for url in SetOfUrls:
            if not Text.objects.filter(source=url).exists():
                web_text = Text()
                web_text.source = url
                web_text.content = GetWebContent(url)
                web_text.uniqueness = -1.0
                if web_text.content != "0":
                    web_text.shingle_dict = json.dumps(CreateShingleDictionary(web_text.content),
                                                       ensure_ascii=False)
                    web_text.save()
                else:
                    del web_text


# function finds similar areas in text by id and
# returns list with sources, similar parts and dictionary with sources id as a key and text parts as a value
def FindSimilarAreas(text_id: int, user_text_shingles: List[int]) -> Tuple[List[int], List[int], Dict[int, List[str]]]:
    sources: List[int] = []
    similar_parts: List[int] = []
    database_text_similar_content: Dict[int: List[str]] = {}
    for data_base_text in Text.objects.exclude(id=text_id).exclude(uniqueness=0.0):

        database_text_shingles = [int(item) for item in list(json.loads(data_base_text.shingle_dict).keys())]

        similar_part = GetSimilarAreas(user_text_shingles, database_text_shingles)

        if similar_part:
            sources.append(data_base_text.id)

            str_similar_part = [str(item) for item in similar_part]

            similar_part = RemoveDuplicates(similar_parts, similar_part)

            data_base_text_shingle_dict = json.loads(data_base_text.shingle_dict)

            data_base_similar_content = GetSimilarAreasDefinition(data_base_text_shingle_dict, str_similar_part)
            database_text_similar_content[data_base_text.id] = data_base_similar_content
            similar_parts += similar_part

    return sources, similar_parts, database_text_similar_content


# function compares text by id with other texts in database and compute its uniqueness
# adds sources and similar parts in sources
# EXPLANATION OF IMPLEMENTATION: function contains many actions because it
# contains a lot of calculations with a lot of supporting data useful for other calculations in the future
def CompareWithDatabaseTexts(text_id: int) -> None:
    text = Text.objects.get(id=text_id)

    user_text_shingle_dict = CreateShingleDictionary(text.content)

    text.shingle_dict = json.dumps(user_text_shingle_dict, ensure_ascii=False)

    user_text_shingles = list(user_text_shingle_dict.keys())

    sources, similar_parts, database_text_similar_content = FindSimilarAreas(text_id, user_text_shingles)

    try:
        text.sources = json.dumps(sources)
    except TypeError:
        text.sources = -1

    text.uniqueness = SimilarityPercentageCalculation(user_text_shingles, similar_parts)
    if text.uniqueness < 0:
        text.uniqueness = 0.0
    text.save()

    user_text_similar_content = GetSimilarAreasDefinition(user_text_shingle_dict, similar_parts)
    SeparateBurrowedContent(text_id, user_text_similar_content, database_text_similar_content)