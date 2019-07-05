from .hash_encryption import encryption
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()


def canonize(source):
        source = str(source)
        stop_symbols = '[].,!?:;-\'\"—\n\r()'

        stop_words = (u'і', u'й', u'так', #сполучники
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
        u'без', u'біля', u'до', #прийменники
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
        u'я', u'ми', u'ти', #займенники
        u'ви', u'він', u'вона',
        u'воно', u'вони', u'себе',
        u'мій', u'твій', u'наш',
        u'свій', u'ваш', u'його',
        u'її', u'їх', u'їхній',
        u'той', u'цей', u'такий',
        u'стільки')

        cleaned_text = [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)]
        o =[]
        for i in range(len(cleaned_text)):
            o.append(morph.parse(cleaned_text[i])[0].normal_form)
        return (o)
        #return ([x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)])



def genshingle(source):
    source = str(source)
    import binascii
    shingleLen = 10 #длина шингла
    out = [] 
    for i in range(len(source)-(shingleLen - 1)):
        out.append (binascii.crc32(' '.join( [x for x in source[i:i+shingleLen]] ).encode('utf-8')))

    return out

def compaire(source1, source2):
    source1 = str(source1)
    source2 = str(source2)
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1
    print(same)
    return same/float(len(source1))*100

def compaire_texts(text1, text2):
    return (compaire(genshingle(canonize(text1)), genshingle(canonize(text2))))

if (__name__=="__main__"):
    text1 =u'The Rolling Stones (Роллинг Стоунз[2][3], МФА: [ˈrəʊ.lɪŋ stəʊnz]; букв. с англ. «катящиеся камни», идиоматический перевод — «вольные странники» или бродяги[4]) — британская рок-группа, образовавшаяся 12 июля 1962 года и многие годы соперничавшая по популярности с The Beatles. The Rolling Stones, ставшие важной частью Британского вторжения, считаются одной из самых влиятельных и успешных групп в истории рока[5]. The Rolling Stones, которые по замыслу менеджера Эндрю Луга Олдэма должны были стать «бунтарской» альтернативой The Beatles, уже в 1969 году в ходе американского турне рекламировались как «величайшая рок-н-ролльная группа в мире» и (согласно Allmusic) сумели сохранить этот статус по сей день[1].'
    text3 = u'В античні часи на території України виникли державні утворення скіфів, давньогрецьких колоністів, готів, але відправним пунктом української слов\'янської державності й культури вважається Київська Русь IX—XIII століть [5].' # Текст 1 для сравнения
    text2 = u'На сучасній території України відомі поселення багатьох археологічних культур, починаючи з доби палеоліту — мустьєрської, гребениківської, кукрецької, трипільської, середньостогівської, ямної, бойових сокир, чорноліської тощо. В античні часи на території України виникли державні утворення скіфів, давньогрецьких колоністів, готів, але відправним пунктом української слов\'янської державності й культури вважається Київська Русь IX—XIII століть [5]. Після монгольської навали її спадкоємцем стало Руське королівство XIII—XIV століття [5]. Воно було поглинуте сусідніми Литвою та Польщею, об\'єднаними з XVI століття у федеративну Річ Посполиту.' # Текст 2 для сравнения
    # print(len(text2.split()))

    cmp1 = genshingle(canonize(text1))
    cmp2 = genshingle(canonize(text2))

    print (compaire(cmp1, cmp2))

##    print(compaire_texts(text1, text2))
