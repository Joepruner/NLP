"""
Tokenize.py:
This program tokenizes and assigns Stanford CoreNLP tags to a sentence. Input can either be standard input or sysin.

File name: Tokenize.py
Author: Angie Pinchbeck, Joseph Pruner
Date created: 27/02/2018
Date last modified: 27/03/2018
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
from nltk.tokenize import word_tokenize
from inflection import singularize


class Tokenize():
    """
    Tokenize is a class that tokenizes and assigns Stanford CoreNLP tags to a sentence.
    It first scrubs the sentence of "stop words", that is, words that are common and not of use to discovering overall meaning,
    and also has the ability to return only the roots of words, instead of the entire word.

    Modifications:
        20/03/2018  Fixed __init__ to tag words before scrubbing them
        25/03/2018  Moved numberStartsWith() to be inside the Tokenize class
        26/03/2018  Expanded the kept stop words; added singularize method and removed PorterStemmer
        27/03/2018  Added the initDatabaseDictionaries() method to initialize Label, Relationships, etc.

    Attributes:
        keptStopWords(String[]): A list of words that we don't want to have scrubbed from input, even though
            they appear in the NLTK modul stop words.
        stopWords (String[]): The words that are considered "stop words" by the NLTK module; words that will be scrubbed.
            There are 179 stop words as of 10/03/2018.
            Use the following two lines to see number of stop words and list of stop words:
            print (len(stopWords))  # Number of words
            print(stopWords)        # List of words
        words (String[]): The words of the sentence that is being tokenized.
        wordsUnFiltered (String[]): The words and their Stanford CoreNLP tags attached, so far unfiltered of stop words.
        wordsTagged (Tuple(String, String)): The words and their Stanford CoreNLP tags attached, after being filtered
            of stop words.
        labels [List]:  The list of unique labels that exist within a graph database.
        relationships [List]:   The list of unique relationships that exist within a graph database.
        labelProperties [Dictionary]:   Has the properties attached to every label from the "labels" list.
        relationshipProperties [Dictionary]:   Has the properties attached to every
            relationship from the "relationships" list.

    """
    
    keptStopWords = ["how", "all", "with", "have", "who", "and", "are", "is"]
    stopWords = set(stopwords.words('english')) - set(keptStopWords)
    labels = []
    relationships = []
    labelProperties = {}
    relationshipProperties = {}

    def __init__(self, data):
        self.initDatabaseDictionaries()
        self.words = word_tokenize(data.lower())
        self.wordsUnFiltered = nltk.pos_tag(self.words)
        self.wordsTagged = []
        for wt in self.wordsUnFiltered:
            if wt[0] not in self.stopWords:
                tuple = (singularize(wt[0]), wt[1])
                self.wordsTagged.append(tuple)

    """
    Method name: initDatabaseDictionaries()
    Author: Angie Pinchbeck
    Date created: 27/03/2018
    Date last modified: 27/03/2018
    Python version: Python 3.5
    
    This method initializes the lists that are used for language comparison in the translation methods. 
    For now, these are hardcoded to fit an "Outlaw" database. However, this can be extended for use with 
    actual databases. The Cypher query needed to return that information from the database is listed
    above each initialization so that, in the future, this method can be scaled to include the feature of 
    linking to a real database. 
    """
    def initDatabaseDictionaries(self):

        # MATCH (n) RETURN distinct labels(n)
        self.labels = ["Person", "Animal", "Outlaw"]

        #MATCH n-[r]-() RETURN distinct type(r)
        self.relationships = ["LIKES", "DISLIKES", "PARENTS", "BROTHER"]

        """ Note that the following Cypher query would need to run in a loop for every label that 
        was already in self.labels to fill out the labelProperties dictionary """
        # MATCH (n:Label) UNWIND keys(n) AS key RETURN collect(distinct key)
        self.labelProperties = dict(Person=["name", "female", "size", "bounty"], Animal=["name", "species"],
                                         Outlaw=["name", "bounty", "size"])

        """ Note that the following Cypher query would need to run in a loop for every relationship that 
        was already in self.relationships to fill out the relationshipProperties dictionary """
        # MATCH (n:Label) UNWIND keys(n) AS key RETURN collect(distinct key)
        self.relationshipProperties = dict(LIKES=["because"], DISLIKES=["because"], PARENTS=["gift"], BROTHER=[])



    """
    Method name: runTranslator()
    Author: Angie Pinchbeck
    Date created: 26/03/2018
    Date last modified: 26/03/2018
    Python version: Python 3.5
    
    This is a method that will run an input tagMap through all the other translation methods, and then return a list
    of all the queries that are output.
    """
    def runTranslator(self, tagMap):
        results = []
        if self.matchLabelAndProperty(tagMap) != -1:
            results.append(self.matchLabelAndProperty(tagMap))
        if self.numberStartsWith(tagMap) != -1:
            results.append(self.numberStartsWith(tagMap))
        if self.listAllOf(tagMap) != -1:
            results.append(self.listAllOf(tagMap))
        if self.returnName(tagMap) != -1:
            results.append(self.returnName(tagMap))
        return results

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

    def returnName(self, tagMap):
        """Creating a list of possible labels and attributes
        that may be in the tagMap"""
        # atrList = {"name": "name", "names": "name"}
        # labelList = {"outlaws": "outlaw", "outlaw": "outlaw"}
        # preLabelList = {"outlaw", "name"}
        label = []
        attribute = []
        preLabel = ""

        """Looping through the tagMap"""
        # for elem in tagMap:
        #     word = str(elem[0]).lower() #makes the entire word lower case so is easier to work with
        #     if (word == "who" and elem[1] == "WP") or word in atrList.keys():
        #         attribute = "name"
        #     if word in labelList.keys():
        #         label = "Outlaw"
        #     if label in preLabelList or attribute in preLabelList:
        #         preLabel = "Person"


        """Attempt 2 lol"""
        for elem in tagMap:
            word = str(elem[0]).lower()
            for i in range(0, len(self.labels)-1):
                if word == self.labels[i]:
                    label.append(self.labels[i])
                    print (self.labels[i])
        #print (label)


        """If any of the following variables are empty then Return 2"""
        # if attribute == "" or label == "" or preLabel == "":
        #     return -1
        # else:
        #     output = "MATCH (n : {} : {} ) RETURN n.{}".format(preLabel, label, attribute)
        # return output
      
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

#sysin = sys.argv[1:]
#string = " ".join(sysin)
#string = "What are the names of all the people?"
#string = "How many names start with J?"
#string = "Show me all the species that are dogs?"
#string = "what are the names of the outlaws"
string = "who are the Outlaw and Animal"

""" Create a tokenize object on the input string and print the tuple of the scrubbed words and their tags. """
t = Tokenize(string)
tagMap = t.wordsTagged
#print(tagMap)
#print(t.matchLabelAndProperty(tagMap))
#print(t.numberStartsWith(tagMap))
#print(t.listAllOf(tagMap))
print (t.labels)
print ("LOL")

# results = t.runTranslator(tagMap)
# for item in results:
#     print(item)


"""
string = input()
while (string != 'e'):
    t = Tokenize(string)
    tagMap = t.wordsTagged
    results = t.runTranslator(tagMap)
    for item in results:
        print(item)
    print("Enter a sentence to tokenize (\"e\" to exit): ")
    string = input()
"""

