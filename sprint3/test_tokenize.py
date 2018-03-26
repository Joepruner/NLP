import unittest
from Tokenize import Tokenize

class TestTokenize(unittest.TestCase):

    query1_1 = "MATCH (p :Person) RETURN p.name"
    query1_2 = "MATCH (m :Movie) RETURN m.title"
    query5_1 = "MATCH (n) WHERE n.name STARTS WITH \"J\" RETURN COUNT (n.name)"

    """
    Test that stopWords from Python's NLTK is working.
    """
    def test_stopWords(self):
        string = "from above into myself"
        t = Tokenize(string)
        self.assertEqual(t.wordsTagged, []);

    """
    Test that stopWords is working even though the input has capital letters. 
    """
    def test_stopWords_capitalized(self):
        string = "FROM ABOVE INTO MYSELF"
        t = Tokenize(string)
        self.assertEqual(t.wordsTagged, []);

    """
    Test that keptStopWords is working
    """
    def test_keptStopWords(self):
        string = "How do you do"
        t = Tokenize(string)
        self.assertEqual(t.wordsTagged, [('how', 'WRB')]);

    """
    Test matchLabelAndProperty with query1_1, defined above.
    """
    def test1_matchLabelAndProperty(self):
        string = "What are the names of all the people?"
        t = Tokenize(string)
        self.assertEqual(t.matchLabelAndProperty(t.wordsTagged), self.query1_1)

    """
    Test matchLabelAndProperty with query1_1, defined above, with lowercase.
    """
    def test2_matchLabelAndProperty(self):
        string = "what are the names of all the people?"
        t = Tokenize(string)
        self.assertEqual(t.matchLabelAndProperty(t.wordsTagged), self.query1_1)

    """
    Test matchLabelAndProperty with query1_1, defined above, with uppercase.
    """
    def test3_matchLabelAndProperty(self):
        string = "WHAT ARE THE NAMES OF ALL THE PEOPLE?"
        t = Tokenize(string)
        self.assertEqual(t.matchLabelAndProperty(t.wordsTagged), self.query1_1)

    """
    Test matchLabelAndProperty with a "how many" question; should return -1.
    """

    def test4_matchLabelAndProperty(self):
        string = "How many names start with J?"
        t = Tokenize(string)
        self.assertEqual(t.matchLabelAndProperty(t.wordsTagged), -1)

    """
    Test matchLabelAndProperty with query1_2, defined above.
    """
    def test5_matchLabelAndProperty(self):
        string = "What are all the movie titles?"
        t = Tokenize(string)
        self.assertEqual(t.matchLabelAndProperty(t.wordsTagged), self.query1_2)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above, with lowercase.
    """
    def test1_numberStartsWith(self):
        string = "how many names start with J?"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above, with uppercase.
    """
    def test2_numberStartsWith(self):
        string = "HOW MANY NAMES START WITH J?"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test3_numberStartsWith(self):
        string = "How many names start with J?"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test4_numberStartsWith(self):
        string = "How many of the names start with a J?"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)


if __name__ == '__main__':
    unittest.main()