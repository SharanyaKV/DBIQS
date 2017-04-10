import sqlite3
import itertools
from nltk.corpus import stopwords
from SemanticBuilder import BuildSemanticMap
from MRBuilder import generateMR

#Checking substring similarity between 2 strings
def issimilar(s1, s2):
    if s1.lower() in s2.lower() or s2.lower() in s1.lower():
        return True
    return False


#Code Genration Function
def generateCode(database):
    keywords, text, nlq, numerals = generateMR()
    schema = BuildSemanticMap(database)
    table = []
    attr = []
    cond = []
    special = []
    #Special words and Table, attribute selection
    for word in keywords:
        identified = False
        outlier= ['select', 'list', 'show', 'out','name', 'number']
        if word.lower() not in outlier:
            for tname in schema:
                if issimilar(word, tname):
                    table.append(tname)
                    identified = True
                for attname in schema[tname]:
                    if issimilar(word, attname):
                        attr.append(tname + '.' + attname)
                        table.append(tname)
                        identified = True
            if not identified:
                special.append(word)

    table = list(set(table))
    attr = list(set(attr))
    #Relational operator
    relatn_op = {'greater than' : '>', 'more than' : '>', 'less than':'<'}
    numlist = {}
    num_op = {}


    for num in numerals:
        numindex = text.index(num)
        temp = ' '.join([text[numindex-2], text[numindex-1]]).lower()
        temp = temp.strip(' ')
        if temp in relatn_op:
            num_op[num]= relatn_op[temp]

        else:
            num_op[num] = '='


        for i in range(1, 5):
            identified = False

            if numindex - i > -1:
                prev = text[numindex - i]
                if prev in keywords and prev not in special:
                    if num in numlist:
                        numlist[num].append(prev)
                    else:
                        numlist[num] = [prev]
                    identified = True

            if identified:
                break
    #print(numlist)

    for num in numlist:
        for tname in schema:
            for attname in schema[tname]:
                if issimilar(numlist[num][0], attname):
                    cond.append(tname + '.' + attname + num_op[num] + num)
                    #print("Relational Operator Condition : ", tname + '.' + attname + num_op[num] + num)

    stopw = ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'preposition', 'conjunction', 'interjection', 'article',
             'list', 'show'] + stopwords.words('english')

    #print("Selected tables : ", table)
    #print("Selected attributes : ", attr)
    #print("*"*50)
    attlist = ', '.join(attr)
    tablelist = ', '.join(table)


    #Join condition Generation

    if len(table)>1:
        for tablepairs in itertools.combinations(table, 2):
            for attribute in schema[tablepairs[0]]:
                if attribute in schema[tablepairs[1]]:
                    cond.append(tablepairs[0] + '.' + attribute + '=' + tablepairs[1] + '.' + attribute)
                    #print("Join Condition : ", tablepairs[0] + '.' + attribute + '=' + tablepairs[1] + '.' + attribute)

    if attlist == '':
        attlist = '*'
    #Special word processing
    condlist = {}
    for item in special:
        if item.lower() not in stopw:
            itemindex = text.index(item)
            for i in range(0, 3):
                identified = False
                if itemindex - i > -1:
                    prev = text[itemindex - i]
                    if prev in keywords and prev not in special:
                        if item in condlist:
                            condlist[item].append(prev)
                        else:
                            condlist[item] = [prev]
                        identified = True

                if itemindex + i < len(text):
                    next = text[itemindex + i]
                    if next in keywords and next not in special:
                        if item in condlist:
                            condlist[item].append(next)
                        else:
                            condlist[item] = [next]
                        identified = True
                if identified:
                    break

    #print("condlist :" +condlist)
    #Equality condition checking
    for item in condlist:
        for tname in schema:
            for attname in schema[tname]:
                if issimilar(condlist[item][0], attname):
                    cond.append(tname + '.' + attname + " = '" + item + "'")
                    #print("Equality Condition : "+tname + '.' + attname + " = '" + item + "'")

    condstr = ' and '.join(cond)
    #print()
    #print("*" * 50)
    print("*" * 50)


    if condstr != '':
        sqlquery = 'SELECT ' + attlist + ' FROM ' + tablelist + ' WHERE ' + condstr + '; '
    else:
        sqlquery = 'SELECT ' + attlist + ' FROM ' + tablelist + '; '
    print( "Query : "+ sqlquery)
    print()

    proceed = input('Proceed? (Y/N) : ')
    if proceed == 'Y' or proceed == 'y':
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        data = cursor.execute(sqlquery)
        for tuple in data:
            print(tuple)
