import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import sys

#string = "Show me the names of actors in the movie with title ""Cloud Atlas"""
sysin = sys.argv[1:]

string = " ".join(sysin)

# string  = "my name is david"
tag = "VB"


def showTags (string):
    word = nltk.word_tokenize(string)
    print nltk.pos_tag(word)

#string2 = "Show me the title of all the movies that ""Halle Berry"" acted in"

def output (string):

    print string + "<br>"
    print

    def findSpeechPart (string, tag):
        out = []
        sentences = nltk.sent_tokenize(string)
        data = []
        for sent in sentences:
            data = data + nltk.pos_tag(nltk.word_tokenize(sent))
        for word in data:
            if word[1] == tag:
                out.append(word)
        return out

    NNS = findSpeechPart(string, "NNS")

    NN = findSpeechPart(string, "NN")

    JJ = findSpeechPart(string,"JJ")

    NNP = findSpeechPart(string, "NNP")

    print "<br>" \
          "These are all of the Plural Nouns <br>" \
          "<br>"
    print (NNS)
    print "<br>" \
          "These are all of the Singular Nouns <br>" \
          "<br>"
    print (NN)
    print "<br>" \
          "These are all of the Adjectives <br>" \
          "<br>"
    print (JJ)
    print "<br>" \
          "These are all of the Singular Proper Nouns <br>" \
          "<br>"
    print (NNP)

showTags(string)

# print

# output(string2)
#
# print
#
# output("who acted in movie with title ""Cloud Atlas""")
#
# print
#
# output("who acted in movie ""Cloud Atlas""")
#
#
# showTags("who acted in movie ""Cloud Atlas"""
#          )

