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

import sys

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


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
                # self.wordsFiltered.append(self.ps.stem(w))
        self.wordsTagged = nltk.pos_tag(self.wordsFiltered)
        """ The next line can be used if we ever decide to deal in multiple sentences at one time. """
        # self.wordsTagged.append(nltk.pos_tag(self.wordsFiltered))


"""
Method name: numberStartsWith
Author: Kevin Feddema
Date created: 19/03/2018
Date last modified: 19/03/2018
Python version: Anaconda 3.6
    
The following method accepts a tokenized tag map and constructs a query for questions similar to "How many names 
begin with a J?" or "What is the number of people with a name starting with J?". This two questions are the most
common when asking for the number of names that begin with a letter according to out NLP survey results
"""


def numberStartsWith(tagMap):
    query5 = ""  # the final query that is returned after processing
    countIndicator = 0  # countIndicator is either 1 or 0. 1 if there is a chunk or part of speach that indicates the need to return count and 0 if not

    """Determine if there is a count indicator in the user's input"""
    for elem in tagMap:
        if elem[0] == 'number':
            countIndicator = 1

    chunkSequence = '''
                    Chunk:
                    {<WRB>+ <JJ>+}'''
    NPChunker = nltk.RegexpParser(chunkSequence)
    chunks = NPChunker.parse(tagMap)
    for n in chunks:
        if isinstance(n, nltk.tree.Tree):
            if n.label() == 'Chunk':
                howMany = n
                countIndicator = 1

    """If a countIndicator is not found in the question, the question cannot be handled by this method, return -1"""
    if countIndicator == 0:
        return -1

    """Determine the attribute that the user wants the count of. And determine whether the user wants to know if the attribute contains, starts with, or ends with"""
    attribute = ""
    condition = ""
    # NOTE: there are quite a few assumptions made here
    for elem in tagMap:
        if elem[1] == 'RB' or elem[1] == 'NNS':
            attribute = elem[0]
        if elem[0] == 'start' or elem[0] == 'starts' or elem[0] == 'begin' or elem[1] == 'begins':
            condition = 'STARTS WITH'
        if elem[0] == 'ends':
            condition = "ENDS WITH"
        if elem[0] == 'contain' or elem[0] == 'contains':
            condition == "CONTAINS"

    """Determine the value that the question filters by, ie. J, K, A, N, etc"""
    value = ""
    for elem in tagMap:
        if elem[1] == 'NNP':
            value = elem[0]

    query5 = "MATCH (n) WHERE n " + attribute + " " + condition + " \"" + value + "\" " + "RETURN COUNT (n " + attribute + ")"
    return query5


"""
The following code allows for input. 
When running from website use:
    string = " ".join(sysin)
When running from console use:
    string = input()  
For testing purposes, a while-loop is included at the bottom (commented out) that will allow for continual input and 
tokenization until "e" is entered. 
"""
# print("Enter a sentence to tokenize (\"e\" to exit): ")
sysin = sys.argv[1:]
string = " ".join(sysin)
# string = input()

""" Create a tokenize object on the input string and print the tuple of the scrubbed words and their tags. """
t = Tokenize(string)
tagMap = t.wordsTagged
print(numberStartsWith(tagMap))

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
