"""importing Flask"""
#from datetime import datetime  url_for, redirect, , flash
from ast import IsNot
import random
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from PyMultiDictionary import MultiDictionary


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb'
#database???
db = SQLAlchemy(app)

class PlayerInfo:
    """declaring PlayerInfo Class to keep track of words, score, guesses"""
    # Private variable score keep track of the score of the user
    score = 0
    # Private variable number_of_card_pairs left on screen
    # (updates once the user answered the question correctly)
    number_of_card_pairs = 5
    #words from txt file converted to word bank

    word_bank = []
    #need to call function set_difficulty to initialize it
     # Moving this to an individual function??? Or thought we are using the multidictionary library?
    # with open('easy_words.txt','r', encoding="utf-8") as w:

    #     word_bank = w.read().split()
    # Array storing English words
    english = []
    #english.append(word_bank[0])
    #comment out later but for now leave for display
    #english = random.choices(word_bank, k=5)
    #varaible for the other language
    language = ""
    # Array storing words in another languages selected by the user
    other_language = []
    #int for finding language in the multidictionary
    language_index = 6
    # Array to hold other_language and english words for the display
    all_words_random = []
    # Dictionary to hold all words and their translations
    translations = {}
    # Number of guesses for each words and resets after correct selection
    num_of_guesses = 0
    #difficulty: should contain either Easy, Medium, or Hard
    difficulty = ""
    #match
    match = "NO MATCH"




player = PlayerInfo()
dic = MultiDictionary()

def set_difficulty():
    if player.difficulty == "Easy":
        with open('easy_words.txt','r', encoding="utf-8") as w:
            player.word_bank = w.read().split()
    if player.difficulty == "Medium":
        with open('medium_words.txt','r', encoding="utf-8") as w:
            player.word_bank = w.read().split()
    if player.difficulty == "Hard":
        with open('hard_words.txt','r', encoding="utf-8") as w:
            player.word_bank = w.read().split()

def set_language():
    if player.language == "Spanish":
        # player.language = "es"
        player.language_index = 6
    if player.language == "French":
        # player.language == "fr"
        player.language_index = 7



def read_word(file):
    with open(file, 'r', encoding="utf-8") as w:
        player.word_bank = w.read().split()


def set_guess(level):
    if player.difficulty == "Hard":
        player.num_of_guesses += 5
    elif player.difficulty == "Medium":
        player.num_of_guesses += 4
    else:
        player.num_of_guesses += 3



def get_meaning(provided_language, word, target_language):
    """Get meaning of the passed in word in the required language"""
    word = dic.translate(provided_language, word, to=target_language)
    return word



def generate_rand_words(target_language):
    """Generate several? random words in the target_language"""
    # Assigning definition and words into 2 separate arrays each one contains 5 words
    # Will randomly choose words from the txt files for the english array
    player.english = random.choices(player.word_bank, k=player.number_of_card_pairs)
    removeDuplicates()
    # Getting definitions by calling get_meaning for the second array definitions
    for i in range(player.number_of_card_pairs):
        player.other_language.append(dic.translate("en", player.english[i])[player.language_index][1].capitalize())
        #adding to the dictionary for translations
        player.translations[player.english[i]] = dic.translate("en", player.english[i])[player.language_index][1].capitalize()
        player.translations[dic.translate("en", player.english[i])[player.language_index][1].capitalize()] = player.english[i]
    # Initialize the all_words_random
    for i in range(player.number_of_card_pairs):
        player.all_words_random.append(player.english[i])
        player.all_words_random.append(player.other_language[i])
    random.shuffle(player.all_words_random)
        
def removeDuplicates():
    temp_english = [*set(player.english)]
    if len(temp_english) < 5:
        while len(temp_english) < 5:
            temp_english.append(random.choice(player.word_bank))
        player.english = temp_english



# def valid_input(user_input):
#     """Checking if valid user input, comparing get_meaning to user input"""
#     # Checking the array of definitions and words to see if user_input exists
#     valid = False
#     if player.num_of_guesses == 0:
#         # Fix later so instead of printing we end game
#         return print("Ran out of guesses, sorry :(")
#     for i in range(player.number_of_card_pairs):
#         if user_input == player.english[i]:
#             valid = True
#     if valid is False:
#         player.num_of_guesses -= 1
#     return valid



def correct_input(idx1, idx2):
    """Check if the user input is correct"""
    # Check if word matches the definition
    print(player.translations.get(player.all_words_random[idx2]))
    if player.all_words_random[idx1] == player.translations.get(player.all_words_random[idx2]):
        player.match = "MATCH"
        update_user_score()
        #should update frontend display of guesses
        #player.num_of_guesses = player.num_of_guesses - 
        #render_template("index.html", guess = player.num_of_guesses, score = player.score)
    else:
        player.match = "NO MATCH"
        player.num_of_guesses = player.num_of_guesses - 1
    render_template("index.html", Language=player.language, Difficulty=player.difficulty,
    score = player.score, guess = player.num_of_guesses,
    spanish_words = player.other_language, english = player.english, all_words = player.all_words_random) 



def remove(word):
    """Remove word and definition once we get it correct"""
    for i in range(player.number_of_card_pairs):
        if word == player.english[i]:
            player.english.pop(i)
            player.other_language.pop(i)
            player.number_of_card_pairs -= 1


def updateDifficulty(level):
    if level != "Easy" or level != "Medium" or level != "Hard":
        print("Something is wrong")
    else:
        player.level_of_difficulty = level


def status():
    """Check if the game is over"""
    return player.number_of_card_pairs == 0 or player.num_of_guesses == 0



def check_not_same():
    """Returning an arry of index of repeated words in other_language array"""
    seen = []
    same = []
    for i in player.other_language:
        if i not in seen:
            seen.append(i)
        else:
            same.append(i)
    return len(same)


def get_user_score():
    """Controls the user score"""
    return player.score


def set_user_score(input):
    """Setting the user score"""
    player.score = input


def update_user_score():
    """ Updating the user score"""
    if player.difficulty == "Hard":
        player.score += 3
        if player.score == 15:
            print("SCORE GOTTEN")
            test()
    elif player.difficulty == "Medium":
        player.score += 2
        if player.score == 10:
            print("SCORE GOTTEN")
            test()
    else:
        player.score += 1
        if player.score == 5:
            print("SCORE GOTTEN")
            test()


@app.route('/')
def welcome():
    """Setting a welcome page"""
    return render_template('welcome.html')

@app.route('/end')
def test():
    """Setting a welcome page"""
    print("MADE IT")
    return render_template('endgame.html', score = player.score)


@app.route('/Beginning Input(L/D)')
def beginning_input():
    """Inputting two variables language and difficulty from user"""
    player.language = request.args["Language"]
    player.difficulty = request.args["Difficulty"]
    set_difficulty()
    set_guess(player.difficulty)
    set_language()
    generate_rand_words(player.language)
    return render_template('index.html', Language=player.language, Difficulty=player.difficulty,
    score = player.score, guess = player.num_of_guesses, all_words = player.all_words_random)

# @app.route("/anything", methods=['GET', 'POST'])
# def cardIndexCheck():
#     cardIndex1 = 0
#     cardIndex2 = 0
#     new_score = 0
#     new_guess = 0
#     data = []
#     if request.method == "POST":
#         data = request.form["data"]
#         cardIndex1 = int(data[0])
#         cardIndex2 = int(data[2])
#         correct_input(cardIndex1, cardIndex2)
#         new_score = player.score
#         new_guess = player.num_of_guesses
#         return render_template('index.html', Language=player.language, Difficulty=player.difficulty,
#         score = new_score, guess = new_guess, all_words = player.all_words_random)
#         #return str(cardIndex1) + str(cardIndex2) + "Hello"

@app.route("/Card Check", methods=['GET', 'POST'])
def cardIndexCheck():
    cardIndex1 = 0
    cardIndex2 = 0
    boolCardCheck = True
    data = []
    if request.method == "POST":
        data = request.form["data"]
        cardIndex1 = int(data[0])
        cardIndex2 = int(data[2])
        correct_input(cardIndex1, cardIndex2)
        returnText = str(player.score)
        return returnText
    return render_template("index.html", Language=player.language, Difficulty=player.difficulty,
         score = 2, guess = 8, all_words = player.all_words_random)
 


if __name__ == "__main__":
    app.run(debug=True)

