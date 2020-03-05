"""
Module contains business-logic responsible for comparison of texts
"""

import binascii
import re
from typing import Union, List, Dict, Tuple
from pymorphy2 import MorphAnalyzer
from .StopSymbols import stop_words, stop_symbols
from django.conf import settings

# shingle_len = settings.SHINGLE_LENGTH

morph = MorphAnalyzer(lang='uk')


def Canonize(source: str) -> List[str]:
    # text_cleaning = [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)]
    text_cleaning = []
    pattern = r'[^a-zA-Zа-яА-ЯёЁЇїІіЄєҐґ\'-]'
    splitted_text = source.lower().split()
    for i in range(len(splitted_text)):
        splitted_text[i] = re.sub(pattern, '', splitted_text[i])
    j = 0
    while j < len(splitted_text):
        if re.match(r'^\s*$', splitted_text[j]):
            del splitted_text[j]
        else:
            j += 1
    for k in range(len(splitted_text)):
        if splitted_text[k] not in stop_words:
            text_cleaning.append(splitted_text[k])

    cleaned_text = []
    for i in range(len(text_cleaning)):
        cleaned_text.append(morph.parse(text_cleaning[i])[0].normal_form)
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
    if re.search(r'[^\Da-zA-Zа-яА-ЯёЁЇїІіЄєҐґ\'-]', word):
        word_without_symbol = re.sub(r'[^\Da-zA-Zа-яА-ЯёЁЇїІіЄєҐґ\'-]', "", word)
        return word_without_symbol
    else:
        return word


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

        word_without_symbol = PunctuationRemoval(separated_text[i])
        if shingle_len == 0:
            if separated_text[i].lower() not in stop_words and re.search(stop_symbols, separated_text[i]) and (
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

        if separated_text[i].lower() not in stop_words and re.search(stop_symbols, separated_text[i]) and (
                word_without_symbol == "" or word_without_symbol not in stop_words):
            shingle_len -= 1

        if (shingle_len == 2 and stop_words_counter == 0) and separated_text[i].lower() not in stop_words and\
                re.search(stop_symbols, separated_text[i]) and (word_without_symbol == "" or word_without_symbol not in stop_words):
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
def GetSimilarAreasDefinition(text1_dictionary: Dict[int, str],
                              compared_texts: Dict[Union[int, str], List[Union[int, str]]],
                              text_type=0)\
        -> Union[Dict[Union[int, str], List[Union[int, str]]], List[str]]:
    areas = []
    new_list_of_areas = []
    list_of_areas = []
    defined_area = ""
    word = ""
    areas_str = ""
    last_words_string = ""
    for i in range(len(compared_texts)):
        local_areas = []
        for k in range(len(list(compared_texts.values())[i])):
            if list(compared_texts.values())[i][k] in text1_dictionary:
                local_areas.append((text1_dictionary.get(list(compared_texts.values())[i][k])))
        areas.append(local_areas)

    for k in range(len(areas)):
        for i in range(len(areas[k])):
            new_list_of_areas.append(areas[k][i].split(' '))
            counter = 0
            middle_words = ""
            for j in range(len(new_list_of_areas[i])):

                view_var_delete_later = new_list_of_areas[i][j]

                word_without_punct = PunctuationRemoval(new_list_of_areas[i][j])
                if new_list_of_areas[i][j].lower() not in stop_words and re.search(stop_symbols, new_list_of_areas[i][j]) \
                        and (word_without_punct == new_list_of_areas[i][j] or word_without_punct not in stop_words):
                    counter += 1

                if counter == 2 or counter == 3:
                    middle_words += new_list_of_areas[i][j] + ' '
                if counter == 4:
                    middle_words = re.sub(r'\s$', "", middle_words)

                if middle_words not in defined_area and counter > 3:
                    defined_area += " #" + ' '.join(new_list_of_areas[i])
                    break

                if counter == 4:
                    last_words_string += ' ' + new_list_of_areas[i][j]

            defined_area += last_words_string
            last_words_string = ""

        list_of_local_areas = defined_area.split('#')

        del list_of_local_areas[0:k+1]
        list_of_areas.append(list_of_local_areas)

    if text_type:
        dict_of_areas = {}
        for i in range(len(list_of_areas)):
            dict_of_areas.update({list(compared_texts.keys())[i]: list_of_areas[i]})
        return dict_of_areas
    else:
        return list_of_areas[0]


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
    # text1 = u'Київ здавна розташовувався на перетині важливих шляхів. Ще за Київської Русі таким шляхом був ' \
    #         u'легендарний Шлях із варягів у греки. Після цього промий його під холодною водою. Нині місто перетинають ' \
    #         u'міжнародні автомобільні та залізничні шляхи. Потім висип рис в каструлю з киплячою підсоленою водою. ' \
    #         u'Пропорції: 1 стакан дикого рису на 3 склянки води На сучасній території України відомі поселення ' \
    #         u'багатьох археологічних культур, починаючи з доби палеоліту — мустьєрської, гребениківської, кукрецької, ' \
    #         u'трипільської, середньостогівської, ямної, бойових сокир, чорноліської тощо.'
    #
    # text2 = u'Київ здавна розташовувався на перетині важливих шляхів. Ще за Київської Русі таким шляхом був ' \
    #         u'легендарний Шлях із варягів у греки. Нині місто перетинають міжнародні автомобільні та залізничні ' \
    #         u'шляхи. На сучасній території України відомі поселення багатьох археологічних культур, починаючи з доби ' \
    #         'палеоліту — мустьєрської, гребениківської, кукрецької, трипільської, середньостогівської, ямної, ' \
    #         u'бойових сокир, чорноліської тощо. Епітет — це слово чи словосполучення, завдяки особливій функції в ' \
    #         u'тексті, допомагає слову набути нового значення або смислового відтінку, підкреслює характерну рису, ' \
    #         u'визначальну якість певного предмету або явища, збагачує мову новим емоційним сенсом, додає до тексту ' \
    #         u'певної мальовничості та насиченості. Місто розташоване на півночі України, на межі Полісся і лісостепу ' \
    #         u'по обидва береги Дніпра в його середній течії.'

    text1 = u'Python (найчастіше вживане прочитання — «Па́йтон», запозичено назву[5] з британського шоу Монті Пайтон) ' \
            u'— інтерпретована об\'єктно-орієнтована мова програмування високого рівня зі строгою динамічною ' \
            u'типізацією.[6] Розроблена в 1990 році Гвідо ван Россумом. Структури даних високого рівня разом із ' \
            u'динамічною семантикою та динамічним зв\'язуванням роблять її привабливою для швидкої розробки програм, ' \
            u'а також як засіб поєднування наявних компонентів. Python підтримує модулі та пакети модулів, ' \
            u'що сприяє модульності та повторному використанню коду. Інтерпретатор Python та стандартні бібліотеки ' \
            u'доступні як у скомпільованій, так і у вихідній формі на всіх основних платформах. В мові програмування ' \
            u'Python підтримується кілька парадигм програмування, зокрема: об\'єктно-орієнтована, процедурна, ' \
            u'функціональна та аспектно-орієнтована. ЗАСТОСУВАННЯ НЕЙРОМЕРЕЖ ДЛЯ ІНФОРМАЦІЙНОГО ПОШУКУ Застосування ' \
            u'нейромереж для задач інформаційного пошуку може значно покращити швидкість та точність пошуку. Сутність ' \
            u'методу полягає в властивості нейромережі до навчання, тобто при правильному алгоритмі результат роботи ' \
            u'програми буде все точніше й точніше, а завдяки зібраному досвіду шлях вирішення задачі буде також ' \
            u'зменшуватись, що прискорить появу результату. Мінусами цього методу є велика вартість в грошових та ' \
            u'обчислювальних ресурсах і значні потреби в часі на розробку, тестування, розгортання та навчання ' \
            u'нейромережі. Розглянемо застосування методу на прикладі реалізації пошукової системи. '

    text2 = u'Матеріал з Вікіпедії — вільної енциклопедії. Python (найчастіше вживане прочитання — «Па́йтон», ' \
            u'запозичено назву[5] з британського шоу Монті Пайтон) — інтерпретована об\'єктно-орієнтована мова ' \
            u'програмування високого рівня зі строгою динамічною типізацією.[6] Розроблена в 1990 році Гвідо ван ' \
            u'Россумом. Структури даних високого рівня разом із динамічною семантикою та динамічним зв\'язуванням ' \
            u'роблять її привабливою для швидкої розробки програм, а також як засіб поєднування наявних компонентів. ' \
            u'Python підтримує модулі та пакети модулів, що сприяє модульності та повторному використанню коду. ' \
            u'Інтерпретатор Python та стандартні бібліотеки доступні як у скомпільованій, так і у вихідній формі на ' \
            u'всіх основних платформах. В мові програмування Python підтримується кілька парадигм програмування, ' \
            u'зокрема: об\'єктно-орієнтована, процедурна, функціональна та аспектно-орієнтована. Серед основних її ' \
            u'переваг можна назвати такі: чистий синтаксис (для виділення блоків слід використовувати відступи); ' \
            u'переносність програм (що властиве більшості інтерпретованих мов); стандартний дистрибутив має велику ' \
            u'кількість корисних модулів (включно з модулем для розробки графічного інтерфейсу); можливість ' \
            u'використання Python в діалоговому режимі (дуже корисне для експериментування та розв\'язання простих ' \
            u'задач); стандартний дистрибутив має просте, але разом із тим досить потужне середовище розробки, ' \
            u'яке зветься IDLE і яке написане мовою Python; зручний для розв\'язання математичних проблем (має засоби ' \
            u'роботи з комплексними числами, може оперувати з цілими числами довільної величини, у діалоговому режимі ' \
            u'може використовуватися як потужний калькулятор); відкритий код (можливість редагувати його іншими ' \
            u'користувачами). Python має ефективні структури даних високого рівня та простий, але ефективний підхід ' \
            u'до об\'єктно-орієнтованого програмування. Елегантний синтаксис Python, динамічна обробка типів, ' \
            u'а також те, що це інтерпретована мова, роблять її ідеальною для написання скриптів та швидкої розробки ' \
            u'прикладних програм у багатьох галузях на більшості платформ. Інтерпретатор мови Python і багата ' \
            u'Стандартна бібліотека (як вихідні тексти, так і бінарні дистрибутиви для всіх основних операційних ' \
            u'систем) можуть бути отримані з сайту Python www.python.org, і можуть вільно розповсюджуватися. Цей ' \
            u'самий сайт має дистрибутиви та посилання на численні модулі, програми, утиліти та додаткову ' \
            u'документацію. Інтерпретатор мови Python може бути розширений функціями та типами даних, розробленими на ' \
            u'C чи C＋＋ (або на іншій мові, яку можна викликати із C). Python також зручна як мова розширення для ' \
            u'прикладних програм, що потребують подальшого налагодження. Ця стаття потребує істотної переробки. ' \
            u'Можливо, її необхідно доповнити, переписати або вікіфікувати.Пояснення причин та обговорення — на ' \
            u'сторінці Вікіпедія:Статті, що необхідно поліпшити. Розробка мови Python була розпочата в кінці 1980-х ' \
            u'років[7] співробітником голландського інституту CWI Гвідо ван Россумом. Для розподіленої ОС Amoeba ' \
            u'потрібна була розширювана скриптова мова, і Гвідо почав писати Python на дозвіллі, запозичивши деякі ' \
            u'напрацювання для мови ABC[en] (Гвідо брав участь у розробці цієї мови, орієнтованої на навчання ' \
            u'програмування). У лютому 1991 року Гвідо опублікував вихідний текст в групі новин alt.sources[8]. Мова ' \
            u'почала вільно поширюватися через Інтернет і сподобалася іншим програмістам. З 1991 року Python є цілком ' \
            u'об\'єктно-орієнтованим. Python також запозичив багато рис таких мов, як C, C++, Modula-3[en] і Icon[' \
            u'en], й окремі риси функціонального програмування з Ліспу. Назва мови виникла зовсім не від виду ' \
            u'плазунів. Автор назвав мову на честь популярного британського комедійного серіалу 70-х років ' \
            u'«Повітряний цирк Монті Пайтона». Втім, все одно назву мови частіше асоціюють саме зі змією, ' \
            u'ніж з фільмом — піктограми файлів в KDE або в Windows, і навіть емблема на сайті python.org зображують ' \
            u'зміїну голову. 3 грудня 2008 року[10], після тривалого тестування, вийшла перша версія Python 3000 (або ' \
            u'Python 3.0, також використовується скорочена Py3k). У Python 3000 усунено багато недоліків архітектури ' \
            u'з максимально можливим (але не повним) збереженням сумісності зі старішими версіями. На сьогодні ' \
            u'підтримуються обидві гілки розвитку (Python 3.7 і 2.7). Розробники мови Python є прихильниками певної ' \
            u'філософії '

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

    # canonized_text1 = Canonize(text1)
    # print(canonized_text1)

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

    print(similar_areas)
    #
    # print(SplitText(text1, similar_areas))
    #
    # print(text1)
