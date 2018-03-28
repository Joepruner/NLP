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
import unicodedata  # for case-insensitive comparisons


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
                    Added equalsIgnoreCase() method to compare two strings case-insensitively.
                    Expanded kept stop words: now include "each".

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
    
    keptStopWords = ["how", "all", "with", "have", "who", "and", "are", "is", "each"]
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


    def initDatabaseDictionaries(self):
        """
        Author: Angie Pinchbeck
        Date created: 27/03/2018
        Date last modified: 27/03/2018

        This method initializes the lists that are used for language comparison in the translation methods.
        For now, these are hardcoded to fit an "Outlaw" database. However, this can be extended for use with
        actual databases. The Cypher query needed to return that information from the database is listed
        above each initialization so that, in the future, this method can be scaled to include the feature of
        linking to a real database.

        :return: nothing
        """

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

    def equals_ignore_case(self, s1, s2):
        """
        Author: Angie Pinchbeck
        Date created: 27/03/2018
        Date last modified: 27/03/2018

        This method compares two strings case-insensitively and returns true if they're the same.

        :param s1: The first string to compare.
        :param s2: The second string to compare.
        :return: boolean: True if they are the same, False if they are different.
        """
        return unicodedata.normalize("NFKD", s1.casefold()) == unicodedata.normalize("NFKD", s2.casefold())


    def runTranslator(self, tagMap):
        """
        Author: Angie Pinchbeck
        Date created: 26/03/2018
        Date last modified: 26/03/2018

        This is a method that will run an input tagMap through all the other translation methods, and then return a list
        of all the queries that are output.

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A list of Cypher queries.
        """
        results = []
        if self.match_label_and_property(tagMap) != -1:
            results.append("query1: " + self.match_label_and_property(tagMap))
        if self.returnName(tagMap) != -1:
            results.append("query2: " + self.returnName(tagMap))
        if self.listAllOf(tagMap) != -1:
            results.append("query3: " + self.listAllOf(tagMap))
        if self.numberStartsWith(tagMap) != -1:
            results.append("query5: " + self.numberStartsWith(tagMap))


        return results

    def match_label_and_property(self, tagMap):
        """
        Author: Angie Pinchbeck, Kevin Feddema (where indicated)
        Date created: 25/03/2018
        Date last modified: 28/03/2018

        This method filters a node for one label only, and returns a list of the properties asked for.

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A Cypher query as a string if appropriate; else, -1.
        """

        """
        Check that there aren't two labels in the words of the tagMap. If there are, this method shouldn't handle it; 
        return -1.
        NOTE: 
            This feature has been added after some failed unittest; it was noted that occasionally nltk.pos_tag doesn't 
            actually tag the words correctly. For example, in the sentence "Who are all the people that are outlaws?", 
            'outlaws' is obviously a noun. But nltk.pos_tag gives in the Stanford CoreNLP tag of 'VBN', that is, a verb 
            past participle. To combat this problem, we first do a quick check by running the words in the tagMap 
            against the words in the labels list.  
        
        """
        labelCount = 0
        for tm in tagMap:
            for l in self.labels:
                if self.equals_ignore_case(tm[0], l):
                    labelCount += 1
        if labelCount > 1:
            return -1

        """
        keywords: A list of words that indicate that the user wants an identifying quality of a Label returned.
        NOTE:
            This operates under the assumption that the database has been designed in such a way that the first
            property listed under any node is the "defining quality". For example, 'name' is usually the first
            thing listed for any kind of person, or 'title' is the first thing listed for a movie/book. This is 
            simply human nature--we tend to write the thing we believe to be the most important, first. 
            However, it will obviously not work if the database has been designed differently.
            This is a section of the program where some reinforcement machine learning could come in handy. 
        """
        keywords = ["who", "every", "each", "all", "list", "return"]

        nounTags = ["NN", "NNS", "NNP", "NNPS"]

        """ Be sure there are at least two nouns to work with """
        nounCount = 0
        for item in tagMap:
            if item[1] in nounTags:
                nounCount += 1
            elif item[0] in keywords:   # another noun has been implied if one of the keywords has been used
                nounCount += 1
        if nounCount < 2:
            return -1

        """
        This portion of the code is a modified version of code written by Kevin Feddema. It determines whether or not
        there are words that indicate the user is asking for a "count" of some kind. If there is, then this method
        should not handle it; return -1.
        
        countIndicator: This will be 1 if "count" is indicated, 0 if not.
        """
        countIndicator = 0
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
        if countIndicator == 1:
            return -1

        """ Create a list of all the nouns in this tagMap """
        nouns = []
        for item in tagMap:
            if item[1] in nounTags:
                nouns.append(item[0])

        """
        Populate a list of the nouns that are labels.
        """
        labelNouns = []
        for n in nouns:
            for l in self.labels:
                if self.equals_ignore_case(n, l):
                    labelNouns.append(n)
        """
        Check that there is only 1 "label" noun. If otherwise, this method should not handle it, return -1.
        If it only has one, assign that one to "label".
        NOTE:
            This code is slightly redundant after having checked the labels at the beginning of this method, 
            but it is kept here for two reasons: One, in case the tagging situation is ever resolved, and two,
            as it assigns the value label.   
        """
        if len(labelNouns) != 1:
            return -1
        else:
            label = labelNouns[0].capitalize()

        """
        Populate a list of the nouns that are properties.
        NOTE:
            The list "keywords" comes into play here. We are assuming that if a user has used a certain keyword, they are 
            implying the use of a defining property, which we are assuming is the first property listed under a node.
            We're assuming a lot.   
        """
        propertyNouns = []
        for tm in tagMap:
            for k in keywords:
                if self.equals_ignore_case(tm[0], k) and self.labelProperties[label][0] not in propertyNouns:
                    propertyNouns.append(self.labelProperties[label][0])

        for n in nouns:
            for item in self.labelProperties[label.capitalize()]:
                if self.equals_ignore_case(n, item) and n not in propertyNouns:
                    propertyNouns.append(n)

        """
        Build the final query.
        """
        prop = "n." + propertyNouns[0]
        if len(propertyNouns) > 1:
            for idx, pn in enumerate(propertyNouns):
                if idx != 0:
                    prop += ", " "n." + pn

        query1 = "MATCH (n :" + label + ") RETURN " + prop
        return query1


    def numberStartsWith(self, tagMap):
        """
        Author: Kevin Feddema
        Date created: 19/03/2018
        Date last modified: 25/03/2018

        The following method accepts a tokenized tag map and constructs a query for questions similar to "How many names
        begin with a J?" or "What is the number of people with a name starting with J?". This two questions are the most
        common when asking for the number of names that begin with a letter according to out NLP survey results

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A Cypher query as a string if appropriate; else, -1.
        """

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
        """
        Author: Osahon David Osemwegie
        Date created: 25/03/2018
        Date last modified: 26/03/2018

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A Cypher query as a string if appropriate; else, -1.
        """

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
            return -1
        else:
            output = "MATCH (n : {} : {} ) RETURN n.{}".format(preLabel, label, attribute)
        return output

    def listAllOf(self, tagMap):
        """
        Author: Kevin Feddema & Joseph Pruner
        Date created: 25/03/2018
        Date last modified: 26/03/2018

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A Cypher query as a string if appropriate; else, -1.
        """
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

sysin = sys.argv[1:]
string = " ".join(sysin)
#string = "Who are the outlaws and what are the bounties on them?"
#string = "What are the species of each the animals?"
#string = "How many names start with J?"
#string = "Show me all the species that are dogs?"
#string = "what are the names of the outlaws"
#string = "Who are all the outlaws?"
#string = "give me a list of all the outlaws"
#string = "Which animals are also outlaws?"
#string = "Who are the people that are outlaws?"

""" Create a tokenize object on the input string and print the tuple of the scrubbed words and their tags. """
t = Tokenize(string)
tagMap = t.wordsTagged
#print(tagMap)
#print(t.matchLabelAndProperty(tagMap))
#print(t.numberStartsWith(tagMap))
#print(t.listAllOf(tagMap))
#print(t.returnName(tagMap))

results = t.runTranslator(tagMap)
for item in results:
    print(item)


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

