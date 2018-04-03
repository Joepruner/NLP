import unittest
from sprint4.Tokenize import Tokenize

class TestTokenize(unittest.TestCase):

    query1_1 = "MATCH (n :Person) RETURN n.name"
    query1_2 = "MATCH (n :Outlaw) RETURN n.name"
    query1_3 = "MATCH (n :Outlaw) RETURN n.bounty"
    query1_4 = "MATCH (n :Outlaw) RETURN n.name, n.bounty"
    query1_5 = "MATCH (n :Outlaw) RETURN n.name, n.bounty, n.size"

    query2_1 = "MATCH (n  :Animal :Outlaw ) RETURN n.name"
    query2_2 = "MATCH (n  :Animal :Outlaw :Person ) RETURN n.name"
    query2_3 = "MATCH (n  :Outlaw :Person ) RETURN n.name, n.size"
    query2_4 = "MATCH (n  :Person :Outlaw ) RETURN n.size"

    query3_1 = "MATCH (n) RETURN n.species"
    query3_2 = "MATCH (n) where exists (n.species) RETURN n"
    query3_3 = "MATCH (n {species :'dog'}) RETURN n"
    query3_4 = "MATCH (n {name :'michael'}) RETURN n"
    query3_5 = "MATCH (n {name :'jeffery'}) RETURN n"
    query3_6 = "MATCH (n {bounty :'1000'}) RETURN n"
    query3_7 = "MATCH (n) where exists (n.bounty) RETURN n"
    query3_8 = "MATCH (n) RETURN n.bounty"

    query5_1 = "MATCH (n) WHERE n.name STARTS WITH \"J\" RETURN COUNT (n.name)"
    query5_2 = "MATCH (n) WHERE n.name ENDS WITH \"J\" RETURN COUNT (n.name)"
    query5_3 = "MATCH (n) WHERE n.name CONTAINS \"J\" RETURN COUNT (n.name)"

    query6_1 = "MATCH (n) WHERE n.species IS NOT NULL RETURN COUNT (n.species)"
    query6_2 = "MATCH (n) WHERE n.species IS NULL RETURN COUNT (n.species)"

    query7_1 = "MATCH (p) -[:parents] -> (n) RETURN n.name"
    query7_2 = "MATCH (p) -[:likes] -> (n) RETURN n.size"
    query7_3 = "MATCH (p) -[:parents] -> (n) RETURN n"
    query7_4 = "MATCH (p) -[:parents] -> (n) RETURN p"
    query7_5 = "MATCH (p) -[:dislikes] -> (n) RETURN n"

    """REMOVE COMMENTS BEFORE PUSHING!!!!!"""
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
    Test match_label_and_property with two labels question; should return -1.
    """
    def test5_match_label_and_property(self):
        string = "Who are the people that are outlaws?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), -1)

    """
    Test match_label_and_property with two labels question; should return -1.
    """
    def test6_match_label_and_property(self):
        string = "What are the names of the outlaws and their animals?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), -1)

    """
    Test match_label_and_property with two labels question; should return -1.
    """
    def test7_match_label_and_property(self):
        string = "Which animals are also outlaws? "
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), -1)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test8_match_label_and_property(self):
        string = "Who are all the outlaws?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test9_match_label_and_property(self):
        string = "What are the names of all the outlaws?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test10_match_label_and_property(self):
        string = "What’s the name of each outlaw?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test11_match_label_and_property(self):
        string = "List each outlaw"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test12_match_label_and_property(self):
        string = "Give me a list of every outlaw"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test13_match_label_and_property(self):
        string = "List the names of the outlaws"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_2, defined above.
    """
    def test14_match_label_and_property(self):
        string = "Return a list of the outlaw’s names"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_2)

    """
    Test match_label_and_property with query1_3, defined above.
    """
    def test15_match_label_and_property(self):
        string = "What are the bounties on the outlaws?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_3)

    """
    Test match_label_and_property with query1_4, defined above.
    """
    def test16_match_label_and_property(self):
        string = "List the bounties on the outlaws"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)

    """
    Test match_label_and_property with query1_4, defined above.
    """
    def test17_match_label_and_property(self):
        string = "What are the names and bounties of the outlaws?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)

    """
    Test match_label_and_property with query1_4, defined above.
    """
    def test18_match_label_and_property(self):
        string = "Who are the outlaws and what are the bounties on them?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)

    """
    Test match_label_and_property with query1_4, defined above.
    """
    def test19_match_label_and_property(self):
        string = "What's the bounty on every outlaw?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)

    """
    Test match_label_and_property with query1_4, defined above.
    """
    def test20_match_label_and_property(self):
        string = "What’s the bounty for each outlaw?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)

    """
    Test match_label_and_property with query1_4, defined above.
    """
    def test21_match_label_and_property(self):
        string = "What are the bounties on all the outlaws?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)

    """
    Test match_label_and_property with query1_4, defined above.
    """
    def test22_match_label_and_property(self):
        string = "List the outlaws and their bounties."
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_4)

    """
    Test match_label_and_property with query1_5, defined above.
    """
    def test23_match_label_and_property(self):
        string = "What are the names, bounties, and sizes of each outlaw?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_5)

    """
    Test match_label_and_property with query1_5, defined above.
    """
    def test24_match_label_and_property(self):
        string = "What’s the bounty and size for each outlaw?"
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_5)

    """
    Test match_label_and_property with query1_5, defined above.
    """
    def test25_match_label_and_property(self):
        string = "Give me a list of the names, bounties, and sizes for every outlaw."
        t = Tokenize(string)
        self.assertEqual(t.match_label_and_property(t.wordsTagged), self.query1_5)


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
        string = "Who has a bounty?"
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

    def test2_relationshipOrder(self):
        string = "Show me the names of people who have parents."
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_1)

    def test3_relationshipOrder(self):
        string = "What are the sizes of everyone with that likes someone?"
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_2)

    def test4_relationshipOrder(self):
        string = "Show me the sizes of people who like anything."
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_2)

    def test5_relationshipOrder(self):
        string = "Who has parents?"
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_3)

    def test6_relationshipOrder(self):
        string = "Show me everyone that has parents."
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_3)

    def test7_relationshipOrder(self):
        string = "Who are parents?."
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_4)

    def test8_relationshipOrder(self):
        string = "Show me everyone that is a parent."
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_4)

    def test9_relationshipOrder(self):
        string = "Who dislikes something?"
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_5)

    def test10_relationshipOrder(self):
        string = "Show me everyone that dislikes anything."
        t = Tokenize(string)
        self.assertEqual(t.relationshipOrder(t.wordsTagged), self.query7_5)


    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test5_numberStartsWith(self):
        string = "How many names begin with J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test6_numberStartsWith(self):
        string = "How many names begin with J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test7_numberStartsWith(self):
        string = "How many names have a J at the front"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test8_numberStartsWith(self):
        string = "How many names have a J at the beginning"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test9_numberStartsWith(self):
        string = "How many names have a J as the first letter"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test10_numberStartsWith(self):
        string = "What is the number of names that start with J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test11_numberStartsWith(self):
        string = "What is the number of names that begin with J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test12_numberStartsWith(self):
        string = "What is the number of names that have a J at the front"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test13_numberStartsWith(self):
        string = "What is the number of names that have a J at the beginning"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_1, defined above.
    """
    def test14_numberStartsWith(self):
        string = "What is the number of names whose first letter is J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_1)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_2, defined above.
    """
    def test15_numberStartsWith(self):
        string = "How many names end with J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_2)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_2, defined above.
    """
    def test16_numberStartsWith(self):
        string = "How many names have a J at the end"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_2)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_2, defined above.
    """
    def test17_numberStartsWith(self):
        string = "How many names have a J as the last Letter"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_2)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_2, defined above.
    """
    def test18_numberStartsWith(self):
        string = "What is the number of names that end with J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_2)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_2, defined above.
    """
    def test19_numberStartsWith(self):
        string = "What is the number of names that have a J at the end"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_2)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_2, defined above.
    """
    def test20_numberStartsWith(self):
        string = "What is the number of names whose last letter is J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_2)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_3, defined above.
    """
    def test21_numberStartsWith(self):
        string = "How many names end with J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_2)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_3, defined above.
    """
    def test22_numberStartsWith(self):
        string = "How many names have a J in any position"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_3)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_3, defined above.
    """
    def test23_numberStartsWith(self):
        string = "What is the number of names that contain a J"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_3)

    """
    Test for Kevin Feddema's numberStartsWith method for query5_3, defined above.
    """
    def test24_numberStartsWith(self):
        string = "What is the number of names that have a J in any position"
        t = Tokenize(string)
        self.assertEqual(t.numberStartsWith(t.wordsTagged), self.query5_3)

    """
    Test for Kevin Feddema's numberNullOrNot method for query6_1, defined above.
    """
    def test1_numberNullOrNot(self):
        string = "What is the number of animals with a known specie"
        t = Tokenize(string)
        self.assertEqual(t.numberNullOrNot(t.wordsTagged), self.query6_1)

    """
    Test for Kevin Feddema's numberNullOrNot method for query6_1, defined above.
    """
    def test2_numberNullOrNot(self):
        string = "How many animals have a known specie"
        t = Tokenize(string)
        self.assertEqual(t.numberNullOrNot(t.wordsTagged), self.query6_1)

    """
    Test for Kevin Feddema's numberNullOrNot method for query6_2, defined above.
    """
    def test3_numberNullOrNot(self):
        string = "What is the number of animals with an unknown specie"
        t = Tokenize(string)
        self.assertEqual(t.numberNullOrNot(t.wordsTagged), self.query6_2)

    """
    Test for Kevin Feddema's numberNullOrNot method for query6_2, defined above.
    """
    def test4_numberNullOrNot(self):
        string = "How many animals have an unknown specie"
        t = Tokenize(string)
        self.assertEqual(t.numberNullOrNot(t.wordsTagged), self.query6_2)

    """
    Test for David Osemwegie return_multiple_labels for query2_1, defined above.
    """
    def test1_return_multiple_labels(self):
        string = "Who are all the animals and outlaws"
        t = Tokenize(string)
        self.assertEqual(t.return_multiple_labels(t.wordsTagged), self.query2_1)

    """
    Test for David Osemwegie return_multiple_labels for query2_1, defined above.
    """
    def test2_return_multiple_labels(self):
        string = "Who are the animals, outlaws and persons"
        t = Tokenize(string)
        self.assertEqual(t.return_multiple_labels(t.wordsTagged), self.query2_2)

    """
    Test for David Osemwegie return_multiple_labels for query2_3, defined above.
    """
    def test3_return_multiple_labels(self):
        string = "What are the sizes of each outlaw and person"
        t = Tokenize(string)
        self.assertEqual(t.return_multiple_labels(t.wordsTagged), self.query2_3)

    """
    Test for David Osemwegie return_multiple_labels for query2_4, defined above.
    """
    def test4_return_multiple_labels(self):
        string = "show me the shoe size of the people and outlaws"
        t = Tokenize(string)
        self.assertEqual(t.return_multiple_labels(t.wordsTagged), self.query2_4)

    """
    Test for David Osemwegie return_multiple_labels.
    """
    def test5_return_multiple_labels(self):
        string = "What are the names of the outlaws?"
        t = Tokenize(string)
        self.assertEqual(t.return_multiple_labels(t.wordsTagged), -1)


if __name__ == '__main__':
    unittest.main()