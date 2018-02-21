import nltk

def getStatement():
    statement = input("Search: ")
    return statement

def Tokenize(statement):
    words = nltk.word_tokenize(statement)
    return words

statement = getStatement()
words = Tokenize(statement)
tags = nltk.pos_tag(words)
print(words)
print(tags)


