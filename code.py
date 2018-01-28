# -*- coding: utf-8 -*-

# Importaciones de librerías requeridas
import re
import time
from tkinter import *
from collections import Counter
import textwrap

# Variables globales
path = "data/corpus.txt"
letters = {}
letters_pair = {}
words = {}
words_pair = {}
total_words = 0
total_letters = 0

encoding_dictionary = {
    '1': ['a', 'á', 'b', 'c'],
    '2': ['d', 'e', 'é', 'f'],
    '3': ['g', 'h', 'i', 'í'],
    '4': ['j', 'k', 'l'],
    '5': ['m', 'n', 'ñ', 'o', 'ó'],
    '6': ['p', 'q', 'r', 's'],
    '7': ['t', 'u', 'ú', 'v'],
    '8': ['w', 'x', 'y', 'z']
}

# Variable usada para medir los tiempos de ejecución
start_time = time.time()

# Método utilizado para realizar el conteo de las letras
def encoding(word):
  res = ''
    
  for letter in list(word):
    if letter == ' ':
      res += letter
      continue
    
    for key in encoding_dictionary:
      if letter in encoding_dictionary.get(key):
        res += key
        break
            
  return res

"""
Método utilizado para calcular la distancia entre dos palabras codificadas.
es utilizado para dar una palabra favorable en caso de no encontrar la
original en el diccionario.
"""
def manhattan_distance(a, b):
  distance = 0
  
  if len(a) > len(b):
    a, b = b, a
  
  for i, x in enumerate(a):
    if a[i] != b[i]:
      distance += 1

  distance += (len(b) - len(a))
  return distance

# Método utilizado para aplicar estadística a los distintos items, es decir,
# este método nos calcula la probabilidad de las palabras/letras en base al total de ellas.
def apply_statistics(items, total):
  for item in items:
    items[item][0] = items[item][0] / total_words

"""
En esta sección abrimos el fichero como lectura y con codificación utf8 para así tratar tildes, etc.
Además, sacamos todas las palabras y letras del corpus y realizamos el conteo de las mismas.
"""
with open(path, "r", encoding="utf8") as file:

  for line in file.readlines():
      
    line = re.sub('[^A-Za-z\u00C0-\u017F]+', ' ', line)
    line = re.sub('[\s]+', ' ', line)
          
    for word in map(lambda x: x.strip().lower(), line.split(' ')):
              
      if word in words:
        words[word][0] += 1
      else:
        words[word] = [1, encoding(word)]
          
      total_words += 1
          
      for letter in list(word):
          
        if letter in letters:
          letters[letter][0] += 1
        else:
          letters[letter] = [1, encoding(letter)]
              
        total_letters += 1
        
#Método que aplica estadística a todos los items        
apply_statistics(words, total_words)
apply_statistics(letters, total_letters)


"""
En esta sección abrimos el fichero como lectura y con codificación utf8 para así tratar tildes, etc.
Además, sacamos todas las palabras y letras del corpus y realizamos el conteo de las mismas para obtener así el bigram.
"""
with open(path, "r", encoding="utf8") as file2:
    
    corpus = ''
    for line in file2.readlines():
      
        line = re.sub('[^A-Za-z\u00C0-\u017F]+', ' ', line)
        line = re.sub('[\s]+', ' ', line)
        corpus += line
    
    #Pongo todo el corpus en minúsculas
    corpus = corpus.lower()
    
    # Genero una lista donde añado el par de palabras
    line_list = list()
    line_list.append(corpus)
    
    # Genero una lista donde añado el par de letras
    line_letters_list = list()
    line_letters_list.append(wrap(corpus, 1))
        
    # Genero el par de palabras (bigram) con listas de compresión
    bigrams = [b for l in line_list for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
    words_pair = Counter(bigrams)
    
     # Genero el par de letras (bigram) con listas de compresión
    bigrams_letters = [b for l in line_letters_list for b in zip(l.split("\n")[:-1], l.split("\n")[1:])]
    letters_pair = Counter(bigrams_letters)
    
    # Total de par de palabras/letras existentes
    total_words_pair = len(words_pair)
    total_letters_pair = len(letters_pair)
    
    # Nuevo diccionario para limpiar el proceso de salida (palabras/letras)
    clean_dictionary = dict()
    clean_dictionary_letters = dict()
    
    # Añado la probabilidad correspondiente a cada par de palabras
    for k in words_pair:
      
        if k[0] not in clean_dictionary:
            clean_dictionary[k[0]] = dict()
          
        clean_dictionary[k[0]][k[1]] = [words_pair[k] / total_words_pair, encoding(k[0]), encoding(k[1])]
        # words_pair[k] = [words_pair[k] / total_words_pair, encoding(k[0]), encoding(k[1])]
        
    # Añado la probabilidad correspondiente a cada par de letras
    for k in letters_pair:
      
        if k[0] not in clean_dictionary_letters:
            clean_dictionary_letters[k[0]] = dict()
          
        clean_dictionary_letters[k[0]][k[1]] = [letters_pair[k] / total_letters_pair, encoding(k[0]), encoding(k[1])]
        
    #Actualizo las variables correspondientes a los diccionarios de letras y palabras después de la limpieza
    words_pair = clean_dictionary
    letters_pair = clean_dictionary_letters

"""
Método utilizado para dividir el texto en n letras separadas.
Ejemplo: hola -> h o l a
"""    
def wrap(s, w):
    return textwrap.fill(s, w)


"""      
Método para obtener una palabra similar a una dada, en caso de que no se
en el diccionario
"""
def similar_word(word):
  res = ''
  min_distance = sys.maxsize
  
  for key, value in words.items():
    distance = manhattan_distance(word, value[1])
    if distance < min_distance:
      res = key
      min_distance = distance
  
  return res
"""
Método unigram_letras usado para proporcionar predicciones de letras 
en base a una cadena de números separados por espacio
"""
def unigram_letras(texto):
    res = ''
    
    for num in texto.split(' '):
        
        max_prob = 0
        letter_max_prob = ''
        
        for key, value in letters.items():
            
            # Compruebo si el número que estamos recorriendo es igual al encontrado en el diccionario
            # de ser así entonces compruebo también que la probabilidad sea más alta que la anterior.
            # Sí es más alta obtengo su probabilidad y la letra a la que se corresponde.
            if value[1] == num and value[0] > max_prob:
                max_prob = value[0]
                letter_max_prob = key

        # Almaceno la letra más probable en la variable res
        res += letter_max_prob + ' '
    
    # Devolvemos el valor encontrado limpiando los espacios iniciales y finales
    return res.strip()

"""
Método unigram_palabras usado para proporcionar predicciones de palabras 
en base a una cadena de números separados por espacio
"""
def unigram_palabras(texto):
    res = ''
    
    for numBlock in texto.split(' '):
        
        max_prob = 0
        word_max_prob = ''
        
        for key, value in words.items():
            """
            Compruebo si el número que estamos recorriendo es igual al encontrado en el diccionario
            de ser así entonces compruebo también que la probabilidad sea más alta que la anterior.
            Sí es más alta obtengo su probabilidad y la letra a la que se corresponde.
            """
            if value[1] == numBlock and value[0] > max_prob:
                max_prob = value[0]
                word_max_prob = key

        if word_max_prob == '':
          res += similar_word(numBlock) + ' '
        else:
          # Almaceno la letra más probable en la variable res
          res += word_max_prob + ' '
    
    # Devolvemos el valor encontrado limpiando los espacios iniciales y finales
    return res.strip()

"""
Método bigram_words_base usado para proporcionar predicciones de palabras
en base a una cadena de números separadas por espacio teniendo en cuenta la
palabra anterior predicha.
"""
def bigram_words_base(last_word, current_word):
  max_prob_word = ''
  max_prob = 0
  
  if last_word not in words_pair:
    return similar_word(current_word)
  
  for key in words_pair[last_word]:
    
    if words_pair[last_word][key][2] == current_word and words_pair[last_word][key][0] > max_prob:
      max_prob = words_pair[last_word][key][0]
      max_prob_word = key
      
  if max_prob_word == '':
    max_prob_word = similar_word(current_word)
  
  # Devolvemos el valor encontrado limpiando los espacios iniciales y finales
  return max_prob_word.strip()

"""
Método de invocación inicial del método bigram_words, usado para predeccir
la primera palabra, ya que esta no tiene una referencia anterior.
"""
def bigram_words(texto):
  res = ''
  last_word = ''
  
  for index, numBlock in enumerate(texto.split(' ')):
    if index == 0:
      word = unigram_palabras(numBlock)
      res += word
      last_word = word
    else:
      word = bigram_words_base(last_word, numBlock)
      res += word
      last_word = word
      
    
    res += ' '

  # Devolvemos el valor encontrado limpiando los espacios iniciales y finales
  return res.strip()

# TESTING  
print("************************** TESTING ******************************")
print("Texto: Hola -> Predicción: " + unigram_letras('3 5 4 1'));
print("Texto: Hola -> Predicción: " + unigram_palabras('3541'));
print("Texto: Hola que tal estas -> Predicción: " + unigram_palabras('3541 672 714 26716'));
print("Texto: Tengo mucho miedo -> Predicción: " + unigram_palabras('72535 57135 53225'));

# Tiempo de ejecución obtenido
print("Tiempo de ejecución en segundos: --- %s seconds ---" % (time.time() - start_time))

# Interfaz gráfica
def show_unigram_letras():
  
    e3.delete(0, END)
    e2.delete(0, END)
    
    e2.insert(10, encoding(e1.get()))
    res = unigram_letras(e2.get())
    #print("Entrada: %s\n" % res)
    e3.insert(10, res)
   
def show_unigram_palabras():
  
    e3.delete(0, END)
    e2.delete(0, END)
    
    e2.insert(10, encoding(e1.get()))
    res = unigram_palabras(e2.get())
    #print("Entrada: %s\n" % res)
    e3.insert(10, res)
    
def show_bigram_words():
  
  e3.delete(0, END)
  e2.delete(0, END)
  
  e2.insert(10, encoding(e1.get()))
  res = bigram_words(e2.get())
  #print("Entrada: %s\n" % res)
  e3.insert(10, res)
  
def show_bigram_letters():
  e3.insert(10, 'Yo me llamo Ralph')

master = Tk()
master.title("Texto predictivo")
master.minsize(width = 350, height = 150)

Label(master, text="Text").grid(row = 0)
Label(master, text="Entrada").grid(row = 1)
Label(master, text="Predicción").grid(row = 3)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)

e1.insert(10, "soy bueno") 
e2.insert(10, "658 17255") #El bloque de números equivale a "Soy bueno"
e3.insert(10, "")

e1.grid(row = 0, column = 1)
e2.grid(row = 1, column = 1)
e3.grid(row = 3, column = 1)

Button(master, text='Unigram letras', command = show_unigram_letras).grid(row = 6, column = 0, sticky = W, pady = 10)
Button(master, text='Unigram palabras', command = show_unigram_palabras).grid(row = 6, column = 1, sticky = W, pady = 10)  
Button(master, text='Bigram letras', command = show_bigram_letters).grid(row = 7, column = 0, sticky = W, pady = 10)  
Button(master, text='Bigram palabras', command = show_bigram_words).grid(row = 7, column = 1, sticky = W, pady = 10)  

master.mainloop()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    