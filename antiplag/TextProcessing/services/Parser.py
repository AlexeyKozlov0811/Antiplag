"""
Module contains business-logic responsible for finding fragments of text in web
"""
import math
import requests
from typing import Union, List
from bs4 import BeautifulSoup
from django.conf import settings


# function returns web page html code or 0 in case of failure
def GetHTML(url: str) -> Union[int, requests.Response]:
    try:
        HTMLCode = requests.get(url)
    except requests.exceptions.RequestException:
        return 0
    else:
        return HTMLCode


# function parsing search result
def GetSearchQueryResult(search_query: str) -> List[str]:
    QueryResultUrls = []
    SearchUrl = 'http://www.google.com/search?q=' + search_query + '&start='
    for NumOfPage in range(pages_of_search):
        SearchResult = GetHTML(SearchUrl + str(NumOfPage * 10))
        if SearchResult:
            QueryResultUrls = GetCleanLink(SearchResult)
    return QueryResultUrls


# function cleans correct link
def GetCleanLink(search_result: Union[int, requests.Response]) -> List[str]:
    ClearedLinks = []
    soup = BeautifulSoup(search_result.text, "html.parser")
    AllLinks = soup.find_all('div', class_="BNeawe UPmit AP7Wnd")
    for Link in AllLinks:
        LinkIsCorrect = (Link.string.rfind('youtube') == -1) and (Link.string.rfind('yandex') == -1) and \
                        (Link.string.rfind('mail.ru') == -1) and (Link.string.rfind('.jpg') == -1) and (
                                Link.string.rfind('.png') == -1) and (Link.string.rfind('.gif')) == -1
        if LinkIsCorrect:
            ClearedLinks.append(Link.string.replace(" › ", "/"))
    return ClearedLinks


# function extracts web page textual content
def GetWebContent(url: str) -> str:
    CleanText = ""
    WebResource = GetHTML(url)
    if WebResource:
        HTMLCode = BeautifulSoup(WebResource.text, "html.parser")
        for Script in HTMLCode(["script", "style"]):
            Script.extract()
        Text = HTMLCode.get_text().split("\n")
        for Phrase in Text:
            PhraseIsMeaningful = (Phrase != '') and (
                    (Phrase[-1] == '.') or (Phrase[-1] == '?') or (Phrase[-1] == '!') or (Phrase[-1] == ':') or (
                     Phrase[-1] == ';'))
            if PhraseIsMeaningful:
                CleanText += str(Phrase)
                CleanText += "\n"
        del Text
        return CleanText
    else:
        return "0"


# function divides text into 32-word phrases
def TextSeparation(text: str) -> List[str]:
    SeparatedPhrases = []
    ListOfWords = text.split()
    NumOfWords = len(ListOfWords)
    NumOfParts = math.ceil(NumOfWords / 32)
    for PartIdx in range(NumOfParts):
        SeparatedPhrases.append(" ".join(ListOfWords[32 * (PartIdx - 1): 32 * PartIdx]))
    del SeparatedPhrases[0]
    return SeparatedPhrases


# function finds text references in web
def FindTextUrls(text: str) -> List[str]:
    Urls = []
    AllParts = TextSeparation(text)
    for Query in AllParts:
        try:
            Urls += GetSearchQueryResult(Query)[0:search_results]
        except IndexError:
            return ["0"]
        else:
            return list(set(Urls))


# debug
if __name__ == "__main__":
    pages_of_search = 1
    search_results = 1
    query = "Матеріал з Вікіпедії — вільної енциклопедії. Python (найчастіше вживане прочитання — «Па́йтон», " \
            "запозичено назву[5] з британського шоу Монті Пайтон) — інтерпретована об'єктно-орієнтована мова " \
            "програмування високого рівня зі строгою динамічною типізацією.[6] Розроблена в 1990 році Гвідо ван " \
            "Россумом. Структури даних високого рівня разом із динамічною семантикою та динамічним зв'язуванням " \
            "роблять її привабливою для швидкої розробки програм, а також як засіб поєднування наявних компонентів. " \
            "Python підтримує модулі та пакети модулів, що сприяє модульності та повторному використанню коду. " \
            "Інтерпретатор Python та стандартні бібліотеки доступні як у скомпільованій, так і у вихідній формі на " \
            "всіх основних платформах. В мові програмування Python підтримується кілька парадигм програмування, " \
            "зокрема: об'єктно-орієнтована, процедурна, функціональна та аспектно-орієнтована. Серед основних її " \
            "переваг можна назвати такі: чистий синтаксис (для виділення блоків слід використовувати відступи); " \
            "переносність програм (що властиве більшості інтерпретованих мов); стандартний дистрибутив має велику " \
            "кількість корисних модулів (включно з модулем для розробки графічного інтерфейсу); можливість " \
            "використання Python в діалоговому режимі (дуже корисне для експериментування та розв'язання простих " \
            "задач); стандартний дистрибутив має просте, але разом із тим досить потужне середовище розробки, " \
            "яке зветься IDLE і яке написане на мові Python; зручний для розв'язання математичних проблем (має засоби " \
            "роботи з комплексними числами, може оперувати з цілими числами довільної величини, у діалоговому режимі " \
            "може використовуватися як потужний калькулятор); відкритий код (можливість редагувати його іншими " \
            "користувачами). Python має ефективні структури даних високого рівня та простий, але ефективний підхід до " \
            "об'єктно-орієнтованого програмування. Елегантний синтаксис Python, динамічна обробка типів, а також те, " \
            "що це інтерпретована мова, роблять її ідеальною для написання скриптів та швидкої розробки прикладних " \
            "програм у багатьох галузях на більшості платформ. Інтерпретатор мови Python і багата Стандартна " \
            "бібліотека (як вихідні тексти, так і бінарні дистрибутиви для всіх основних операційних систем) можуть " \
            "бути отримані з сайту Python www.python.org, і можуть вільно розповсюджуватися. Цей самий сайт має " \
            "дистрибутиви та посилання на численні модулі, програми, утиліти та додаткову документацію. Інтерпретатор " \
            "мови Python може бути розширений функціями та типами даних, розробленими на C чи C＋＋ (або на іншій мові, " \
            "яку можна викликати із C). Python також зручна як мова розширення для прикладних програм, що потребують " \
            "подальшого налагодження. Ця стаття потребує істотної переробки.  Можливо, її необхідно доповнити, " \
            "переписати або вікіфікувати.Пояснення причин та обговорення — на сторінці Вікіпедія:Статті, що необхідно " \
            "поліпшити. Розробка мови Python була розпочата в кінці 1980-х років[7] співробітником голландського " \
            "інституту CWI Гвідо ван Россумом. Для розподіленої ОС Amoeba потрібна була розширювана скриптова мова, " \
            "і Гвідо почав писати Python на дозвіллі, запозичивши деякі напрацювання для мови ABC[en] (Гвідо брав " \
            "участь у розробці цієї мови, орієнтованої на навчання програмування). У лютому 1991 року Гвідо " \
            "опублікував вихідний текст в групі новин alt.sources[8]. Мова почала вільно поширюватися через Інтернет " \
            "і сподобалася іншим програмістам. З 1991 року Python є цілком об'єктно-орієнтованим. Python також " \
            "запозичив багато рис таких мов, як C, C++, Modula-3[en] і Icon[en], й окремі риси функціонального " \
            "програмування з Ліспу. Назва мови виникла зовсім не від виду плазунів. Автор назвав мову на честь " \
            "популярного британського комедійного серіалу 70-х років «Повітряний цирк Монті Пайтона». Втім, " \
            "все одно назву мови частіше асоціюють саме зі змією, ніж з фільмом — піктограми файлів в KDE або в " \
            "Windows, і навіть емблема на сайті python.org зображують зміїну голову. 3 грудня 2008 року[10], " \
            "після тривалого тестування, вийшла перша версія Python 3000 (або Python 3.0, також використовується " \
            "скорочена Py3k). У Python 3000 усунено багато недоліків архітектури з максимально можливим (але не " \
            "повним) збереженням сумісності зі старішими версіями. На сьогодні підтримуються обидві гілки розвитку (" \
            "Python 3.7 і 2.7). Розробники мови Python є прихильниками певної філософії програмування, яку називають " \
            "«The Zen of Python» («Дзен Пайтона»)[11]. Її текст можна отримати у інтерпретаторі Python за допомогою " \
            "команди import this (лише один раз за сесію). Автором цієї філософії вважається Тім Пейтерс. "
    # print(get_content(search_parsing(text_separation(query)[0])[0]))
    # print(search_parsing(text_separation(query)[0]))
    print(FindTextUrls(query))
else:
    search_results = settings.SEARCH_RESULTS
    pages_of_search = search_results // 10 + 1
