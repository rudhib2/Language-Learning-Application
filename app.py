from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from PyMultiDictionary import MultiDictionary
import numpy as np
#object dic created from multiDictionary
dic = MultiDictionary()
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'squlite:///testdb'
#database???
db = SQLAlchemy(app)

def randomfun():
    pass

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

class PlayerInfo:
    #private variable score keep track of the score of the user
    score = 0
    #private variable number_of_card_pairs left on screen (updates once the user answered the question correctly)
    number_of_card_pairs = 5
    #array storing English words
    english = []
    #array storing words in another languages selected by the user
    other_language = []

#get meaning of the passed in word in the required language
def get_meaning(provided_language, word, target_language):
    word = dic.translate(provided_language, word, to=target_language)
    return word
 
#generate several? random words in the target_language
def generate_rand_words(target_language):
    #assigning definition and words into 2 separate arrays each one contains 5 words
    #picking random words to go into first array words
    #getting definitions by calling get_meaning for the second array definitions
    #call check_not_same()
    return
 
#checking the user input if they are valid, comparing the output from get_meaning to the user input
def valid_input(user_input):
    #checking the array of definitions and words to see if user_input exists
    valid = False
    for i in range(number_of_card_pairs):
        if user_input == english[i]:
            valid = True
    return valid
 
 
#Check if the user input is correct
def correct_input(user_input):
    #Check if word matches the definition
    for i in range(number_of_card_pairs):
        if user_input == english[i]:
            update_user_score()
            remove(user_input)
    return 
 
#remove word and definition once we get it correct
def remove(word):
    for i in range(number_of_card_pairs):
        if word == english[i]:
            english.pop(i)
            other_language.pop(i)
            number_of_card_pairs = number_of_card_pairs - 1
    return
 
#Check if the game is over
def finished():
    if number_of_card_pairs != 0:
        return True
    else: 
        return False
 
#Check the random words generated are not the same
def check_not_same():
    return
 
#Controls the user score
def get_user_score():
   
    return score
 
#Setting the user score
def set_user_score(input):
    score = input
    return
 
#updating the user score
def update_user_score():
    score = score + 1
    return

 
