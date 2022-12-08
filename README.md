# Language Learning Game - course-project-group-25

## Summary of presentation introduction
Our Project for CS 222 was a language learning card game that has three working languages, Spanish, English and French. We used Python, JavaScript, HTML, CSS for our application. We also used Flask and PyMultiDictionary.  Users will be able to learn new words through the aspect of matching English words to their translated words in one of two other languages, Spanish or French. We have an interactive UI that is easy for users to navigate and offer three varying difficulties where users can select more challenging words according to  their comfort level. 

## Describes technical architecture
Our Front end consists of two HTML files, Welcome.html and Index.html  Welcome.html is called first to ask for the users input on which language they would like to select as well as the difficulty. This is passed to the back end which then calls the index.html file where the user can play the game. When they click two cards, both cards are passed to the back end and are processed and checked if they are a match. If the two are a match, the score is incremented and the user can continue. If it is not a match the score would be decreased by one. 


Our Back End consists of a PlayerInfo class where we store 
This class includes a score that keep tracks of the score of the user.
Number_of_card_pairs was set to the default value of 5, so in total we have 10 cards on display
Word_bank is an array that stores all the words
English is an away that stores 5 words in english
Language stores the language of  user choice
Other_language is an array that stores the other 5 words in the other selected language
All_words_random is an array that stores the word generated at random
Translations is 

## Installation instructions
Run git pull origin main to download our application. 
To import the Flask, we can use these commands
To set up a virtual environment run this command in the terminal: 
```
Py –3 –m venv venv 
venv\Scripts\activate 
```

To download Python 3 and pip run this command in the terminal:   
```
pip install flask
```



## Group members and their roles
```
Andrew Tran - Frontend Development + Presentation
Shreya Patel - Backend Development + Presentation
Selena Wang - Backend Development
Rudhi Bashambu - Backend Development
```

