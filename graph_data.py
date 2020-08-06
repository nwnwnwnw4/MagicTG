# this script takes the result_data.txt file and creates an array of radar charts 

import numpy
import matplotlib.pyplot as plt
import ast

def result_data():
    f = open('result_data.txt')
    result = ast.literal_eval(f.read())
    f.close()
    list_result =[]

    for key in result.keys():
        list_result.append((sum(result[key]), key, result[key])) 
    list_result.sort(reverse=True)

    return list_result[:]

data = result_data()
fig, axes = plt.subplots(figsize=(11, 8), nrows=4, ncols=5)
fig.subplots_adjust(wspace=0.95, hspace=0.30, top=0.90, bottom=0.02)
colors = ['dimgrey', 'whitesmoke', 'mediumblue', 'black', 'tab:red','forestgreen']
    
for ax, (keyWordSum, KeyWordTitle, keyWordData) in zip(axes.flatten(), data):    
    KeyWordTitle += ' ({})'.format(int(keyWordSum))
    ax.set_title(KeyWordTitle, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        
    def actualValues(val):
        value  = int(numpy.round(val/100.*keyWordSum, 0))
        return value

    ax.pie(keyWordData, colors=colors, 
    shadow=False, startangle=90, counterclock=False)
    ax.axis('equal')

fig.text(0.5, 0.965, 'Most Frequently Used Keywords in Magic (Total Count Excluding Reprints)',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

plt.show()    