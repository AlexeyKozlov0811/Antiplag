from hash_encryption import encryption
import re

myfile_1 = open("text_1.txt", "r", encoding = 'utf-8')
text_1 = myfile_1.read()

myfile_2 = open("text_2.txt", "r", encoding = 'utf-8')
text_2 = myfile_2.read()

encrypted_text_1 = encryption (text_1)
encrypted_text_2 = encryption (text_2)

if encrypted_text_1 == encrypted_text_2:
    print('Texts are similar')
else:
    parahraph_1 = text_1.split('\n')
    parahraph_2 = text_2.split('\n')
    same_par_1 = []
    same_par_2 = []

    for i in range(len(parahraph_1)):
        for j in range(len(parahraph_2)):
          if parahraph_1[i] == parahraph_2[j]:
              same_par_1.append(parahraph_1[i])
              same_par_2.append(parahraph_2[j])

    parahraph_1 = list(frozenset(parahraph_1) ^ frozenset(same_par_1))
    parahraph_2 = list(frozenset(parahraph_2) ^ frozenset(same_par_2))

    parahraph_1 = ''.join(parahraph_1)
    parahraph_2 = ''.join(parahraph_2)

    #print(parahraph_2)
    
    sentences_1 = re.split("[.!?]+", parahraph_1)
    sentences_2 = re.split("[.!?]+", parahraph_2)
    
    same_sent_1 = []
    same_sent_2 = []

    #print(sentences_1)

    for i in range(len(sentences_1)):
        for j in range(len(sentences_2)):
          if sentences_1[i] == sentences_2[j]:
              same_sent_1.append(sentences_1[i])
              same_sent_2.append(sentences_2[j])
    sentences_1 = list(frozenset(sentences_1) ^ frozenset(same_sent_1))
    original = ''.join(sentences_1)
    print(original)

    #разобраться с порядком!


myfile_1.close()
myfile_2.close()