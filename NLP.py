import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

string = "Show me the names of actors in the movie with title ""Cloud Atlas"""
tag = "VB"


def showTags (string):
    word = nltk.word_tokenize(string)
    print nltk.pos_tag(word)

string2 = "Show me the title of all the movies that ""Halle Berry"" acted in"

def output (string):

    print string
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

    print "" \
          "These are all of the Plural Nouns" \
          ""
    print NNS
    print "" \
          "These are all of the Singular Nouns" \
          ""
    print NN
    print "" \
          "These are all of the Adjectives" \
          ""
    print JJ
    print "" \
          "These are all of the Singular Proper Nouns" \
          ""
    print NNP

output(string)

print

output(string2)

print

output("who acted in movie with title ""Cloud Atlas""")

print

output("who acted in movie ""Cloud Atlas""")


showTags("who acted in movie ""Cloud Atlas"""
         )

