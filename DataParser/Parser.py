from bs4 import BeautifulSoup
import requests
import settings
from math import ceil

#function open webpage and checking exceptions and return its html code or 0 in case of failure
def get_HTML(url):
    try:
        Search_request = requests.get(url)
        Search_request.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return 0
    except requests.exceptions.ConnectionError as err:
        print(err)
        return 0
    except requests.exceptions.URLRequired as err:
        print(err)
        return 0
    except requests.exceptions.TooManyRedirects as err:
        print(err)
        return 0
    except requests.exceptions.Timeout as err:
        print(err)
        return 0
    except requests.exceptions.RequestException as err:
        print(err)
        return 0
    else:
        return Search_request

#function parsing search result
def search_parsing(query):
    result=[]
    url ='http://www.google.com/search?q='
    page ='&start='
    for number in range(settings.pages):
        Search_request = get_HTML(url + query + page+str(number*10))
        if (Search_request!=0):
            soup = BeautifulSoup(Search_request.text,"html.parser")
            links = soup.find_all('div',class_="BNeawe UPmit AP7Wnd")
            for link in links:
                if((link.string.rfind('youtube') == -1) and (link.string.rfind('yandex') == -1) and (link.string.rfind('mail.ru') == -1) and (link.string.rfind('.jpg') == -1) and (link.string.rfind('.png') == -1) and (link.string.rfind('.gif')) == -1):
                    result.append(link.string.replace(" › ","/"))
    return result

#function parsing web page and extracts its textual content
def get_content(url):
    Clear_text=""
    Web_resource=get_HTML(url)
    if (Web_resource!=0):
        soup = BeautifulSoup(Web_resource.text,"html.parser")
        for script in soup(["script", "style"]): #ignore javascript code
            script.extract()
        text = soup.get_text().split("\n")
        for phrase in text:
            if((phrase!='') and ((phrase[-1]=='.') or (phrase[-1]=='?') or (phrase[-1]=='!') or (phrase[-1]==':') or (phrase[-1]==';'))):
                Clear_text+=str(phrase)
                Clear_text+="\n"
        del text
        return Clear_text
    else:
        return 0

#function divides text into 32-word phrases
def split_query(query):
    phrases=[]
    phrase = query.split()
    words = len(phrase)
    parts = words/32
    if (int(parts)!=float(parts)):
        parts=ceil(parts)
    for part in range(parts):
        phrases.append(" ".join(phrase[32*(part-1):32*part]))
    del phrases[0]
    return phrases
    



if (__name__=="__main__"):
    query="Матеріал з Вікіпедії — вільної енциклопедії. Python (найчастіше вживане прочитання — «Па́йтон», запозичено назву[5] з британського шоу Монті Пайтон) — інтерпретована об'єктно-орієнтована мова програмування високого рівня зі строгою динамічною типізацією.[6] Розроблена в 1990 році Гвідо ван Россумом. Структури даних високого рівня разом із динамічною семантикою та динамічним зв'язуванням роблять її привабливою для швидкої розробки програм, а також як засіб поєднування наявних компонентів. Python підтримує модулі та пакети модулів, що сприяє модульності та повторному використанню коду. Інтерпретатор Python та стандартні бібліотеки доступні як у скомпільованій, так і у вихідній формі на всіх основних платформах. В мові програмування Python підтримується кілька парадигм програмування, зокрема: об'єктно-орієнтована, процедурна, функціональна та аспектно-орієнтована. Серед основних її переваг можна назвати такі: чистий синтаксис (для виділення блоків слід використовувати відступи); переносність програм (що властиве більшості інтерпретованих мов); стандартний дистрибутив має велику кількість корисних модулів (включно з модулем для розробки графічного інтерфейсу); можливість використання Python в діалоговому режимі (дуже корисне для експериментування та розв'язання простих задач); стандартний дистрибутив має просте, але разом із тим досить потужне середовище розробки, яке зветься IDLE і яке написане на мові Python; зручний для розв'язання математичних проблем (має засоби роботи з комплексними числами, може оперувати з цілими числами довільної величини, у діалоговому режимі може використовуватися як потужний калькулятор); відкритий код (можливість редагувати його іншими користувачами). Python має ефективні структури даних високого рівня та простий, але ефективний підхід до об'єктно-орієнтованого програмування. Елегантний синтаксис Python, динамічна обробка типів, а також те, що це інтерпретована мова, роблять її ідеальною для написання скриптів та швидкої розробки прикладних програм у багатьох галузях на більшості платформ. Інтерпретатор мови Python і багата Стандартна бібліотека (як вихідні тексти, так і бінарні дистрибутиви для всіх основних операційних систем) можуть бути отримані з сайту Python www.python.org, і можуть вільно розповсюджуватися. Цей самий сайт має дистрибутиви та посилання на численні модулі, програми, утиліти та додаткову документацію. Інтерпретатор мови Python може бути розширений функціями та типами даних, розробленими на C чи C＋＋ (або на іншій мові, яку можна викликати із C). Python також зручна як мова розширення для прикладних програм, що потребують подальшого налагодження. Ця стаття потребує істотної переробки.  Можливо, її необхідно доповнити, переписати або вікіфікувати.Пояснення причин та обговорення — на сторінці Вікіпедія:Статті, що необхідно поліпшити. Розробка мови Python була розпочата в кінці 1980-х років[7] співробітником голландського інституту CWI Гвідо ван Россумом. Для розподіленої ОС Amoeba потрібна була розширювана скриптова мова, і Гвідо почав писати Python на дозвіллі, запозичивши деякі напрацювання для мови ABC[en] (Гвідо брав участь у розробці цієї мови, орієнтованої на навчання програмування). У лютому 1991 року Гвідо опублікував вихідний текст в групі новин alt.sources[8]. Мова почала вільно поширюватися через Інтернет і сподобалася іншим програмістам. З 1991 року Python є цілком об'єктно-орієнтованим. Python також запозичив багато рис таких мов, як C, C++, Modula-3[en] і Icon[en], й окремі риси функціонального програмування з Ліспу. Назва мови виникла зовсім не від виду плазунів. Автор назвав мову на честь популярного британського комедійного серіалу 70-х років «Повітряний цирк Монті Пайтона». Втім, все одно назву мови частіше асоціюють саме зі змією, ніж з фільмом — піктограми файлів в KDE або в Windows, і навіть емблема на сайті python.org зображують зміїну голову. 3 грудня 2008 року[10], після тривалого тестування, вийшла перша версія Python 3000 (або Python 3.0, також використовується скорочена Py3k). У Python 3000 усунено багато недоліків архітектури з максимально можливим (але не повним) збереженням сумісності зі старішими версіями. На сьогодні підтримуються обидві гілки розвитку (Python 3.7 і 2.7). Розробники мови Python є прихильниками певної філософії програмування, яку називають «The Zen of Python» («Дзен Пайтона»)[11]. Її текст можна отримати у інтерпретаторі Python за допомогою команди import this (лише один раз за сесію). Автором цієї філософії вважається Тім Пейтерс."
    print(get_content(search_parsing(split_query(query)[0])[0]))


