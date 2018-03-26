"""
Tokenize.py:
This program tokenizes and assigns Stanford CoreNLP tags to a sentence. Input can either be standard input or sysin.

File name: Tokenize.py
Author: Angie Pinchbeck, Joseph Pruner
Date created: 27/02/2018
Date last modified: 25/03/2018
Python version: 3.5

Much of this was based on a tutorial from:
.. _Python Tutorials
    https://pythonspot.com/category/nltk/

As much of possible, we have used the Google style guide for Python:
.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""

import nltk
import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from inflection import singularize
#from pattern.text.en import singularize


class Tokenize():
    """
    Tokenize is a class that tokenizes and assigns Stanford CoreNLP tags to a sentence.
    It first scrubs the sentence of "stop words", that is, words that are common and not of use to discovering overall meaning,
    and also has the ability to return only the roots of words, instead of the entire word.

    Modifications:
        20/03/2018  Fixed __init__ to tag words before scrubbing them
        25/03/2018  Moved numberStartsWith() to be inside the Tokenize class
        26/03/2018  Expanded the kept stop words to include "who".

    Attributes:
        keptStopWords(String[]): A list of words that we don't want to have scrubbed from input, even though
            they appear in the NLTK modul stop words.
        stopWords (String[]): The words that are considered "stop words" by the NLTK module; words that will be scrubbed.
            There are 179 stop words as of 10/03/2018.
            Use the following two lines to see number of stop words and list of stop words:
            print (len(stopWords))  # Number of words
            print(stopWords)        # List of words
        ps(PorterStemmer): An object that will allow the program to return only word stems.
        words (String[]): The words of the sentence that is being tokenized.
        wordsUnFiltered (String[]): The words and their Stanford CoreNLP tags attached, so far unfiltered of stop words.
        wordsTagged (Tuple(String, String)): The words and their Stanford CoreNLP tags attached, after being filtered
            of stop words.

    """
    keptStopWords = ["how", "all", "with", "have", "who", "and"]
    stopWords = set(stopwords.words('english')) - set(keptStopWords)
    ps = PorterStemmer()

    def __init__(self, data):
        self.words = word_tokenize(data.lower())
        self.wordsUnFiltered = nltk.pos_tag(self.words)
        self.wordsTagged = []
        for wt in self.wordsUnFiltered:
            if wt[0] not in self.stopWords:
                tuple = (singularize(wt[0].lower()), wt[1])
                self.wordsTagged.append(tuple)


    """
    Method name: matchLabelAndProperty
    Author: Angie Pinchbeck
    Date created: 25/03/2018
    Date last modified: 26/03/2018
    Python version: Python 3.5
    """

    def matchLabelAndProperty(self, tagMap):
        nounCount = 0
        for item in tagMap:
            if item[1] == 'NN' or item[1] == 'NNS':
                nounCount += 1
        if nounCount < 2:
            return -1

        countIndicator = 0  # countIndicator is either 1 or 0. 1 if there is a chunk or part of speach that indicates
        # the need to return count and 0 if not
        """Determine if there is a count indicator in the user's input"""
        for elem in tagMap:
            if elem[0] == 'number':
                countIndicator = 1
        chunkSequence = '''Chunk:{<WRB>+ <JJ>+}'''
        NPChunker = nltk.RegexpParser(chunkSequence)
        chunks = NPChunker.parse(tagMap)
        for n in chunks:
            if isinstance(n, nltk.tree.Tree):
                if n.label() == 'Chunk':
                    howMany = n
                    countIndicator = 1
        """If a countIndicator is found in the question, the question shouldn't be handled by this method, return -1"""
        if countIndicator == 1:
            return -1

        """
        Based on position of the word 'all', work out whether the label will appear in the tagMap before or 
        after the properties
        """
        flagAllFirst = False
        for item in tagMap:
            if item[1] == 'PDT':
                flagAllFirst = True
                break
            elif item[1] == 'NNS':
                break

        nounCount = 0
        if not flagAllFirst:
            for item in tagMap[::-1]:
                if (item[1] == 'NN' or item[1] == 'NNS') and nounCount == 0:
                    nodeName = item[0][0]
                    label = item[0].capitalize()
                    nounCount += 1
                    #print("Label: " + label)
                elif (item[1] == 'NN' or item[1] == 'NNS'):
                    prop = item[0]
                    nounCount += 1
                    #print("Property: " + prop)
        else:
            for item in tagMap:
                if (item[1] == 'NN' or item[1] == 'NNS') and nounCount == 0:
                    nodeName = item[0][0]
                    label = item[0].capitalize()
                    nounCount += 1
                    #print("Label: " + label)
                elif (item[1] == 'NN' or item[1] == 'NNS'):
                    prop = item[0]
                    nounCount += 1
                    #print("Property: " + prop)

        query1 = "MATCH (" + nodeName + " :" + label + ") RETURN " + nodeName + "." + prop
        return query1


    """
    Method name: numberStartsWith
    Author: Kevin Feddema
    Date created: 19/03/2018
    Date last modified: 25/03/2018
    Python version: Anaconda 3.6
        
    The following method accepts a tokenized tag map and constructs a query for questions similar to "How many names 
    begin with a J?" or "What is the number of people with a name starting with J?". This two questions are the most
    common when asking for the number of names that begin with a letter according to out NLP survey results
    """
    def numberStartsWith(self, tagMap):
        query5 = ""  # the final query that is returned after processing
        countIndicator = 0  # countIndicator is either 1 or 0. 1 if there is a chunk or part of speach that indicates
                            # the need to return count and 0 if not

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

        """Determine the attribute that the user wants the count of. 
        And determine whether the user wants to know if the attribute contains, starts with, or ends with"""
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
            if elem[1] == 'NN':
                value = elem[0].capitalize()

        query5 = "MATCH (n) WHERE n." + attribute + " " + condition + " \"" + value + "\" " + "RETURN COUNT (n." + attribute + ")"
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
#string = "What are the names of all the people?"
#string = "How many names start with J?"

""" Create a tokenize object on the input string and print the tuple of the scrubbed words and their tags. """
t = Tokenize(string)
tagMap = t.wordsTagged
print(tagMap)
print(t.matchLabelAndProperty(tagMap))
#print(t.numberStartsWith(tagMap))


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
