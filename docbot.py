# -*- coding: utf-8 -*-
"""DocBot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/177tIVxPeVfI251cORehe1qeczwkMbtD6
"""

pip install nltk

pip install newspaper3k

# import libraries
import numpy as np
import random
import string
import nltk
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

# download the punkt package
nltk.download('punkt', quiet=True)

# get the article
article = Article('https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963')
article.download()
article.parse()
article.nlp()
full_text = article.text
full_text

# tokenization
text = full_text
sentence_list = nltk.sent_tokenize(text) # a list of sentences
sentence_list

# a function to return a random greeting response to a users greeting 
def greeting_response(text):
  text = text.lower()

  # bots greeting response
  bot_greetings = ['hi', 'hey', 'hello', 'hola']
  # users greeting
  user_greetings = ['hi','hey', 'hello', 'greetings']

  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)

# a function to sort index
def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        #swap
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp

  return list_index

# create the bots response
def bot_response(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  bot_response = ''
  cm = CountVectorizer().fit_transform(sentence_list)
  similarity_scores = cosine_similarity(cm[-1], cm)
  similarity_scores_list = similarity_scores.flatten()
  index = index_sort(similarity_scores_list)
  index = index[1:]
  response_flag = 0

  j = 0
  for i in range(len(index)):
    if similarity_scores_list[index[i]] > 0.0:
      bot_response = bot_response + " " + sentence_list[index[i]]
      response_flag = 1
      j = j + 1
    if j > 2:
      break
  if response_flag == 0:
    bot_response = bot_response +" " + "Sorry, I don't understand"

  sentence_list.remove(user_input)

  return bot_response

# start the chat
print("Doctor Bot: Hi! I am Doctor Bot! I will answer your queries about Coronavirus disease. If you want to exit, type bye.")
exit_list = ['bye', 'good bye', 'see you', 'see you later', 'quit', 'exit']
while(True):
  user_input = input()
  if user_input.lower() in exit_list:
    print("Doc Bot: Chat with you later!")
    break
  else:
    if greeting_response(user_input) != None:
      print("Doc Bot: " + greeting_response(user_input))
    else:
      print("Doc Bot: " + bot_response(user_input))