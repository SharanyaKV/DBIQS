import sqlite3

def BuildSemanticMap(database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    query = '''select sql from sqlite_master where type = 'table';'''
    data = cursor.execute(query)

    schema={}

    for tuple in data:
        #print(tuple)
        for creatnQuery in tuple:
            #print(creatnQuery)
            junk=['\n','\t','"',"'"]

            wordlist = creatnQuery.split(' ')

            schema[wordlist[2]]= []
            creatnQuery = ' '.join(wordlist[3:])
            creatnQuery= creatnQuery[1:-1]
            attrlist = creatnQuery.split(', ')
            for attr in attrlist:
                attr = attr.split(' ')
                for i in junk:
                    if i in attr[0]:
                        attr[0].replace(i,"")
                schema[wordlist[2]].append(attr[0])
    #print("Scheme : " ,schema)
    return schema

#BuildSemanticMap('data/collegesystem.db')

