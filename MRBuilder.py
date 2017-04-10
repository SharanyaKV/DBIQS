import nltk

def generateMR():
    nlq = input('Natural language query : ')
    text = nltk.word_tokenize(nlq)
    nlquery = nltk.pos_tag(text)

    #print(nlquery)

    keywords = []
    numerals = []
    tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']

    for i in nlquery:
        if i[1] in tags:
            keywords.append(i[0])
        elif i[1] == 'CD':
            numerals.append(i[0])
    return keywords,text, nlq, numerals
