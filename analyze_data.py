"""
This script extracts data from AllPrintings.json file, performs the counting keyword occurences by color identity, and writes the results into a result_data.txt file. Result is the keyword dictionary of counts in the following format {keyword: [# of colorless cards, # of white cards, # of blue cards, # of black cards, # of red cards, # of greenc ards]}.

Notes:
1) Reprints of cards are omitted. This avoids double counting of keywords that occur as result of reprints in subsequent sets.  
2) Key words are identified in the MTGJSON project. Some key words may appear in the rule text but are not necessarily associated with the card.  For example, Oran-Reif Recluse is associated with the keywords, kicker and reach; flying is in the card's rule text but is not a key word associated with the card. 
"""

import json

def ConvertJsonFile():
    # convert json file into data dictionary
    dataFile = open('allprintings.json','r')
    data = json.loads(dataFile.read())
    dataFile.close()
    return data

def mainRun():
    # create and populate a key word dictionary that maintains a count of key word occurences
    data = ConvertJsonFile()
    keyWordSet = set()
    keyWordDict = dict()
    # main analysis
    for magicSet in data['data'].keys():
        for i in range(len(data['data'][magicSet]['cards'])):
            if data['data'][magicSet]['cards'][i]['name'] not in keyWordSet:
                keyWordSet.add(data['data'][magicSet]['cards'][i]['name'])
                # check to make sure keywords and color identity exists. Some Magic sets in the data do not.
                if 'keywords' in data['data'][magicSet]['cards'][i] and 'colorIdentity' in data['data'][magicSet]['cards'][i]:
                    keyWords = data['data'][magicSet]['cards'][i]['keywords']
                    colorIdentity = data['data'][magicSet]['cards'][i]['colorIdentity']
                    counterIncrement = getcounterIncrement(colorIdentity)    
                    for keyWord in keyWords:
                        if keyWord not in keyWordDict:
                            keyWordDict.update({keyWord: [0, 0, 0, 0, 0, 0]})
                        keyWordCount = keyWordDict[keyWord]
                        keyWordDict.update({keyWord : [sum(x) for x in zip(keyWordCount,counterIncrement)]})
    return keyWordDict

def getcounterIncrement(colorIdentity):
    # Gets color increment based on color identity. 
    # colorIdentity is a list of the colors. 
    # counters for counterIncrement are in the following order: colorless, white, blue, black, red, and green
    counterIncrement = [0, 0, 0, 0, 0, 0]
    #defining increments for white, blue, black, red, and green
    WIncrement = [0, 1, 0, 0, 0, 0]
    UIncrement = [0, 0, 1, 0, 0, 0]
    BIncrement = [0, 0, 0, 1, 0, 0]
    RIncrement = [0, 0, 0, 0, 1, 0]
    GIncrement = [0, 0, 0, 0, 0, 1]
    #for colorless cards; if list is empty
    if not colorIdentity:
        counterIncrement = [1, 0, 0, 0, 0, 0]
        return counterIncrement
    #for colored cards
    else:
        if "W" in colorIdentity:
            counterIncrement = [sum(x) for x in zip(WIncrement,counterIncrement)]
        if "U" in colorIdentity:
            counterIncrement = [sum(x) for x in zip(UIncrement,counterIncrement)]            
        if "B" in colorIdentity:
            counterIncrement = [sum(x) for x in zip(BIncrement,counterIncrement)]        
        if "R" in colorIdentity:
            counterIncrement = [sum(x) for x in zip(RIncrement,counterIncrement)]
        if "G" in colorIdentity:
            counterIncrement = [sum(x) for x in zip(GIncrement,counterIncrement)]
        #for mulit-colored cards, counterincrement is weighted by dividing sum of # of colors in colorIdentity. 
        counterIncrement = [x/sum(counterIncrement) for x in counterIncrement]
        return counterIncrement

result = mainRun()
f = open("result_data.txt","w")
f.write(str(result))
f.close()

