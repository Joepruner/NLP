import unittest
from Tokenize import Tokenize

class TestTokenize(unittest.TestCase):

    query1_1 = "MATCH (n :Person) RETURN n.name"
    query1_2 = "MATCH (n :Outlaw) RETURN n.name, n.bounty"
    query1_3 = "MATCH (n :Animal) RETURN n.name, n.species"
    query5_1 = "MATCH (n) WHERE n.name STARTS WITH \"J\" RETURN COUNT (n.name)"

    """
    Test that stopWords from Python's NLTK is working.
    """
    def test_stopWords(self):
        string = "from above into myself"
        t = Tokenize(string)
        self.assertEqual(t.wordsTagged, [])

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
    Test match_label_and_property with query1_1, defined above.
    """
    def test1_match_label_and_property(self):
        string = "What are the names of all the people?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_1)

    """
    Test match_label_and_property with query1_1, defined above, with lowercase.
    """
    def test2_match_label_and_property(self):
        string = "what are the names of all the people?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_1)

    """
    Test match_label_and_property with query1_1, defined above, with uppercase.
    """
    def test3_match_label_and_property(self):
        string = "WHAT ARE THE NAMES OF ALL THE PEOPLE?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_1)

    """
    Test match_label_and_property with a "how many" question; should return -1.
    """
    def test4_match_label_and_property(self):
        string = "How many names start with J?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), -1)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test5_match_label_and_property(self):
        string = "What are the names and bounties of the outlaws?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test6_match_label_and_property(self):
        string = "Who are the outlaws and what are the bounties on them?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_3, defined above.
    """
    def test7_match_label_and_property(self):
        string = "What is the species of each animal?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_3)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test8_match_label_and_property(self):
        string = "What's the bounty on every outlaw?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_3, defined above.
    """

    def test9_match_label_and_property(self):
        string = "What are the species of all the animals?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_3)

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