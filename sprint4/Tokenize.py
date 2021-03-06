"""
Tokenize.py:
This program tokenizes and assigns Stanford CoreNLP tags to a sentence. Input can either be standard input or sysin.

File name: Tokenize.py
Author: Angie Pinchbeck, Joseph Pruner
Date created: 27/02/2018
Date last modified: 02/04/2018
Python version: 3.5

Much of this was based on a tutorial from:
.. _Python Tutorials
    https://pythonspot.com/category/nltk/

As much of possible, we have used the Google style guide for Python:
.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""

import unicodedata  # for case-insensitive comparisons
from itertools import product

import nltk
"""I needed to import sys or I got an error -Joe"""
import sys
from inflection import singularize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import sys

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
                    Expanded kept stop words: now includes "each".
        30/03/2018  Expanded kept stop words: now includes "than".
        02/04/2018  Fixed queries 5 and 6 to pass all tests. Add queries 3 and 7. All methods pass all 92 tests. 

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
    
    keptStopWords = ["how", "all", "with", "have", "has", "who", "are", "and", "is", "each", "than"]
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

        # MATCH n-[r]-() RETURN distinct type(r)
        self.relationships = ["likes", "dislikes", "parents", "brother"]

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

        string1 = u"{}".format(s1)
        string2 = u"{}".format(s2)
        return unicodedata.normalize('NFKD', string1.lower()) == unicodedata.normalize('NFKD', string2.lower())

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
        if self.listAllWithProperty(tagMap) != -1:
            results.append("query3: " + self.listAllWithProperty(tagMap))
        if self.return_multiple_labels(tagMap) != -1:
            results.append("query2: " + self.return_multiple_labels(tagMap))
        if self.numberStartsWith(tagMap) != -1:
            results.append("query5: " + self.numberStartsWith(tagMap))
        if self.numberNullOrNot(tagMap) != -1:
            results.append("query6: " + self.numberNullOrNot(tagMap))
        if self.relationshipOrder(tagMap) != -1:
            results.append("query7: " + self.relationshipOrder(tagMap))

        return results

    def similarity_score(self, wordx, wordy):
        """
        Author: Angie Pinchbeck
        Date created: 30/03/2018
        Date last modified: 30/03/2018

        This is a method that determines how closely related two words are--not that they are similar in spelling or
        grammar, but that they are conceptually related. For example, if the words "tall" and "size" are checked,
        the method returns 0.9090909090909091, indicating that the words "tall" and "size" are closely related. However,
        if the words "cabbage" and "spaceship" are compared, it returns 0.38095238095238093. Words that are almost
        identical, such as "parent" and "parents" return 1.0.

        :param wordx: The first word for comparison.
        :param wordy: The second word for comparison.
        :return: A float representation of how closely related two words are. The closer to 1, the more related.
        """
        sem1, sem2 = wn.synsets(wordx), wn.synsets(wordy)
        maxscore = float(0)
        for i, j in list(product(sem1, sem2)):
            score = i.wup_similarity(j)  # Wu-Palmer
            if score is not None and maxscore < score:
                maxscore = score
        return maxscore

    def match_label_and_property(self, tagMap):
        """
        Author: Angie Pinchbeck, Kevin Feddema (where indicated)
        Date created: 25/03/2018
        Date last modified: 30/03/2018

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
                if self.similarity_score(tm[0], l) > 0.9:
                    labelCount += 1
        if labelCount > 1:
            return -1

        """
        Check that there are no relationship nouns in the words of the tagMap. If there are, this method shouldn't 
        handle it; return -1;
        """
        relationshipCount = 0
        for tm in tagMap:
            for r in self.relationships:
                # print(self.similarity_score(tm[0], r))
                if self.similarity_score(tm[0], r) > 0.9:
                    relationshipCount += 1
        if relationshipCount > 0:
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
            elif item[0] in keywords:  # another noun has been implied if one of the keywords has been used
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
        Date last modified: 02/04/2018

        The following method accepts a tokenized tag map and constructs a query for questions similar to "How many names
        begin with a J?" or "What is the number of people with a name starting with J?". These two questions are the
        most common when asking for the number of names that begin with a letter according to out NLP survey results.
        This method will only execute if all the 3 indicators have been given a value of 1, else the method returns -1.
        The 3 indicators are the countIndicator, the letterIndicator, and the letterPosIndicator.

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A Cypher query as a string if appropriate; else, -1.
        """

        query5 = ""  # the final query that is returned after processing
        startWords = {"start", "starting", "begin", "beginning", "first", "front"} #Words indicating STARTS WITH
        endWords = {"end", "ending", "last", "back"} #Words indicating ENDS WITH
        containWords = {"contain", "position"}
        countIndicator = 0  # countIndicator is either 1 or 0. 1 if there is a chunk or part of speach that indicates
        # the need to return count and 0 if not
        letterPosIndicator = 0  # 1 or 0. 1 if input contains any one of the start words
        letterIndicator = 0  # 1 or 0. 1 if input contains any one of the end words
        attribute = "" #The attribute of the query
        condition = "" #The condition of the query
        value = "" # The value or letter for the query

        """Determine if a "How many" count indicator is present"""
        chunkSequence = '''Chunk:{<WRB>+ <JJ>+}'''
        NPChunker = nltk.RegexpParser(chunkSequence)
        chunks = NPChunker.parse(tagMap)
        for n in chunks:
            if isinstance(n, nltk.tree.Tree):
                if n.label() == 'Chunk':
                    howMany = n
                    countIndicator = 1

        """Determine if all three indicators are present in the user's input and assign condition"""
        """
        NOTE:
        The position of the containWords if statement must be positioned before the startWords check and the endWords
        check because if the user asks "How many names have a J in the start position" the query will still be 
        returned correctly in that the condition will initially be set to "CONTAINS" because position is a member of
        containsWords, but the value will be overwritten by "STARTS WITH" after reaching the startWords check.
        """
        for elem in tagMap:
            if elem[0] == 'number':
                countIndicator = 1
            if elem[0] in containWords:
                letterPosIndicator = 1
                condition = "CONTAINS"
            if elem[0] in startWords:
                letterPosIndicator = 1
                condition = "STARTS WITH"
            if elem[0] in endWords:
                letterPosIndicator = 1
                condition = "ENDS WITH"
            if len(elem[0]) == 1:
                if elem[0].isalpha() and elem[1] == 'NN':
                    letterIndicator = 1
        # print("count indicator is "+str(countIndicator))
        # print("letterPos indicator is "+str(letterPosIndicator))
        # print("letter indicator is "+str(letterIndicator))
        # print("attribute is "+attribute)
        # print("condition is "+condition)
        # print("value is "+value)

        """If all indicators are not found in the question, the question cannot be handled by this method, return -1"""
        if countIndicator == 0 or (letterPosIndicator == 0 and letterIndicator == 0):
            return -1

        """Determine NNS similarity to database label properties and assign attribute"""
        maxLabelProp = ""
        maxScore = 0
        for elem in tagMap:
            print(elem)
            if len(elem[0]) == 1:
                if elem[0].isalpha() and elem[1] == 'NN'or elem[1] == 'JJ':
                    letterIndicator = 1
                    value = elem[0].capitalize()
            if elem[1] == 'RB' or elem[1] == 'NNS' or elem[1] == 'NN':
                for label in self.labelProperties.values():
                    for labelProp in label:
                        score = self.similarity_score(labelProp, elem[0])
                        if score >= maxScore:
                            maxLabelProp = labelProp
                            maxScore = score
        attribute = maxLabelProp

        query5 = "MATCH (n) WHERE n." + attribute + " " + condition + " \"" + value + "\" " + "RETURN COUNT (n." + attribute + ")"
        return query5

    def numberNullOrNot(self, tagMap):
        """
        Author: Kevin Feddema
        Date created: 31/03/2018
        Date last modified: 01/04/2018

        The following method accepts a tokenized tag map and constructs a query for questions similar to "What
        is the number of animals with a known specie". Much like the numberStartsWith method, the numberNullOrNot
        determines if the question contains a count indicator and analyzes accordingly. This method does not handle
        anything more complicated than NULL or NOT NULL questions, for example "What is the number of animals that
        are dogs" as this would require querying the database for all possible values for species in order to
        correctly differentiate between a numberStartsWith and a numberNullOrNot question.

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A Cypher query as a string if appropriate; else, -1.
        """
        print("Test test test")

        query6 = ""  # the final query that is returned after processing
        nullWords = {"unknown"} # Words indicating an IS NULL condition
        notNullWords = {"known"} # Words indicating an IS NOT NULL condition
        countIndicator = 0  # countIndicator is either 1 or 0. 1 if there is a count indicator
        nullIndicator = 0  # 1 or 0. 1 if input contains any one of the null words
        attribute = ""  # The attribute of the query
        condition = ""  # The condition of the query

        """Determine if a "How many" count indicator is present"""
        chunkSequence = '''Chunk:{<WRB>+ <JJ>+}'''
        NPChunker = nltk.RegexpParser(chunkSequence)
        chunks = NPChunker.parse(tagMap)
        for n in chunks:
            if isinstance(n, nltk.tree.Tree):
                if n.label() == 'Chunk':
                    howMany = n
                    countIndicator = 1

        """Determine if the two indicators are present in the user's input and assign condition"""
        for elem in tagMap:
            if elem[0] == 'number':
                countIndicator = 1
            if elem[0] in nullWords:
                nullIndicator = 1
                condition = "IS NULL"
            if elem[0] in notNullWords:
                nullIndicator = 1
                condition = "IS NOT NULL"
        print("count indicator is " + str(countIndicator))
        print("null indicator is " + str(nullIndicator))
        print("attribute is " + attribute)
        print("condition is " + condition)
        """If the two indicators are not found in the question, the question cannot be handled by this method, return -1"""
        if countIndicator == 0 or nullIndicator == 0:
            return -1

        """Determine NNS similarity to database label properties and assign attribute"""
        maxLabelProp = ""
        maxScore = 0
        for elem in tagMap:
            if elem[1] == 'RB' or elem[1] == 'NNS' or elem[1] == 'NN':
                for label in self.labelProperties.values():
                    for labelProp in label:
                        score = self.similarity_score(labelProp, elem[0])
                        if score >= maxScore:
                            maxLabelProp = labelProp
                            maxScore = score
        attribute = maxLabelProp
        query6 = "MATCH (n) WHERE n." + attribute + " " + condition + " RETURN COUNT (n." + attribute + ")"
        return query6

    def return_multiple_labels(self, tagMap):
        """
        Author: Osahon David Osemwegie
        Date created: 25/03/2018
        Date last modified: 26/03/2018

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A Cypher query as a string if appropriate; else, -1.
        """

        """Sample Question: What are the names of the outlaws and Animals"""
        """This is a list of words that """

        keywords = ["who", "every", "each", "all", "list", "return"]

        nounTags = ["NN", "NNS", "NNP", "NNPS"]

        """Check to see there are more than 1 labels in the words of the Tagmap
        If so then return -1.
        Also checks to see if there are any relationship words in the tagMap
        If ss or less return -1
        Note: This section of code is is a modified version of code written by Angie Pinchbeck"""

        labelCount = 0
        relationshipCount = 0
        for t in tagMap:
            for a in self.labels:
                if self.similarity_score(t[0], a) > 0.9:
                    labelCount += 1
            for b in self.relationships:
                if self.similarity_score(t[0], b) > 0.9:
                    relationshipCount += 1
        if labelCount <= 1 or relationshipCount > 1:
            return -1

        """Check to see if the user is asking for a 'count' if so then return -1"""
        """Note: This section of code is is a modified version of code written by Kevin Feddema and Angie Pinchbeck"""

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

        "Creating a of nouns"
        listOfNouns = []
        for i in tagMap:
            if i[1] in nounTags:
                listOfNouns.append(i[0])

        """Get the nouns that are labels"""
        nounLabels = []
        for n in listOfNouns:
            for l in self.labels:
                if self.equals_ignore_case(n, l):
                    nounLabels.append(n)

        labels = []

        """Check to make sure that are more than 2 labels else return -1"""

        labelCount = len(nounLabels)

        if labelCount < 2:
            return -1
        else:
            for i in nounLabels:
                labels.append(i.capitalize())

        """This is section of modified code written by Angie Pinchbek"""

        propertyNouns = []
        for tm in tagMap:
            for i in labels:
                for k in keywords:
                    if self.equals_ignore_case(tm[0], k) and self.labelProperties[i][0] not in propertyNouns:
                        propertyNouns.append(self.labelProperties[i][0])

        for n in listOfNouns:
            for i in labels:
                for item in self.labelProperties[i.capitalize()]:
                    if self.equals_ignore_case(n, item) and n not in propertyNouns:
                        propertyNouns.append(n)

        properties = "n." + propertyNouns[0]

        """NOTE: Code snippet from Angie Pinchbek"""
        if len(propertyNouns) > 1:
            for idx, pn in enumerate(propertyNouns):
                if idx != 0:
                    properties += ", " "n." + pn

        labelList = ""

        for i in labels:
            labelList += " :" + i

        """Construct Query"""
        query = "MATCH (n {} ) RETURN {}".format(labelList, properties)

        return query

    """
    Method name: listAllof
    Author: Kevin Feddema & Joseph Pruner
    Date created: 25/03/2018
    Date last modified: 26/03/2018
    Python version: Anaconda 3.6
    """

    def listAllWithProperty(self, tagMap):
        """
        Author: Joseph Pruner & Kevin Feddema
        Date created: 25/03/2018
        Date last modified: 02/04/2018

        This method lists all nodes that have a specific property, and optional subtype of property (i.e. Species that is dog).
        You can either have the list of results be the entire node, or just the list of the designated property.

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A Cypher query as a string if appropriate; else, -1.
        """
        propertyIndicator = 0
        property = ""
        propertySubType = ""

        """Do not handle this query if there are relationships or labels in it."""
        for elem in tagMap:
            if elem[0].lower() in self.labels or elem[0].lower() in self.relationships:
                return -1
        for i in range(tagMap.__len__()):
            if tagMap[i][0] == "named":
                tagMap.pop([i][0])
                tagMap.insert([i][0], ("name", 'NN'))
                property = "name"
                propertyIndicator = 1
                break
            if tagMap[i][0] == "list":
                tagMap.pop([i][0])
                tagMap.insert([i][0], ("list", 'VB'))
                break
        if propertyIndicator == 0:
            for elem in tagMap:
                if elem[0] in [x for y in self.labelProperties.values() for x in y] and property == "":
                        property = elem[0]
                        propertyIndicator = 1
        # print(tagMap)

        if propertyIndicator == 0:
            return -1
        nounTagList = ['NN', 'NNS', 'NNP', 'NNPS', 'CD']
        proNounVerbPosessiveList = ['WP', 'WP$', 'VBP', 'VBZ']
        allEvery = ["all", "every"]
        hasHaveIs = ['has', 'ha', 'have', 'is', 'i']
        query3 = ""
        nodeIsProperty = False

        triGrams = nltk.trigrams(tagMap)
        biGrams = nltk.bigrams(tagMap)

        for tri in triGrams:
            # print(tri)
            if tri[0][0] in allEvery and tri[1][0] == property and tri[2][1] in nounTagList:
                propertySubType = tri[2][0]
            elif tri[0][0] in allEvery and tri[1][1] in nounTagList and tri[2][0] == property:
                 propertySubType = tri[1][0]
            elif tri[0][0] == property and tri[1][1] in proNounVerbPosessiveList and tri[2][1] in nounTagList:
                 propertySubType = tri[2][0]
        for bi in biGrams:
            # print(bi)
            if bi[0][0] == property and bi[1][1] in nounTagList:
                propertySubType = bi[1][0]
            elif bi[1][1] in nounTagList and bi[0][0] == property:
                propertySubType = bi[0][0]
            elif bi[0][1] not in nounTagList and bi[0][0] not in hasHaveIs and tagMap.__len__() < 5 and bi[1][0] == property:
                nodeIsProperty = True
        # print("property is "+property)
        # print("propertySubType is "+propertySubType)
        # print("nodeIsProperty is "+str(nodeIsProperty))

        if property != "" and propertySubType != "" and not nodeIsProperty:
            query3 = "MATCH (n {" + property + " :\'" + propertySubType + "\'" + "}) RETURN n"
        elif property != "" and propertySubType == "" and nodeIsProperty:
            query3 = "MATCH (n) RETURN n."+property
            """Show me everything that is a species """
        elif property != "" and propertySubType == "" and not nodeIsProperty:
            query3 = "MATCH (n) where exists (n." + property + ") RETURN n"
        return query3

    def relationshipOrder(self, tagMap):

        """Author: Joseph Pruner
        Date created: 30/03/2018
        Date last modified: 30/03/2018

        This method returns results based on the nodes relationships with each other.
        (i.e. Who has a parent, who is a parent, or what are the names of everyone that likes something etc.)
        Your results can be return either has the node list, or as a property of that node.

         :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
         :return: A Cypher query as a string if appropriate; else, -1.

        """
        relationshipIndicator = 0
        relationship = ""
        relationshipTarget = ""
        relatorProperty = False
        relatedProperty = False
        property = ""
        nounTagList = ['NN', 'NNS', 'NNP', 'NNPS']
        proNounPosessiveList = ['WP', 'WP$']
        allEvery = ["all", "every"]
        hasHave = ["has", "have", "ha", "with"]

        """Determine if there is a relationship in the user's input"""

        for elem in tagMap:
            print(elem[0])
            if elem[0]+"s" in self.relationships:
                relationship = elem[0]
                relationshipIndicator = 1
            elif elem[0] in [x for v in self.labelProperties.values() for x in v]:
                property = elem[0]
        if relationshipIndicator == 0:
            return -1
        print("In a relationship")

        query7 = ""
        triGrams = nltk.trigrams(tagMap)
        """Find the target of the relationship. i.e. parent of "Joe".
        for bi in biGrams:
            print(bi)
            if (bi[0][0] == relationship and bi[1][0] == property) or \
               (bi[0][0] == property and bi[1][0] == relationship) and bi[0][0]:
                noRelationshipTarget = True"""

        for tri in triGrams:
            print(tri)
            if (tri[0][0] == property and tri[1][1] in nounTagList and tri[2][0] == relationship)\
               or (tri[0][0] == relationship and tri[1][1] in nounTagList and tri[2][0] == property):
               relationshipTarget = tri[1][0]
            elif tri[0][1] in nounTagList and tri[1][0] == relationship and tri[2][0] == property:
               relationshipTarget = tri[0][0]
            elif tri[0][1] in proNounPosessiveList and tri[1][0] == relationship and tri[2][1] in nounTagList:
               relationshipTarget = tri[2][0]
            elif tri[0][1] in proNounPosessiveList and tri[1][1] in nounTagList and tri[2][0] == relationship:
               relationshipTarget = tri[1][0]
            elif tri[0][0] == property and tri[1][0] in allEvery and tri[2][0] == relationship:
                relatorProperty = True
            elif tri[0][0] == property and tri[1][0] in allEvery and tri[2][0] == relationship:
                relatorProperty = True

            if tri[0][1] in nounTagList and (tri[1][1] in hasHave or tri[1][1] in proNounPosessiveList)\
                    and tri[2][0] == relationship:
                relatedProperty = True
            elif tri[0][1] in proNounPosessiveList and tri[1][0] in hasHave and tri[2][0] == relationship:
                relatedProperty = True
            elif tri[0][1] in nounTagList and tri[1][0] in hasHave and tri[2][0] == relationship:
                relatedProperty = True
            elif tri[0][0] == relationship and tri[1][0] in hasHave and tri[2][1] in proNounPosessiveList:
                relatedProperty = True
            elif (tri[0][1] in proNounPosessiveList or tri[0][1] in nounTagList) and \
                    tri[1][0] == relationship and tri[2][1] in nounTagList:
                relatedProperty = True
                print("here")

            if relationshipTarget == "something" or "anything":
                relationshipTarget = ""
        print("relationship is " + relationship)
        print("relationship target is " + relationshipTarget)
        print("Property is " + property)
        print("relatorProperty is "+str(relatorProperty))
        print("relatedProperty is "+str(relatedProperty))
        relationship += "s"

        if relationshipTarget == "" and property != "" and not relatorProperty and not relatedProperty:
            query7 += "MATCH (p) -[:" + relationship + "] -> (n" + property + ") RETURN n"
        elif relationshipTarget == "" and relatorProperty:
            query7 += "MATCH (p) -[:" + relationship + "] -> (n) RETURN p." + property
        elif relationshipTarget == "" and relatedProperty and property != "":
            query7 += "MATCH (p) -[:" + relationship + "] -> (n) RETURN n." + property
        elif relationshipTarget == "" and relatedProperty and property == "":
            query7 += "MATCH (p) -[:" + relationship + "] -> (n) RETURN n"
        elif relationshipTarget == "" and property == "" and not relatedProperty and not relatorProperty:
            query7 += "MATCH (p) -[:" + relationship + "] -> (n) RETURN p"

        return query7

    def count_with_operators(self, tagMap):
        """
        Author: Angie Pinchbeck
        Date created: 30/03/2018
        Date last modified: 30/03/2018

        This method returns queries that are used for aggregating the results of filtering Nodes based on
        quantification of properties. It deals with the operators <, >, <>, =, >=, <=

        :param tagMap: A list of tuples consisting of words and their Stanford CoreNLP tags.
        :return: A Cypher query as a string if appropriate; else, -1.
        """

        """
        This portion of the code is a modified version of code written by Kevin Feddema. It determines whether or not
        there are words that indicate the user is asking for a "count" of some kind. If there is no count indicator, 
        then this method should not handle it; return -1.

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
        if countIndicator == 0:
            return -1

        keywords = ["than", "equal", "less", "greater"]


"""
The following code allows for input. 
When running from website use:
    string = " ".join(sysin)
When running from console use:
    string = input()  
For testing purposes, a while-loop is included at the bottom (commented out) that will allow for continual input and 
tokenization until "e" is entered. 
"""
# string = input()
sysin = sys.argv[1:]
string = " ".join(sysin)
#string = "What are the sizes of the animals and outlaws"
# string = "What are the names of the animals"
# string = "What are the female people"
# string = "What are the names of people with parents?"
# string = "How many outlaws have a bounty of less than $10,000 on them?"
# string = "Who are the outlaws and what are the bounties on them?"
# string = "What are the species of each the animals?"
# string = "How many names start with J?"
# string = "How many names have a J in any position"
# string = "How many names contain a J"
# string = "How many animals have an unknown specie"
# string = "Who are all the females that are outlaws?"
# string = "What are the names of people with parents from biggest smallest?"
# string = "what are the names of the outlaws"
# string = "Who are all the outlaws?"
# string = "give me a list of all the outlaws"
# string = "Which animals are also outlaws?"
# string = "Who are the people that are outlaws?"

""" Create a tokenize object on the input string and print the tuple of the scrubbed words and their tags. """
t = Tokenize(string)
tagMap = t.wordsTagged
# print(tagMap)
# print(t.matchLabelAndProperty(tagMap))
# print(t.numberStartsWith(tagMap))
# print(t.numberNullOrNot(tagMap))
# print(t.listAllOf(tagMap))
# print (t.labels)
# print ("LOL")

results = t.runTranslator(tagMap)
for item in results:
    print(item)

# print(t.match_label_and_property(tagMap))
# print(t.return_multiple_labels(tagMap))

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
