from Crypto.Cipher import DES
 
myfile = open("some_text.txt", "r", encoding = 'utf-8')
some_text = myfile.read()
print(some_text)
print('\n\n\n')

key = b'abcdefgh'
 
def pad(text):
    while len(text) % 8 != 0:
        text += b' '
    return text
 
des = DES.new(key, DES.MODE_ECB)
padded_text = pad(some_text.encode())
 
encrypted_text = des.encrypt(padded_text)
#myfile_enc = open("enc_text.txt", "wb")
#some_text_1 = myfile_enc.write(encrypted_text)
print(encrypted_text)
print('\n\n\n')

decrypted_text = des.decrypt(encrypted_text)
#myfile_dec = open ("dec_text.txt", "w", encoding = 'utf-8')
#some_text_2 = myfile_dec.write(decrypted_text.decode("utf-8"))
print(decrypted_text.decode("utf-8")) 
print('\n\n\n')

#myfile_dec.close()
#myfile_enc.close()

myfile.close()

