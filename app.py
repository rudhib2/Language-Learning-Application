#importing flask
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from PyMultiDictionary import MultiDictionary
from datetime import datetime
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb'
#database???
db = SQLAlchemy(app)

class user(db.Model):
    name = db.Column(db.String(50), nullable=False, primary_key=True)
    score = db.Column(db.Integer, default=0)
    finished = db.Column(db.Boolean, default=False)

    def __init__(self, name):
        self.name = name
        self.score = get_user_score()
        self.finished = status()




# # @app.route('/')
# # def index():
# #     temp = 1
# #     return render_template('index.html', value = temp, guess = "test")

# if __name__ == "__main__":
#     app.run(debug=True)

class PlayerInfo:
    # Private variable score keep track of the score of the user
    score = 0
    # Private variable number_of_card_pairs left on screen
    # (updates once the user answered the question correctly)
    number_of_card_pairs = 5
    #words from txt file converted to word bank
    #word_bank = []
    with open('easy_words.txt','r') as w:
        word_bank = w.read().split()
    # Array storing English words
    english = []
    # Array storing words in another languages selected by the user
    other_language = []
    # Number of guesses for each words and resets after correct selection
    num_of_guesses = 3


player = PlayerInfo()
dic = MultiDictionary()

# Get meaning of the passed in word in the required language
def get_meaning(provided_language, word, target_language):
    word = dic.translate(provided_language, word, to=target_language)
    return word

# Generate several? random words in the target_language
def generate_rand_words(target_language):
    # Assigning definition and words into 2 separate arrays each one contains 5 words
    player.english.append(player.word_bank[0])
    #will randomly choose words from the txt files for the english array
    #still need to check for duplicates
    player.english.append(random.choices(player.word_bank, player.number_of_card_pairs))
    # Getting definitions by calling get_meaning for the second array definitions
    for i in range(player.number_of_card_pairs):
        player.other_language.append(get_meaning("en", player.english[i], target_language))
    # Call check_not_same()
    num_of_dups = check_not_same()
    if num_of_dups() > 0:
        #remove duplicates  
        for i in player.other_language:
            if i in num_of_dups:
                player.other_language.remove(i)
    return

# Checking the user input if they are valid, comparing the output from get_meaning to the user input
def valid_input(user_input):
    # Checking the array of definitions and words to see if user_input exists
    valid = False
    for i in range(player.number_of_card_pairs):
        if user_input == player.english[i]:
            valid = True
    if valid == False:
        player.num_of_guesses -= 1
        if player.num_of_guesses == 0:
            # Fix later so instead of printing we end game
            print("Ran out of guesses, sorry :(")
    return valid


# Check if the user input is correct
def correct_input(user_input):
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
    return

# Remove word and definition once we get it correct
def remove(word):
    for i in range(player.number_of_card_pairs):
        if word == player.english[i]:
            player.english.pop(i)
            player.other_language.pop(i)
            player.number_of_card_pairs -= 1
    return

# Check if the game is over
def status():
    if player.number_of_card_pairs == 0 or player.num_of_guesses == 0:
        return True
    else:
        return False

# Returning an arry of index of repeated words in other_language array
def check_not_same():
    seen = []
    same = []
    for i in player.other_language:
        if i not in seen:
            seen.append(i)
        else:
            same.append[i]
    return same

# Controls the user score
def get_user_score():
    return player.score

# Setting the user score
def set_user_score(input):
    player.score = input
    return

# Updating the user score
def update_user_score():
    player.score += 1
    return

@app.route('/')
def index():
    temp = 1
    return render_template('index.html', user = user.query.all(), score = player.score,
    guess = player.num_of_guesses, words = player.english)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/', methods = ['GET', 'POST'])
def instance():
    if request.method == 'POST':
        player = user(request.form['name'])
        db.session.add(player)
        db.session.commit()
        flash('You can start playing!!!')
        return redirect(url_for('index'))
    else:
        return render_template('instance.html')


@app.route('/delete/')
def delete(name):
    user_to_delete = user.query.get_or_404(name)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('index'))
