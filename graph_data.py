# this script takes the result_data.txt file and creates an array of pie charts 

import numpy
import matplotlib.pyplot as plt
import ast
import math

def result_data():
    #reads the txt file and returns the data, ordered by total counts, in this format [(total count, index of dominant color, key word, list of counts by color)]
    f = open('result_data.txt')
    result = ast.literal_eval(f.read())
    f.close()
    list_result =[]
    for key in result.keys():
        list_result.append((sum(result[key]), result[key].index(max(result[key])), key, result[key])) 
    return patterned_sort(list_result)

def patterned_sort(list_result):
    #this is a hack to sort data so that it displays vertically color-wise on the output graph
    list_result.sort(reverse=True)
    def takeSecond(elem):
        return elem[1]
    list_result.sort(key=takeSecond)
    sorted_list_result = []
    for row in range(4): # 4 corresponds with number of rows in graph
        for color_index in range(6): # work through colorless + 5 colors
            counter = 0
            while True:
                if list_result[counter][1] == color_index:
                    sorted_list_result.append(list_result.pop(counter))
                    break
                else:
                    counter += 1
    sorted_list_result.append(list_result) #append remaining data        
    return sorted_list_result

data = result_data()
fig, axes = plt.subplots(figsize=(11, 8), nrows=4, ncols=6)
fig.subplots_adjust(wspace=0.95, hspace=0.30, top=0.90, bottom=0.02)
colors = ['dimgrey', 'whitesmoke', 'mediumblue', 'black', 'tab:red','forestgreen']
    
for ax, (keyWordSum, colorIndex, KeyWordTitle, keyWordData) in zip(axes.flatten(), data):    
    KeyWordTitle += ' ({})'.format(int(math.ceil(keyWordSum)))
    ax.set_title(KeyWordTitle, weight='bold', size='medium', position=(0.5, 1.1),
        horizontalalignment='center', verticalalignment='center')
    ax.pie(keyWordData, colors=colors, 
        shadow=False, startangle=90, counterclock=False)
    ax.axis('equal')

fig.text(0.5, 0.955, 'Most Frequently Used Keywords in Magic by Color \n Keyword(Total Count)',
    horizontalalignment='center', color='black', weight='bold',
    size='large')

plt.show()    