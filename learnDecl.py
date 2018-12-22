#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from SPARQLWrapper import SPARQLWrapper, JSON


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


LANG = "it"
TARGET = "Q1412"

points = [0, 0, 0]

loop = True

query = """SELECT ?lemma ?representation ?numberLabel ?caseLabel {
    ?lexeme <http://purl.org/dc/terms/language> wd:""" + TARGET + """.
    ?lexeme wikibase:lemma ?lemma .
    ?lexeme ontolex:lexicalForm ?form .
    ?form ontolex:representation ?representation .
    ?form wikibase:grammaticalFeature ?number, ?case .
    ?number wdt:P31 wd:Q104083 .
    ?case wdt:P31 wd:Q128234 .
    SERVICE wikibase:label {
        bd:serviceParam wikibase:language \"""" + LANG + """, en"
    }
} order by ?lexeme"""

endpoint_url = "https://query.wikidata.org/sparql"
data = get_results(endpoint_url, query)

lemmas = []
for n in range(len(data["results"]["bindings"])):
    lemma = data["results"]["bindings"][n]
    lemmas.append([lemma["lemma"]["value"],
        lemma["caseLabel"]["value"],
        lemma["numberLabel"]["value"],
        lemma["representation"]["value"]
    ])

while loop:
    n = random.randint(0, len(lemmas) - 1)
    word = []
    for i in range(len(lemmas)):
    	if (lemmas[i][0] == lemmas[n][0] and lemmas[i][1] == lemmas[n][1]
    	    and lemmas[i][2] == lemmas[n][2]):
    	    word.append(lemmas[i][3])
    answer = input(lemmas[n][0] + " ("
                   + lemmas[n][1] + ", " + lemmas[n][2] + "): ")
    if (answer in word):
        print("Right!")
        if (len(word) > 1):
        	print("All valid answers are: ")
        	for i in range(len(word)):
        		print(word[i])
        points[0] += 1
    elif (answer == ""):
        print("Valid answers were: ")
        for i in range(len(word)):
	        print(word[i])
        points[1] += 1
    elif (answer == "exit"):
        print("Number of right answers: " + str(points[0]))
        print("Number of empty answers: " + str(points[1]))
        print("Number of wrong answers: " + str(points[2]))
        print("Goodbye!")
        loop = False
    else:
        points[2] += 1
        print("Wrong! Valid answers were: ")
        for i in range(len(word)):
	        print(word[i])
