from Crypto.Cipher import DES
 
key = b'abcdefgh'
des = DES.new(key, DES.MODE_ECB)
 
# function which can fill any line with spaces until it is a multiple of 8
# the string we encrypt must be a multiple of 8, because DES encryption key size is 8 bytes

def pad(text):
    while len(text) % 8 != 0:
        text += b' '
    return text

#function that encrypts text

def DES_encrypting(text):
    
    
    padded_text = pad(text.encode())
 
    encrypted_text = des.encrypt(padded_text)
    return encrypted_text

#function that decrypts text

def DES_decrypting(encryption):
    decrypted_text = des.decrypt(encryption)

    return decrypted_text.decode("utf-8")


if (__name__=="__main__"):
    text = "В данной статье мы рассмотрим встроенные средства python для работы с файлами: открытие / закрытие, чтение и запись. Итак, начнем. Прежде, чем работать с файлом, его надо открыть. С этим замечательно справится встроенная функция open:"
    enc = DES_encrypting(text)
    print("Encrypted text: ", enc, "\n\n")
    print ("Decryption: ",  DES_decrypting(enc), "\n\n")