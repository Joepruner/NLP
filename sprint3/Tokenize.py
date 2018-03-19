"""
Tokenize.py:
This program tokenizes and assigns Stanford CoreNLP tags to a sentence. Input can either be standard input or sysin.

File name: Tokenize.py
Author: Angie Pinchbeck
Date created: 27/02/2018
Date last modified: 10/03/2018
Python version: 3.5

Much of this was based on a tutorial from:
.. _Python Tutorials
    https://pythonspot.com/category/nltk/

As much of possible, we have used the Google style guide for Python:
.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys

class Tokenize():
    """
    Tokenize is a class that tokenizes and assigns Stanford CoreNLP tags to a sentence.
    It first scrubs the sentence of "stop words", that is, words that are common and not of use to discovering overall meaning,
    and also has the ability to return only the roots of words, instead of the entire word.

    Attributes:
        stopWords (String[]): The words that are considered "stop words" by the NLTK module; words that will be scrubbed.
            There are 179 stop words as of 10/03/2018.
            Use the following two lines to see number of stop words and list of stop words:
            print (len(stopWords))  # Number of words
            print(stopWords)        # List of words
        ps(PorterStemmer): An object that will allow the program to return only word stems.
        words (String[]): The words of the sentence that is being tokenized.
        wordsFiltered (String[]): The words left after the sentence has been scrubbed of stop words.
        wordsTagged (Tuple(String, String)): The wordsFiltered with their Stanford CoreNLP tags attached.

    """

    stopWords = set(stopwords.words('english'))
    ps = PorterStemmer()

    def __init__(self, data):
        self.words = word_tokenize(data)
        self.wordsFiltered = []
        for w in self.words:
            if w not in self.stopWords:
                """
                For stems of words instead of whole words, comment out the 
                first line of this loop and comment in the second line:
                    self.wordsFiltered.append(self.ps.stem(w))
                """
                self.wordsFiltered.append(w)
                #self.wordsFiltered.append(self.ps.stem(w))
        self.wordsTagged = nltk.pos_tag(self.wordsFiltered)
        """ The next line can be used if we ever decide to deal in multiple sentences at one time. """
        #self.wordsTagged.append(nltk.pos_tag(self.wordsFiltered))
        
"""
The following code allows for input. 
When running from website use:
    string = " ".join(sysin)
When running from console use:
    string = input()  

For testing purposes, a while-loop is included at the bottom (commented out) that will allow for continual input and 
tokenization until "e" is entered. 
"""
#print("Enter a sentence to tokenize (\"e\" to exit): ")
sysin = sys.argv[1:]
string = " ".join(sysin)
#string = input()

""" Create a tokenize object on the input string and print the tuple of the scrubbed words and their tags. """
t = Tokenize(string)
print(t.wordsTagged)


"""
while (data != 'e'):
    t = Tokenize(data)
    print(t.words)
    #print(t.wordsFiltered)
    print(t.wordsTagged)
    #print(t.get_tags())
    print("Enter a sentence to tokenize (\"e\" to exit): ")
    data = input()

"""

