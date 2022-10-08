from PyMultiDictionary import MultiDictionary
import random

score = 0
number_of_cards = 5

#get meaning of the passed in word in the required language
def get_meaning(provided_language, word, target_language):
    dic = MultiDictionary()
    word = dic.translate(provided_language, word, to=target_language)
    return word

#generate several? random words in the target_language 
def generate_rand_words(target_language):
    #assigning definition and words into 2 separate arrays
    #picking random words to go into first array words
    #getting definitions by calling get_meaning for the second array definitions
    #call check_not_same()
    return 

#checking the user input if they are valid, comparing the output from get_meaning to the user input
def valid_input(user_input):
    #checking the array of definitions and words to see if the user_input exists
    return

#Check if the game is over
def finished():
    return

#Check the random words generated are not the same

#Controls the user score
#Setting the user score

#private variables 
    #array of random words generated
    #keep track of user score
    #number of pairs left on screen