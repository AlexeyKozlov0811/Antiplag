from hashlib import sha512

#function encrypts recieved text into hash code

def encryption (text):
    encrypted_text = sha512(text.encode()).hexdigest()
    return encrypted_text

if (__name__=="__main__"):
    text = "В данной статье мы рассмотрим встроенные средства python для работы с файлами: открытие / закрытие, чтение и запись. Итак, начнем. Прежде, чем работать с файлом, его надо открыть. С этим замечательно справится встроенная функция open:"
    print(encryption(text))