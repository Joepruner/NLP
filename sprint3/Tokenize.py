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
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


class Tokenize():
    """
    Tokenize is a class that tokenizes and assigns Stanford CoreNLP tags to a sentence.
    It first scrubs the sentence of "stop words", that is, words that are common and not of use to discovering overall meaning,
    and also has the ability to return only the roots of words, instead of the entire word.

    Modifications:
        20/03/2018  Fixed __init__ to tag words before scrubbing them
        25/03/2018  Moved numberStartsWith() to be inside the Tokenize class

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
    keptStopWords = ["how", "all", "with", "have", "are", "is"]
    stopWords = set(stopwords.words('english')) - set(keptStopWords)
    ps = PorterStemmer()

    def __init__(self, data):
        self.words = word_tokenize(data)
        self.wordsUnFiltered = nltk.pos_tag(self.words)
        self.wordsTagged = []
        for wt in self.wordsUnFiltered:
            if wt[0].lower() not in self.stopWords:
                """
                For stems of words instead of whole words, comment out:
                self.wordsFiltered.append(wt)
                Then comment in:
                self.wordsFiltered.append(self.ps.stem(w))
                """
                self.wordsTagged.append(wt)
                # self.wordsFiltered.append(self.ps.stem(w))

    """ The next line can be used if we ever decide to deal in multiple sentences at one time. """
    # self.wordsTagged.append(nltk.pos_tag(self.wordsFiltered))


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

    def returnName(self, tagMap):
        """Creating a list of possible labels and attributes
        that may be in the tagMap"""
        atrList = {"name": "name", "names": "name"}
        labelList = {"outlaws": "outlaw", "outlaw": "outlaw"}
        preLabelList = {"outlaw", "name"}
        label = ""
        attribute = ""
        preLabel = ""

        """Looping through the tagMap"""
        for elem in tagMap:
            word = str(elem[0]).lower() #makes the entire word lower case so is easier to work with
            if (word == "who" and elem[1] == "WP") or word in atrList.keys():
                attribute = "name"
            if word in labelList.keys():
                label = "Outlaw"
            if label in preLabelList or attribute in preLabelList:
                preLabel = "Person"

        """If any of the following variables are empty then Return 2"""
        if attribute == "" or label == "" or preLabel == "":
            return -2
        else:
            output = "MATCH (n : {} : {} ) RETURN n.{}".format(preLabel, label, attribute)

        return output
    """
   Method name: listAllof
   Author: Kevin Feddema & Joseph Pruner
   Date created: 25/03/2018
   Date last modified: 26/03/2018
   Python version: Anaconda 3.6
    """

    def listAllOf(self, tagMap):
        listAllIndicator = 0

        """Determine if there is an 'all' indicator in the user's input"""
        for elem in tagMap:
            if elem[0] == 'every' or elem[0] == 'all':
                listAllIndicator = 1
        if listAllIndicator == 0:
            return -1

        query3 = ""
        noun = ""
        property = ""
        biGrams = nltk.bigrams(tagMap)

        for bi in biGrams:
            print(bi)
            if (bi[0][1] == 'PDT' or bi[0][1] == 'DT') and \
                    (bi[1][1] == 'NNS' or bi[1][1] == 'NNP' or bi[1][1] == 'NN' or bi[1][1] == 'NNPS' or bi[1][
                        1] == 'JJ'):
                property = bi[1][0]
            if (bi[0][1] == 'VBP' or bi[0][1] == 'VBZ') and \
                    (bi[1][1] == 'NNS' or bi[1][1] == 'NNP' or bi[1][1] == 'NN' or bi[1][1] == 'NNPS' or bi[1][
                        1] == 'JJ'):
                noun = bi[1][0]
        if property != "" and noun != "":
            query3 += "MATCH (n {" + property + " :"
            query3 += "\'" + noun + "\'" + "}) RETURN n"
        elif property != "" and noun == "":
            query3 += "MATCH (n :" + property + ") RETURN n"
        return query3
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

# # sysin = sys.argv[1:]
# # string = " ".join(sysin)
# string = "what are the outlaw's names"
sysin = sys.argv[1:]
string = " ".join(sysin)
#string = "Show me all the species that are dogs?"

""" Create a tokenize object on the input string and print the tuple of the scrubbed words and their tags. """
print (string)
t = Tokenize(string)
tagMap = t.wordsTagged

#print(t.wordsTagged)
print(t.numberStartsWith(tagMap))
print(t.listAllOf(tagMap))

string = "what are the names of the outlaws"
print (string)
t = Tokenize(string)
tagMap = t.wordsTagged
print(t.wordsTagged)
print (t.wordsUnFiltered)
print (t.returnName(tagMap))
print

string = "who are the outlaws"
print (string)
t = Tokenize(string)
tagMap = t.wordsTagged
print(t.wordsTagged)
print (t.wordsUnFiltered)
print (t.returnName(t.wordsUnFiltered))

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
