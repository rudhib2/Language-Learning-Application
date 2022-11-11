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

# class user(db.Model):
#     name = db.Column(db.String(50), nullable=False, primary_key=True)
#     score = db.Column(db.Integer, default=0)
#     finished = db.Column(db.Boolean, default=False)

#     def __init__(self, name):
#         self.name = name
#         self.score = get_user_score()
#         self.finished = status()




# # @app.route('/')
# # def index():
# #     temp = 1
# #     return render_template('index.html', value = temp, guess = "test")

# if __name__ == "__main__":
#     app.run(debug=True)

class PlayerInfo:
    """declaring PlayerInfo Class to keep track of words, score, guesses"""
    # Private variable score keep track of the score of the user
    score = 0
    # Private variable number_of_card_pairs left on screen
    # (updates once the user answered the question correctly)
    number_of_card_pairs = 5
    #words from txt file converted to word bank

    #word_bank = []
    #need to call function set_difficulty to initialize it
     # Moving this to an individual function??? Or thought we are using the multidictionary library?
    with open('easy_words.txt','r', encoding="utf-8") as w:

        word_bank = w.read().split()
    # Array storing English words
    english = []
    #english.append(word_bank[0])
    #comment out later but for now leave for display
    english = random.choices(word_bank, k=5)
    #varaible for the other language
    language = ""
    # Array storing words in another languages selected by the user
    other_language = []
    # Number of guesses for each words and resets after correct selection
    num_of_guesses = 0
    #difficulty: should contain either Easy, Medium, or Hard
    difficulty = ""



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
        player.language = "es"
    if player.language == "French":
        player.language == "fr"



def read_word(file):
    with open(file, 'r', encoding="utf-8") as w:
        player.word_bank = w.read().split()
        


def set_guess(level):
    if player.level_of_difficulty == "Hard":
        player.num_of_guesses += 5
    elif player.level_of_difficulty == "Medium":
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
    player.english.append(player.word_bank[0])
    # Will randomly choose words from the txt files for the english array
    # English = random.choices(word_bank, k=5)
    player.english = random.choices(player.word_bank, k=player.number_of_card_pairs)
    # Getting definitions by calling get_meaning for the second array definitions
    for i in range(player.number_of_card_pairs):
        player.other_language.append(get_meaning("en", player.english[i], target_language))
    # Call check_not_same(), check for duplicates
    if check_not_same() > 0:
        # Remove duplicates
        for i in player.other_language:
            if i in check_not_same():
                player.other_language.remove(i)



def valid_input(user_input):
    """Checking if valid user input, comparing get_meaning to user input"""
    # Checking the array of definitions and words to see if user_input exists
    valid = False
    if player.num_of_guesses == 0:
        # Fix later so instead of printing we end game
        return print("Ran out of guesses, sorry :(")
    for i in range(player.number_of_card_pairs):
        if user_input == player.english[i]:
            valid = True
    if valid is False:
        player.num_of_guesses -= 1
    return valid



def correct_input(user_input):
    """Check if the user input is correct"""
    # Check if word matches the definition
    # Call valid_input
    valid_input(user_input)
    for i in range(player.number_of_card_pairs):
        if user_input == player.english[i]:
            update_user_score()
            remove(user_input)
            player.num_of_guesses = 3
            #should update frontend display of guesses
            render_template("index.html", guess = player.num_of_guesses)


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
    if player.level_of_difficulty == "Hard":
        player.score += 3
    elif player.level_of_difficulty == "Medium":
        player.score += 2
    else:
        player.score += 1


@app.route('/')
def welcome():
    """Setting a welcome page"""
    return render_template('welcome.html')


@app.route('/Beginning Input(L/D)')
def beginning_input():
    """Inputting two variables language and difficulty from user"""
    player.language = request.args["Language"]
    player.difficulty = request.args["Difficulty"]
    return render_template('index.html', Language=player.language, Difficulty=player.difficulty,
    score = player.score, guess = player.num_of_guesses,
    words = player.english, bank = player.word_bank)

# @app.route('/')
# def index():
#     temp = 1
#     #user = user.query.all(),
#     return render_template('index.html', score = player.score,
#     guess = player.num_of_guesses, words = player.english)

if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/', methods = ['GET', 'POST'])
# def instance():
#     if request.method == 'POST':
#         player = user(request.form['name'])
#         db.session.add(player)
#         db.session.commit()
#         flash('You can start playing!!!')
#         return redirect(url_for('index'))
#     else:
#         return render_template('instance.html')


# @app.route('/delete/')
# def delete(name):
#     user_to_delete = user.query.get_or_404(name)
#     db.session.delete(user_to_delete)
#     db.session.commit()
#     return redirect(url_for('index'))
