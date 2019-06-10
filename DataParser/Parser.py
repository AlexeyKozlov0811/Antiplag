from bs4 import BeautifulSoup
import requests
import settings


def GetHTML(url):
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


def Search_parsing(query):
    result=[]
    url ='http://www.google.com/search?q='
    page ='&start='
    for number in range(settings.pages):
        Search_request = GetHTML(url + query + page+str(number*10))
        if (Search_request!=0):
            soup = BeautifulSoup(Search_request.text,"html.parser")
            links = soup.find_all('div',class_="BNeawe UPmit AP7Wnd")
            for link in links:
                if((link.string.rfind('youtube') == -1) and (link.string.rfind('yandex') == -1) and (link.string.rfind('mail.ru') == -1) and (link.string.rfind('.jpg') == -1) and (link.string.rfind('.png') == -1) and (link.string.rfind('.gif')) == -1):     
                    result.append(link.string.replace(" › ","/"))
    return result




if (__name__=="__main__"):
   print(Search_parsing("Python"))
