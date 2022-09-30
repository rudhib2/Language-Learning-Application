from PyMultiDictionary import MultiDictionary
import random

#get meaning of the passed in word in the required language
def get_meaning(provided_language, word, target_language):
    dic = MultiDictionary()
    word = dic.translate(provided_language, word, to=target_language)
    return word

#generate several? random words in the target_language 
def generate_rand_words(target_language):

    return 


