"""
Module contains business-logic responsible for comparison of texts
"""

import binascii
import re
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


# Removes symbols after word
def PunctuationRemoval(word: str):
    if re.search(r'\W$', word):
        word_without_symbol = re.sub(r'\W$', "", word)
        return word_without_symbol
    else:
        return ""


# Splits the text and returns dictionary of hashes and phrases
def CreateShingleDictionary(text: str) -> Dict[int, str]:
    hashes = ShingleGeneration(Canonize(text))
    separated_text = text.split()
    separated_list = []
    separated_str = ""
    shingle_len = 4
    start_index = 0
    i = 0
    stop_words_counter = 0
    while int(i) < len(separated_text):
        # print(stop_words_counter)
        word_without_symbol = PunctuationRemoval(separated_text[i])
        if shingle_len == 0:
            if separated_text[i].lower() not in stop_words and separated_text[i] not in stop_symbols and (
                    word_without_symbol == "" or word_without_symbol not in stop_words):
                i = start_index
                separated_list.append(separated_str)
                shingle_len = 4
                separated_str = ""
            else:
                separated_str += " "

        if separated_text[i].lower() in stop_words or word_without_symbol in stop_words:
            stop_words_counter += 1

        if shingle_len == 4:
            stop_words_counter = 0

        if separated_text[i].lower() not in stop_words and separated_text[i] not in stop_symbols and (
                word_without_symbol == "" or word_without_symbol not in stop_words):
            shingle_len -= 1

        if (shingle_len == 2 and stop_words_counter == 0) and separated_text[i].lower() not in stop_words and \
                separated_text[i] not in stop_symbols and (word_without_symbol == "" or word_without_symbol not in stop_words):
            start_index = i
        else:
            if shingle_len == 3 and stop_words_counter == 1:
                start_index = i

        separated_str += separated_text[i]

        if shingle_len != 0:
            separated_str += " "
        i += 1
        if i == len(separated_text):
            separated_list.append(separated_str)
    words_dict = dict(zip(hashes, separated_list))
    return words_dict


# compares texts and returns list of similar hashed shingles
def GetSimilarAreas(source1: List[int], source2: List[int]) -> List[int]:
    similar_phrases = []
    for i in range(len(source1)):
        if source1[i] in source2:
            similar_phrases.append(source1[i])
    return similar_phrases


# returns common parts of the texts
def GetSimilarAreasDefinition(text1_dictionary: Dict[int, str], compared_texts: List[Union[int, str]]) -> List[str]:
    areas = []
    new_list_of_areas = []
    defined_area = ""
    word = ""
    areas_str = ""
    last_words_string = ""
    for k in range(len(compared_texts)):
        if compared_texts[k] in text1_dictionary:
            areas.append((text1_dictionary.get(compared_texts[k])))
    key = False
    for i in range(len(areas)):
        new_list_of_areas.append(areas[i].split(' '))
        counter = 0
        middle_words = ""
        for j in range(len(new_list_of_areas[i])):

            view_var_delete_later = new_list_of_areas[i][j]

            word_without_punct = PunctuationRemoval(new_list_of_areas[i][j])
            if new_list_of_areas[i][j].lower() not in stop_words and new_list_of_areas[i][j] not in stop_symbols and (
                    word_without_punct == "" or word_without_punct not in stop_words):
                counter += 1

            if counter == 2 or counter == 3:
                middle_words += new_list_of_areas[i][j] + ' '
            if counter == 4:
                middle_words = re.sub(r'\s$', "", middle_words)

            if middle_words not in defined_area and counter > 3:
                defined_area += " #" + ' '.join(new_list_of_areas[i])
                key = True
            else:
                key = False

            if counter == 4 and key is False:
                last_words_string += ' ' + new_list_of_areas[i][j]

        defined_area += last_words_string
        last_words_string = ""

    list_of_areas = defined_area.split('#')
    del list_of_areas[0]

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


def SplitText(text, borrowed_content):
    diapasons = str(len(borrowed_content))
    for borrowed_str in borrowed_content:
        first = text.find(borrowed_str)
        last = first + len(borrowed_str)
        diapasons += " " + str(first) + ":" + str(last)
    return diapasons


if __name__ == "__main__":
    text1 = u'Київ здавна розташовувався на перетині важливих шляхів. Ще за Київської Русі таким шляхом був ' \
            u'легендарний Шлях із варягів у греки. Після цього промий його під холодною водою. Нині місто перетинають ' \
            u'міжнародні автомобільні та залізничні шляхи. Потім висип рис в каструлю з киплячою підсоленою водою. ' \
            u'Пропорції: 1 стакан дикого рису на 3 склянки води На сучасній території України відомі поселення ' \
            u'багатьох археологічних культур, починаючи з доби палеоліту — мустьєрської, гребениківської, кукрецької, ' \
            u'трипільської, середньостогівської, ямної, бойових сокир, чорноліської тощо.'

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

    shingle_dict = CreateShingleDictionary(text1)

    print(shingle_dict)

    # print(ShingleGeneration(Canonize(text1)))
    # print(Canonize(text1))
    # print(len(Canonize(text1)))
    # print(len(ShingleGeneration(Canonize(text1))))

    shingled_canonized_text1 = ShingleGeneration(Canonize(text1))
    shingled_canonized_text2 = ShingleGeneration(Canonize(text2))
    # shingled_canonized_text3 = ShingleGeneration(Canonize(text3))
    #
    similar_1 = GetSimilarAreas(shingled_canonized_text1, shingled_canonized_text2)
    # similar_2 = GetSimilarAreas(shingled_canonized_text1, shingled_canonized_text3)
    #
    # print(similar_1)
    # #
    # # print(similar_2)
    # #
    # # print(similar_1 + similar_2)
    #
    # similar_2 = RemoveDuplicates(similar_1, similar_2)
    #
    # similar_1 += similar_2
    #
    # # print(similar_1)
    # #
    # # print(list(set(similar_1 + similar_2)))
    #
    similar_areas = GetSimilarAreasDefinition(shingle_dict, similar_1)

    # print(similar_areas)
    #
    # print(SplitText(text1, similar_areas))
    #
    # print(text1)
