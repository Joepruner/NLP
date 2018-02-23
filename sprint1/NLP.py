import nltk
import unittest

class UserIn:
    def __init__(self, search):
        self.statement = search
        self.tokens = nltk.word_tokenize(self.statement)
        self.tags = nltk.pos_tag(self.tokens)

userIn = UserIn(input("Search: "))
print(userIn.statement)
print(userIn.tokens)
print(userIn.tags)
