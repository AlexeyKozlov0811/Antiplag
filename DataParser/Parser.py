from bs4 import BeautifulSoup
import requests
import settings

#function open webpage and checking exceptions and return its html code or 0 in case of failure 
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

#function parsing search result
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

#function parsing web page and extracts its textual content
def Get_content(url):
    Clear_text=[]
    Web_resource=GetHTML(url)
    if (Web_resource!=0):
        soup = BeautifulSoup(Web_resource.text,"html.parser")   
        for script in soup(["script", "style"]): #ignore javascript code
            script.extract()
        text = soup.get_text().split("\n")
        for phrase in text:
            if((phrase!='') and ((phrase[-1]=='.') or (phrase[-1]=='?') or (phrase[-1]=='!') or (phrase[-1]==':') or (phrase[-1]==';'))):
                Clear_text.append(phrase)
        del text
        return Clear_text
    else:
        return 0



if (__name__=="__main__"):
    print(Search_parsing("Python"))
    print("\n\n")
    
    text=Get_content(Search_parsing("Python")[2])
    for a in text:
        print(a)

   
