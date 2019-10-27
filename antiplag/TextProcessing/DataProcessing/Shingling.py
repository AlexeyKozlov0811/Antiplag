# coding=utf-8
# from hash_encryption import encryption
import binascii
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer(lang="uk")


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


def gen_shingle(source, key):
    shingle_len = 4  # длина шингла
    out = []
    words = []
    words_crc = []
    for i in range(len(source) - (shingle_len + 1)):
        if key == 1:
            words.append(' '.join([x for x in source[i:i + shingle_len]]))
            words_crc.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))
        out.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))
    words_dict = dict(zip(words_crc, words))
    if key == 1:
        return words_dict
    return out


def compare(source1, source2):
    same = 0
    s = []
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1
            s.append(source1[i])
    # print(len(s))
    # print(s)
    return s
    # return same / float(len(source1) + len(source2) - same) * 100
    # return same*2/float(len(source1) + len(source2))*100


def similarity_percentage(source1, source2, same):
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
            u'бойових сокир, чорноліської тощо. Після монгольської навали її спадкоємцем стало ' \
            u'Руське королівство XIII—XIV століття.'  # Текст 2 для сравнения

    # text2 = u'В античні часи на території України виникли державні утворення скіфів, давньогрецьких колоністів,
    # готів, але відправним пунктом української слов\'янської державності й культури вважається Київська Русь IX—XIII
    # століть.' # Текст 2 для сравнения

    # print(len(text2.split()))

    shingle_dict = gen_shingle(canonize(text1), 1)

    cmp1 = gen_shingle(canonize(text1), 0)
    cmp2 = gen_shingle(canonize(text2), 0)

    # print(cmp1, "\n\n")
    # print(cmp2, "\n\n")

    # hashed_str1 = []
    # str1 = canonize(text1)
    # str1_ = ' '.join(str1)
    #
    # for j in range(len(str1)):
    #     hashed_str1.append(binascii.crc32(' '.join(str1_[j]).encode('utf-8')))
    #
    # hashed_str1_and_str1 = dict(zip(hashed_str1, str1))
    #
    # print(hashed_str1_and_str1, "\n\n")
    print(cmp1, "\n\n")

    similar = compare(cmp1, cmp2)
    print(shingle_dict, "\n\n")
    print(similarity_percentage(cmp1, cmp2, similar), "\n\n")
    # print(len(compare(cmp1, cmp2)))

    a = []
    for k in range(len(shingle_dict)):
        if cmp1[k] in shingle_dict:
            a.append((shingle_dict.get(cmp1[k])))
        else:
            print("false")
    print(a)
