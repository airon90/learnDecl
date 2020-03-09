#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import random
import unicodedata
from SPARQLWrapper import SPARQLWrapper, JSON


def strip_accents(word):    # TODO: buggy
    return ''.join(w for w in unicodedata.normalize('NFD', word)
                   if unicodedata.category(w) != 'Mn')

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def generate_lemmas(TARGET, LANG):
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
        lemmas.append({
            "lemma": lemma["lemma"]["value"],
            "case": lemma["caseLabel"]["value"],
            "number": lemma["numberLabel"]["value"],
            "repr": lemma["representation"]["value"]
        })
        
    return lemmas

LANG = "it"

loopLang = True
while(loopLang):
    loopLang = False
    targlang = input("Language code: ")

    if (targlang == "de"):
        TARGET = "Q188"
    elif (targlang == "et"):
        TARGET = "Q9072"
    elif (targlang == "fi"):
        TARGET = "Q1412"
    elif (targlang == "la"):
        TARGET = "Q397"
    elif (targlang == "ru"):
        TARGET = "Q7737"
    elif (targlang == "sv"):
        TARGET = "Q9027"
    else:
        print("Code not recognized")
        loopLang = True

points = [0, 0, 0]

loopGame = True
loopMenu = True

cols = ["lemma", "case", "number", "repr"]

while loopMenu:
    menu = input("1. Play\n2. Update words\nChoose: ")
    if menu == "1":
        lemmas = []
        csvfile = TARGET + ".csv"
        with open(csvfile, "r") as output:
            reader = csv.DictReader(output, fieldnames=cols)
            for word in reader:
                if TARGET == "la":
                    lemmas.append({
                        "lemma": word[cols[0]],
                        "case": word[cols[1]],
                        "number": word[cols[2]],
                        "repr": strip_accents(word[cols[3]])
                    })
                else:
                    lemmas.append({
                        "lemma": word[cols[0]],
                        "case": word[cols[1]],
                        "number": word[cols[2]],
                        "repr": word[cols[3]]
                    })
        
        word = []
        for n in range(len(lemmas)):
            if lemmas[n][cols[0]] not in word:
                word.append(lemmas[n][cols[0]])
        print("Numero di lemmi: " + str(len(word)))
        print("Numero di parole: " + str(len(lemmas)))

        while loopGame:
            n = random.randint(0, len(lemmas) - 1)
            word = []
            for i in range(len(lemmas)):
                if (lemmas[i][cols[0]] == lemmas[n][cols[0]]
                    and lemmas[i][cols[1]] == lemmas[n][cols[1]]
                    and lemmas[i][cols[2]] == lemmas[n][cols[2]]):
                    word.append(lemmas[i][cols[3]]) 

            answer = input(lemmas[n][cols[0]] + " ("
                       + lemmas[n][cols[1]] + ", " + lemmas[n][cols[2]] + "): ")
            if (answer in word):
                print("Giusto!")
                if (len(word) > 1):
                    print("Le risposte valide erano: ")
                    for i in range(len(word)):
                        print(word[i])
                points[0] += 1
            elif (answer == ""):
                print("Le risposte valide erano: ")
                for i in range(len(word)):
                    print(word[i])
                points[1] += 1
            elif (answer == "exit"):
                print("Numero di parole indovinate: " + str(points[0]))
                print("Numero di parole lasciate in bianco: " + str(points[1]))
                print("Numero di parole sbagliate: " + str(points[2]))
                print("Addio!")
                loopGame = False
                loopMenu = False
            else:
                points[2] += 1
                print("Sbagliato! Le risposte valide erano: ")
                for i in range(len(word)):
                    print(word[i])

    elif menu == "2":    
        lemmas = generate_lemmas(TARGET, LANG)
        csvfile = TARGET + ".csv"
        with open(csvfile, 'w') as output:
            writer = csv.DictWriter(output, fieldnames=cols)
            for data in lemmas:
                writer.writerow(data)
        
            
    elif menu == "3":
        print("Goodbye!")
        loopMenu = False
        
    else:
        print("Wrong choice")
