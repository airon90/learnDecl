# learnDecl
Learn declensions using Wikidata via terminal.

## Requisites
* Python 3
* [SPARQLWrapper](https://rdflib.github.io/sparqlwrapper): ```pip install sparqlwrapper```

## Using
As of now, initial support for some language has been added. You can add the languages manually by changing the code under [line 52](https://github.com/airon90/learnDecl/blob/master/learnDecl.py#L52) with the [Wikidata](https://www.wikidata.org) item of your desired languages. Moreover, hardcoded Italian language is used to display the name of case and name of grammar number. You can change the variable ```LANG```. English language (```en```) is used as fallback one.

## Roadmap
1. Use system language instead of using a variable to define it
2. Make the script translatable
3. Create a website

## Thanks
I want to thank [Luitzen](https://www.wikidata.org/wiki/User:Luitzen) and [Tagishsimon](https://www.wikidata.org/wiki/User:Tagishsimon) for the [query](https://www.wikidata.org/w/index.php?title=Wikidata:Request_a_query&oldid=817351771#Getting_words_and_decletions) used to get the words and declensions
