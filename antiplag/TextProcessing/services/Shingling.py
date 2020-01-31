"""
Module contains business-logic responsible for comparison of texts
"""

import binascii
from typing import Union, List, Dict
from pymorphy2 import MorphAnalyzer
from .StopSymbols import stop_words, stop_symbols

morph = MorphAnalyzer(lang='uk')


def Canonize(source: str) -> List[str]:
    text_cleaning = [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)]
    cleaned_text = []
    # print(text_cleaning)
    for i in range(len(text_cleaning)):
        cleaned_text.append(morph.parse(text_cleaning[i])[0].normal_form)
    # print(cleaned_text)
    return cleaned_text


# generates shingles
def ShingleGeneration(source: List[str]) -> List[int]:
    shingle_len = 4  # длина шингла
    out = []
    words = []
    words_crc = []
    for i in range(len(source) - (shingle_len - 1)):
        out.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))
    words_dict = dict(zip(words_crc, words))  # zip -  creates dictionary where keys are elements of words_crc
    return out


# Splits the text and returns dictionary of hashes and phrases
def CreateShingleDictionary(text: str) -> Dict[int, str]:
    hashes = ShingleGeneration(Canonize(text))
    separated_text = text.split()
    separated_list = []
    separated_str = ""
    shingle_len = 4
    start_index = 0
    i = 0
    while int(i) < len(separated_text):
        if separated_text[i] not in stop_words:
            shingle_len -= 1
            if shingle_len == 2:
                start_index = i
        separated_str += separated_text[i]
        if shingle_len != 0:
            separated_str += " "
        if shingle_len == 0:
            separated_list.append(separated_str)
            shingle_len = 4
            separated_str = ""
            i = start_index
        else:
            i += 1
    # print(separated_list)
    words_dict = dict(zip(hashes, separated_list))
    return words_dict


# compares texts and returns list of similar hashed shingles
def GetSimilarAreas(source1: List[int], source2: List[int]) -> List[int]:
    # same = 0
    similar_phrases = []
    for i in range(len(source1)):
        if source1[i] in source2:
            # same = same + 1
            similar_phrases.append(source1[i])
    return similar_phrases


# def DuplicateSearch(similar_phrases_1, similar_phrases_2):
#     without_duplicates = similar_phrases_1
#     if similar_phrases_1 == similar_phrases_2:
#         return similar_phrases_1
#     else:
#         for i in range(len(similar_phrases_2)):
#             if similar_phrases_2[i] not in without_duplicates:
#                 without_duplicates.append(similar_phrases_2[i])
#     return without_duplicates


# returns common parts of the texts
def GetSimilarAreasDefinition(text1_dictionary: Dict[int, str], compared_texts: List[Union[int, str]]) -> List[str]:
    areas = []
    new = []
    defined_area = ""
    word = ""
    areas_str = ""
    counter = 0
    for k in range(len(compared_texts)):
        if compared_texts[k] in text1_dictionary:
            areas.append((text1_dictionary.get(compared_texts[k])))
        else:
            print("false")
    for k in range(len(areas)):
        new.append(areas[k].split(' '))
        for l in range(len(new[k])):
            ind = new[k][l]
            if new[k][l] not in stop_words:
                counter += 1
                if counter == 3:
                    word = new[k][l]
        areas_str = ' '.join(new[k])
        counter = 0
        if word not in defined_area:
            defined_area += "#" + areas_str + " "
        else:
            areas_str = areas_str.split()
            defined_area += ' '.join(areas_str[areas_str.index(word) + 1:len(new[k])]) + " "
    list_of_areas = defined_area.split('#')
    del list_of_areas[0]
    # print(list_of_areas)
    return list_of_areas


def RemoveDuplicates(old_similar_phrases: List[int], new_similar_phrases: List[int]) -> List[int]:
    duplicates_indexes = []
    for word_in_old in old_similar_phrases:
        for word_in_new in new_similar_phrases:
            if word_in_new == word_in_old:
                duplicates_indexes.append(new_similar_phrases.index(word_in_new))
    duplicates_indexes = list(set(duplicates_indexes))
    duplicates_indexes.sort(reverse=True)
    for duplicate in duplicates_indexes:
        del new_similar_phrases[duplicate]
    return new_similar_phrases


# counts the percentage of two texts, will be changed later
def SimilarityPercentageCalculation(source: List[int], same: List[int]) -> float:
    try:
        return float(format(100 - len(same) / float(len(source)) * 100, '.2f'))
    except ZeroDivisionError:
        return 0.0


def SplitText(text, burrowed_content):
    diapasons = str(len(burrowed_content))
    for burrowed_str in burrowed_content:
        first = text.find(burrowed_str)
        last = first+len(burrowed_str)
        diapasons += " " + str(first) + ":" + str(last)
    return diapasons


if __name__ == "__main__":
    text1 = u'Київ здавна розташовувався на перетині важливих шляхів. Ще за Київської Русі таким шляхом був ' \
            u'легендарний Шлях із варягів у греки. Нині місто перетинають міжнародні автомобільні та залізничні ' \
            u'шляхи. На сучасній території України відомі поселення багатьох археологічних культур, починаючи з доби ' \
            'палеоліту — мустьєрської, гребениківської, кукрецької, трипільської, середньостогівської, ямної, ' \
            u'бойових сокир, чорноліської тощо. Епітет — це слово чи словосполучення, завдяки особливій функції в ' \
            u'тексті, допомагає слову набути нового значення або смислового відтінку, підкреслює характерну рису, ' \
            u'визначальну якість певного предмету або явища, збагачує мову новим емоційним сенсом, додає до тексту ' \
            u'певної мальовничості та насиченості. Місто розташоване на півночі України, на межі Полісся і лісостепу ' \
            u'по обидва береги Дніпра в його середній течії.'

    text2 = u'Київ здавна розташовувався на перетині важливих шляхів. Ще за Київської Русі таким шляхом був ' \
            u'легендарний Шлях із варягів у греки. Нині місто перетинають міжнародні автомобільні та залізничні ' \
            u'шляхи. На сучасній території України відомі поселення багатьох археологічних культур, починаючи з доби ' \
            'палеоліту — мустьєрської, гребениківської, кукрецької, трипільської, середньостогівської, ямної, ' \
            u'бойових сокир, чорноліської тощо. Епітет — це слово чи словосполучення, завдяки особливій функції в ' \
            u'тексті, допомагає слову набути нового значення або смислового відтінку, підкреслює характерну рису, ' \
            u'визначальну якість певного предмету або явища, збагачує мову новим емоційним сенсом, додає до тексту ' \
            u'певної мальовничості та насиченості. Місто розташоване на півночі України, на межі Полісся і лісостепу ' \
            u'по обидва береги Дніпра в його середній течії.'

    text3 = u'Київ здавна розташовувався на перетині важливих шляхів. Ще за Київської Русі таким шляхом був ' \
            u'легендарний Шлях із варягів у греки. Нині місто перетинають міжнародні автомобільні та залізничні ' \
            u'шляхи. На сучасній території України відомі поселення багатьох археологічних культур, починаючи з доби ' \
            'палеоліту — мустьєрської, гребениківської, кукрецької, трипільської, середньостогівської, ямної, ' \
            u'бойових сокир, чорноліської тощо. Епітет — це слово чи словосполучення, завдяки особливій функції в ' \
            u'тексті, допомагає слову набути нового значення або смислового відтінку, підкреслює характерну рису, ' \
            u'визначальну якість певного предмету або явища, збагачує мову новим емоційним сенсом, додає до тексту ' \
            u'певної мальовничості та насиченості. Місто розташоване на півночі України, на межі Полісся і лісостепу ' \
            u'по обидва береги Дніпра в його середній течії.'

    # text2 = u'Київ здавна розташовувався на перетині важливих шляхів. Ще за Київської Русі таким шляхом був ' \
    #         u'легендарний Шлях із варягів у греки. Нині місто перетинають міжнародні автомобільні та залізничні ' \
    #         u'шляхи. На сучасній території України відомі поселення багатьох археологічних культур, починаючи з доби ' \
    #         u'палеоліту — мустьєрської, гребениківської, кукрецької, трипільської, середньостогівської, ямної, ' \
    #         u'бойових сокир, чорноліської тощо. В античні часи на території України виникли державні утворення ' \
    #         u'скіфів, давньогрецьких колоністів, готів, але відправним пунктом української слов\'янської державності ' \
    #         u'й культури вважається Київська Русь IX—XIII століть. Після монгольської навали її спадкоємцем стало ' \
    #         u'Руське королівство XIII—XIV століття. Воно було поглинуте сусідніми Литвою та Польщею, ' \
    #         u'об\'єднаними з XVI століття у федеративну Річ Посполиту.'
    #
    # text3 = u'На сучасній території України відомі поселення багатьох археологічних культур, починаючи з доби ' \
    #         u'палеоліту — мустьєрської, гребениківської, кукрецької, трипільської, середньостогівської, ямної, ' \
    #         u'бойових сокир, чорноліської тощо. В античні часи на території України виникли державні утворення ' \
    #         u'скіфів, давньогрецьких колоністів, готів, але відправним пунктом української слов\'янської державності ' \
    #         u'й культури вважається Київська Русь IX—XIII століть. Після монгольської навали її спадкоємцем стало ' \
    #         u'Руське королівство XIII—XIV століття. Воно було поглинуте сусідніми Литвою та Польщею, ' \
    #         u'об\'єднаними з XVI століття у федеративну Річ Посполиту. Місто розташоване на півночі України, ' \
    #         u'на межі Полісся і лісостепу по обидва береги Дніпра в його середній течії. Площа міста 836 км. Довжина ' \
    #         u'вздовж берега — понад 20 км. '

    shingle_dict = CreateShingleDictionary(text1)

    # print(shingle_dict)

    shingled_canonized_text1 = ShingleGeneration(Canonize(text1))
    shingled_canonized_text2 = ShingleGeneration(Canonize(text2))
    shingled_canonized_text3 = ShingleGeneration(Canonize(text3))

    similar_1 = GetSimilarAreas(shingled_canonized_text1, shingled_canonized_text2)
    similar_2 = GetSimilarAreas(shingled_canonized_text1, shingled_canonized_text3)

    # print(similar_1)
    #
    # print(similar_2)
    #
    # print(similar_1 + similar_2)

    similar_2 = RemoveDuplicates(similar_1, similar_2)

    similar_1 += similar_2

    # print(similar_1)
    #
    # print(list(set(similar_1 + similar_2)))

    similar_areas = GetSimilarAreasDefinition(shingle_dict, similar_1)

    print(SplitText(text1, similar_areas))

    print(text1)
