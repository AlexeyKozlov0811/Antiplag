"""
Module contains business-logic responsible for comparison of texts
"""

import binascii
import re
from typing import Union, List, Dict, Tuple
from pymorphy2 import MorphAnalyzer

from django.conf import settings

morph = MorphAnalyzer(lang='uk')
if __name__ == "__main__":
    from antiplag.TextProcessing.services.StopSymbols import stop_words, stop_symbols
    shingle_len = 10
else:
    from .StopSymbols import stop_words, stop_symbols
    shingle_len = settings.SHINGLE_LENGTH

def Canonize(source: str) -> List[str]:
    return [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)]


# generates shingles
def ShingleGeneration(source: List[str]) -> List[int]:
    words_crc = []
    for i in range(len(source) - (shingle_len - 1)):
        words_crc.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))
    return words_crc


# # Removes symbols after word
# def PunctuationRemoval(word: str):
#     if re.search(r'[^\Da-zA-Z?-??-???????????\'-]', word):
#         word_without_symbol = re.sub(r'[^\Da-zA-Z?-??-???????????\'-]', "", word)
#         return word_without_symbol
#     else:
#         return word


# Splits the text and returns dictionary of hashes and phrases
def CreateShingleDictionary(text: str) -> Dict[int, List[str]]:
    canonized = Canonize(text)
    hashes = ShingleGeneration(canonized)
    words = []
    for i in range(len(canonized) - (shingle_len - 1)):
        words.append([x for x in canonized[i:i + shingle_len]])
    words_dict = dict(zip(hashes, words))
    return words_dict


# compares texts and returns list of similar hashed shingles
def GetSimilarAreas(source1: List[int], source2: List[int]) -> List[int]:
    similar_phrases = []
    for i in range(len(source1)):
        if source1[i] in source2:
            similar_phrases.append(source1[i])
    return similar_phrases


# returns common parts of the texts
def GetSimilarAreasDefinition(text1_dictionary: Dict[int, List[str]],
                              compared_texts: Dict[Union[int, str], List[Union[int, str]]],
                              text_type=0)\
        -> Union[Dict[Union[int, str], List[Union[int, str]]], List[List[str]]]:
    list_of_areas = []
    for i in range(len(compared_texts)):
        list_of_local_areas = []
        local_areas = []
        for k in range(len(list(compared_texts.values())[i])):
            if list(compared_texts.values())[i][k] in text1_dictionary:
                local_areas.append((text1_dictionary.get(list(compared_texts.values())[i][k])))
        area = ' '.join(local_areas[i])
        for k in range(len(local_areas) - 1):
            if sum(word in local_areas[k] for word in local_areas[k + 1]) == shingle_len - 1:
                area += ' '
                area += local_areas[k + 1][-1]
            else:
                list_of_local_areas.append(area)
                area = ' '.join(local_areas[k + 1])
        list_of_local_areas.append(area)
        list_of_areas.append(list_of_local_areas)

    if text_type:
        dict_of_areas = {}
        for i in range(len(list_of_areas)):
            dict_of_areas.update({list(compared_texts.keys())[i]: list_of_areas[i]})
        return dict_of_areas
    else:
        return list_of_areas


def RemoveDuplicates(similar_phrases: Dict[Union[int, str], List[int]],
                     new_similar_phrases: Dict[int, List[int]]) -> Dict[Union[int, str], List[int]]:
    duplicates_keys = []
    transformed_dict = {}
    similar_phrases.update(new_similar_phrases)

    for key in similar_phrases:
        if str(key) != str(list(new_similar_phrases.keys())[0]):
            if list(new_similar_phrases.values())[0] == similar_phrases[key]:
                sources = str(key) + "_" + str(list(new_similar_phrases.keys())[0])
                transformed_dict.update({sources: list(new_similar_phrases.values())[0]})
                duplicates_keys.append(key)
                duplicates_keys.append(list(new_similar_phrases.keys())[0])

    if duplicates_keys:
        for key in duplicates_keys:
            del similar_phrases[key]
        similar_phrases.update(transformed_dict)

    return similar_phrases


# counts the percentage of two texts, will be changed later
def SimilarityPercentageCalculation(source: List[int], same: List[int]) -> float:
    try:
        return float(format(100 - len(same) / float(len(source)) * 100, '.2f'))
    except ZeroDivisionError:
        return 0.0


def SplitText(text, borrowed_content):
    diapasons = str(len(borrowed_content))
    for borrowed_str in borrowed_content:
        first = text.find(borrowed_str)
        last = first + len(borrowed_str)
        diapasons += " " + str(first) + ":" + str(last)
    return diapasons


if __name__ == "__main__":
    shingle_len = 10

    text1 = "Python (найчастіше вживане прочитання — «Па́йтон», запозичено назву[5] з британського шоу Монті Пайтон) " \
            "— інтерпретована об'єктно-орієнтована мова програмування високого рівня зі строгою динамічною ffffffffff " \
            "fffffffff типізацією. [6] Розроблена в 1990 році Гвідо ван Россумом. Структури даних високого рівня разом " \
            "із динамічною семантикою та динамічним зв'язуванням роблять її привабливою для швидкої розробки програм " \
            "В мові програмування Python підтримується кілька парадигм програмування, зокрема: об'єктно-орієнтована, " \
            "процедурна, функціональна та аспектно-орієнтована"

    text2 = "Python (найчастіше вживане прочитання — «Па́йтон», запозичено назву[5] з британського шоу Монті Пайтон) " \
            "— інтерпретована об'єктно-орієнтована мова програмування високого рівня зі строгою динамічною " \
            "типізацією. [6] Розроблена в 1990 році Гвідо ван Россумом. Структури даних високого рівня разом із " \
            "динамічною семантикою та динамічним зв'язуванням роблять її привабливою для швидкої розробки програм" \

    text3 = "Python (найчастіше вживане прочитання — «Па́йтон», запозичено назву[5] з британського шоу Монті Пайтон) " \
            "— інтерпретована об'єктно-орієнтована мова програмування високого рівня зі строгою динамічною " \
            "типізацією. [6] Розроблена в 1990 році Гвідо ван Россумом. Структури даних високого рівня разом із " \
            "динамічною семантикою та динамічним зв'язуванням роблять її привабливою для швидкої розробки програм" \

    text4 = "В мові програмування Python підтримується кілька парадигм програмування, зокрема: об'єктно-орієнтована, " \
            "процедурна, функціональна та аспектно-орієнтована"

    shingle_dict = CreateShingleDictionary(text1)

    shingled_canonized_text1 = ShingleGeneration(Canonize(text1))
    shingled_canonized_text2 = ShingleGeneration(Canonize(text2))
    shingled_canonized_text3 = ShingleGeneration(Canonize(text3))
    shingled_canonized_text4 = ShingleGeneration(Canonize(text4))

    similar_1 = GetSimilarAreas(shingled_canonized_text1, shingled_canonized_text2)
    similar_2 = GetSimilarAreas(shingled_canonized_text1, shingled_canonized_text3)
    similar_3 = GetSimilarAreas(shingled_canonized_text1, shingled_canonized_text4)

    similar = RemoveDuplicates({1: similar_1}, {2: similar_2})
    similar = RemoveDuplicates(similar, {3: similar_3})

    similar_areas = GetSimilarAreasDefinition(shingle_dict, similar, 1)

    print(similar_areas)


