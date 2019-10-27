# coding=utf-8
# from hash_encryption import encryption
import binascii
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer(lang='uk')


def canonize(source):
    stop_symbols = '[].,!?:;-\'\"—\n\r()'
    stop_words = (u'і', u'й', u'так',  # сполучники
                  u'а', u'але', u'та',
                  u'бо', u'як', u'що',
                  u'на', u'ніби', u'неначе',
                  u'якже', u'якби', u'якщо',
                  u'проте', u'зате', u'як',
                  u'де', u'тому що', u'доки',
                  u'мов', u'наче', u'немов',
                  u'цебто', u'оскільки', u'однак',
                  u'тільки', u'хоч', u'хай',
                  u'аби', u'відтоді', u'тобто',
                  u'нібито', u'щоб', u'аби',
                  u'без', u'біля', u'до',  # прийменники
                  u'зза', u'ізза', u'проти',
                  u'серед', u'назустріч', u'напереріз',
                  u'наперекір', u'усупереч', u'навздогін',
                  u'над', u'під', u'перед',
                  u'поза', u'на', u'об',
                  u'о', u'по', u'з',
                  u'із', u'зі', u'між',
                  u'за', u'у', u'в',
                  u'відповідно до', u'для', u'до',
                  u'через', u'тощо',
                  u'я', u'ми', u'ти',  # займенники
                  u'ви', u'він', u'вона',
                  u'воно', u'вони', u'себе',
                  u'мій', u'твій', u'наш',
                  u'свій', u'ваш', u'його',
                  u'її', u'їх', u'їхній',
                  u'той', u'цей', u'такий',
                  u'стільки')

    text_cleaning = [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)]
    cleaned_text = []
    for i in range(len(text_cleaning)):
        cleaned_text.append(morph.parse(text_cleaning[i])[0].normal_form)
    return cleaned_text
    # return ([x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)])


# generates shingles, if key = 1, that means that we make shingles out of canonized text, if key = 0, ...out of hashes
def shingle_generation(source, key):
    shingle_len = 4  # длина шингла
    out = []
    words = []
    words_crc = []
    for i in range(len(source) - (shingle_len + 1)):
        if key == 1:
            words.append(' '.join([x for x in source[i:i + shingle_len]]))
            words_crc.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))
        out.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))
    words_dict = dict(zip(words_crc, words))  # zip -  creates dictionary where keys are elements of words_crc
    if key == 1:
        return words_dict
    return out


# compares texts and returns list of similar hashed shingles
def comparation(source1, source2):
    same = 0
    similar_phrases = []
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1
            similar_phrases.append(source1[i])
    return similar_phrases


# puts together all the words that
def similar_areas_definition(text1_dictionary, compared_texts):
    areas = []
    for k in range(len(compared_texts)):
        if compared_texts[k] in text1_dictionary:
            areas.append((text1_dictionary.get(compared_texts[k])))
        else:
            print("false")
    new = []
    for l in range(len(areas)):
        new.append(areas[l].split(' '))
    areas = new
    defined_area = []
    for i in range(len(areas)):
        for j in range((len(areas[i]))):
            if i+1 < (len(areas)):
                if areas[i][j] != areas[i+1][j - 1]:
                    defined_area.append(areas[i][j])

    defined_area = defined_area + areas[(len(areas)-1)]
    return defined_area


# counts the percentage of two texts, will be changed later
def similarity_percentage_calculation(source1, source2, same):
    return len(same) / float(len(source1) + len(source2) - len(same)) * 100


if __name__ == "__main__":
    text2 = u'На сучасній території України відомі поселення багатьох археологічних культур, починаючи з доби ' \
            u'палеоліту — мустьєрської, гребениківської, кукрецької, трипільської, середньостогівської, ямної, ' \
            u'бойових сокир, чорноліської тощо. В античні часи на території України виникли державні утворення ' \
            u'скіфів, давньогрецьких колоністів, готів, але відправним пунктом української слов\'янської державності ' \
            u'й культури вважається Київська Русь IX—XIII століть. Після монгольської навали її спадкоємцем стало ' \
            u'Руське королівство XIII—XIV століття. Воно було поглинуте сусідніми Литвою та Польщею, ' \
            u'об\'єднаними з XVI століття у федеративну Річ Посполиту.'  # Текст 1 для сравнения

    text1 = u'На сучасній території України відомі поселення багатьох археологічних культур, починаючи з доби ' \
            u'палеоліту — мустьєрської, гребениківської, кукрецької, трипільської, середньостогівської, ямної, ' \
            u'бойових сокир, чорноліської тощо. Как видно из примера, присвоение по новому ключу расширяет словарь, ' \
            u'присвоение по существующему ключу перезаписывает его, а попытка извлечения несуществующего ключа ' \
            u'порождает исключение.'  # Текст 2 для сравнения

    shingle_dict = shingle_generation(canonize(text1), 1)

    shingled_canonized_text1 = shingle_generation(canonize(text1), 0)
    shingled_canonized_text2 = shingle_generation(canonize(text2), 0)

    similar = comparation(shingled_canonized_text1, shingled_canonized_text2)

    print(similar_areas_definition(shingle_dict, similar))

    print(similarity_percentage_calculation(shingled_canonized_text1, shingled_canonized_text2, similar))
