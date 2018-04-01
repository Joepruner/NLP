import unittest
from sprint4.Tokenize import Tokenize


class TestTokenize(unittest.TestCase):

    query1_1 = "MATCH (n :Person) RETURN n.name"
    query1_2 = "MATCH (n :Outlaw) RETURN n.name"
    query1_3 = "MATCH (n :Outlaw) RETURN n.bounty"
    query1_4 = "MATCH (n :Outlaw) RETURN n.name, n.bounty"
    query1_5 = "MATCH (n :Outlaw) RETURN n.name, n.bounty, n.size"

    query3_1 = "MATCH (n) RETURN n.species"
    query3_2 = "MATCH (n) where exists (n.species) RETURN n"
    query3_3 = "MATCH (n {species :'dog'}) RETURN n"
    query3_4 = "MATCH (n {name :'michael'}) RETURN n"
    query3_5 = "MATCH (n {name :'jeffery'}) RETURN n"
    query3_6 = "MATCH (n {bounty :'1000'}) RETURN n"
    query3_7 = "MATCH (n) where exists (n.bounty) RETURN n"
    query3_8 = "MATCH (n) RETURN n.bounty"

    query5_1 = "MATCH (n) WHERE n.name STARTS WITH \"J\" RETURN COUNT (n.name)"

    query7_1 = "MATCH (p) -[:parents] -> (n) RETURN n.name"

    """REMOVE COMMENTS BEFORE PUSHING!!!!!"""
    # """
    # Test that stopWords from Python's NLTK is working.
    # """
    # def test_stopWords(self):
    #     string = "from above into myself"
    #     t = Tokenize(string)
    #     self.assertEqual(t.wordsTagged, [])
    #
    # """
    # Test that stopWords is working even though the input has capital letters.
    # """
    # def test_stopWords_capitalized(self):
    #     string = "FROM ABOVE INTO MYSELF"
    #     t = Tokenize(string)
    #     self.assertEqual(t.wordsTagged, []);
    #
    # """
    # Test that keptStopWords is working
    # """
    # def test_keptStopWords(self):
    #     string = "How do you do"
    #     t = Tokenize(string)
    #     self.assertEqual(t.wordsTagged, [('how', 'WRB')]);
    #
    # """
    # Test match_label_and_property with query1_1, defined above.
    # """
    # def test1_match_label_and_property(self):
    #     string = "What are the names of all the people?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_1)
    #
    # """
    # Test match_label_and_property with query1_1, defined above, with lowercase.
    # """
    # def test2_match_label_and_property(self):
    #     string = "what are the names of all the people?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_1)
    #
    # """
    # Test match_label_and_property with query1_1, defined above, with uppercase.
    # """
    # def test3_match_label_and_property(self):
    #     string = "WHAT ARE THE NAMES OF ALL THE PEOPLE?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_1)
    #
    # """
    # Test match_label_and_property with a "how many" question; should return -1.
    # """
    # def test4_match_label_and_property(self):
    #     string = "How many names start with J?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), -1)
    #
    # """
    # Test match_label_and_property with two labels question; should return -1.
    # """
    # def test5_match_label_and_property(self):
    #     string = "Who are the people that are outlaws?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), -1)
    #
    # """
    # Test match_label_and_property with two labels question; should return -1.
    # """
    # def test6_match_label_and_property(self):
    #     string = "What are the names of the outlaws and their animals?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), -1)
    #
    # """
    # Test match_label_and_property with two labels question; should return -1.
    # """
    # def test7_match_label_and_property(self):
    #     string = "Which animals are also outlaws? "
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), -1)
    #
    # """
    # Test match_label_and_property with query1_2, defined above.
    # """
    # def test8_match_label_and_property(self):
    #     string = "Who are all the outlaws?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)
    #
    # """
    # Test match_label_and_property with query1_2, defined above.
    # """
    # def test9_match_label_and_property(self):
    #     string = "What are the names of all the outlaws?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)
    #
    # """
    # Test match_label_and_property with query1_2, defined above.
    # """
    # def test10_match_label_and_property(self):
    #     string = "What’s the name of each outlaw?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)
    #
    # """
    # Test match_label_and_property with query1_2, defined above.
    # """
    # def test11_match_label_and_property(self):
    #     string = "List each outlaw"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)
    #
    # """
    # Test match_label_and_property with query1_2, defined above.
    # """
    # def test12_match_label_and_property(self):
    #     string = "Give me a list of every outlaw"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)
    #
    # """
    # Test match_label_and_property with query1_2, defined above.
    # """
    # def test13_match_label_and_property(self):
    #     string = "List the names of the outlaws"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)
    #
    # """
    # Test match_label_and_property with query1_2, defined above.
    # """
    # def test14_match_label_and_property(self):
    #     string = "Return a list of the outlaw’s names"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)
    #
    # """
    # Test match_label_and_property with query1_3, defined above.
    # """
    # def test15_match_label_and_property(self):
    #     string = "What are the bounties on the outlaws?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_3)
    #
    # """
    # Test match_label_and_property with query1_4, defined above.
    # """
    # def test16_match_label_and_property(self):
    #     string = "List the bounties on the outlaws"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)
    #
    # """
    # Test match_label_and_property with query1_4, defined above.
    # """
    # def test17_match_label_and_property(self):
    #     string = "What are the names and bounties of the outlaws?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)
    #
    # """
    # Test match_label_and_property with query1_4, defined above.
    # """
    # def test18_match_label_and_property(self):
    #     string = "Who are the outlaws and what are the bounties on them?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)
    #
    # """
    # Test match_label_and_property with query1_4, defined above.
    # """
    # def test19_match_label_and_property(self):
    #     string = "What's the bounty on every outlaw?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)
    #
    # """
    # Test match_label_and_property with query1_4, defined above.
    # """
    # def test20_match_label_and_property(self):
    #     string = "What’s the bounty for each outlaw?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)
    #
    # """
    # Test match_label_and_property with query1_4, defined above.
    # """
    # def test21_match_label_and_property(self):
    #     string = "What are the bounties on all the outlaws?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)
    #
    # """
    # Test match_label_and_property with query1_4, defined above.
    # """
    # def test22_match_label_and_property(self):
    #     string = "List the outlaws and their bounties."
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)
    #
    # """
    # Test match_label_and_property with query1_5, defined above.
    # """
    # def test23_match_label_and_property(self):
    #     string = "What are the names, bounties, and sizes of each outlaw?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_5)
    #
    # """
    # Test match_label_and_property with query1_5, defined above.
    # """
    # def test24_match_label_and_property(self):
    #     string = "What’s the bounty and size for each outlaw?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_5)
    #
    # """
    # Test match_label_and_property with query1_5, defined above.
    # """
    # def test25_match_label_and_property(self):
    #     string = "Give me a list of the names, bounties, and sizes for every outlaw."
    #     t = Tokenize(string)
    #     self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_5)
    #
    #
    # """
    # Test for Kevin Feddema's numberStartsWith method for query5_1, defined above, with lowercase.
    # """
    # def test1_numberStartsWith(self):
    #     string = "how many names start with J?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)
    #
    # """
    # Test for Kevin Feddema's numberStartsWith method for query5_1, defined above, with uppercase.
    # """
    # def test2_numberStartsWith(self):
    #     string = "HOW MANY NAMES START WITH J?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)
    #
    # """
    # Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    # """
    # def test3_numberStartsWith(self):
    #     string = "How many names start with J?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)
    #
    # """
    # Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    # """
    # def test4_numberStartsWith(self):
    #     string = "How many of the names start with a J?"
    #     t = Tokenize(string)
    #     self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """break"""
    def test1_listAllWithProperty(self):
        string = "Show me all the species."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_1)

    def test2_listAllWithProperty(self):
        string = "Show me every species."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_1)

    def test3_listAllWithProperty(self):
        string = "List the species."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_1)

    def test4_listAllWithProperty(self):
        string = "What are all the species?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_1)

    def test5_listAllWithProperty(self):
        string = "What are the species?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_1)

    def test6_listAllWithProperty(self):
        string = "Show me everything that is a species."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_2)

    def test7_listAllWithProperty(self):
        string = "What is a species?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_2)

    def test8_listAllWithProperty(self):
        string = "Who are species?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_2)

    def test8_listAllWithProperty(self):
        string = "Show me all the species that are dogs."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_3)

    def test9_listAllWithProperty(self):
        string = "What has a species of dog?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_3)

    def test10_listAllWithProperty(self):
        string = "Of all the species which are dogs?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_3)

    def test11_listAllWithProperty(self):
        string = "Show me everyone named Michael."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_4)

    def test12_listAllWithProperty(self):
        string = "Who is named Michael?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_4)

    def test13_listAllWithProperty(self):
        string = "Whos name is Jeffery?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_5)

    def test14_listAllWithProperty(self):
        string = "Who has the name Jeffery?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_5)

    def test15_listAllWithProperty(self):
        string = "Who has a bounty of 1000?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_6)

    def test16_listAllWithProperty(self):
        string = "Whos bounty is 1000?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_6)

    def test17_listAllWithProperty(self):
        string = "Show me everyone with a bounty of 1000?"
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_6)

    def test18_listAllWithProperty(self):
        string = "Show me everyone with a bounty on them."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_7)

    def test19_listAllWithProperty(self):
        string = "Who has a bounty."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_7)

    def test20_listAllWithProperty(self):
        string = "Show me everyones bounty."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_8)

    def test21_listAllWithProperty(self):
        string = "List every bounty."
        t = Tokenize(string)
        self.assertEqual(t.listAllWithProperty(t.wordsTagged), self.query3_8)

    def test1_relationshipOrder(self):
        string = "What are the names of everyone with parents?"
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_1)



if __name__ == '__main__':
    unittest.main()