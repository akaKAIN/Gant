#!/usr/bin/env python
# coding: utf-8

# ### Для корректного отодражения диаграмм, следующие скрипты должны быть добавлены в тег head html-документа

# In[ ]:


#<script src="https://cdn.pydata.org/bokeh/release/bokeh-1.2.0.min.js" type="text/javascript"></script>
    


# In[ ]:


import datetime
import pandas as pd
from itertools import groupby
from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.models import ColumnDataSource, Range1d
from bs4 import BeautifulSoup
import time


# In[ ]:


process_list = [
    ['breakfast',
     datetime.datetime(2019, 6, 1, 7, 15),
     datetime.datetime(2019, 6, 1, 7, 55)
    ],
    ['walking',
     datetime.datetime(2019, 6, 1, 8, 15),
     datetime.datetime(2019, 6, 1, 10, 55)
    ],
    ['sleeping',
     datetime.datetime(2019, 6, 1, 11, 15),
     datetime.datetime(2019, 6, 1, 12, 55)
    ],
    ['Hotel_Boot',
     datetime.datetime(2019, 6, 1, 20, 50),
     datetime.datetime(2019, 6, 5, 12, 0)
    ],
    ['dinner',
     datetime.datetime(2019, 6, 1, 13, 15),
     datetime.datetime(2019, 6, 1, 14, 55)
    ],
    ['breakfast',
     datetime.datetime(2019, 6, 2, 7, 15),
     datetime.datetime(2019, 6, 2, 7, 55)
    ],
    ['dinner',
     datetime.datetime(2019, 6, 2, 13, 15),
     datetime.datetime(2019, 6, 2, 14, 55)
    ],
    ['breakfast',
     datetime.datetime(2019, 6, 3, 7, 15),
     datetime.datetime(2019, 6, 3, 7, 55)
    ],
    ['dinner',
     datetime.datetime(2019, 6, 3, 13, 15),
     datetime.datetime(2019, 6, 3, 14, 55)
    ],
    ['walk_ex',
     datetime.datetime(2019, 6, 2, 15, 15),
     datetime.datetime(2019, 6, 2, 19, 0)
    ],
    ['a_photo_session',
     datetime.datetime(2019, 6, 3, 9, 30),
     datetime.datetime(2019, 6, 3, 12, 0)
    ],
    ['wine_museum',
     datetime.datetime(2019, 6, 3, 16, 0),
     datetime.datetime(2019, 6, 5, 10, 30)]
]


# In[ ]:





# In[ ]:


def unpack_lists(lists_in_list: list) -> list:
    unpacked_list = []
    for elem in lists_in_list:
        if type(elem[0]) is str:
            unpacked_list.append(elem)
        else:
            unpacked_list.extend(elem)
    return unpacked_list 


def partition_proc(event: list) -> list:
    delta = event[2].day - event[1].day
    if delta > 0:
        point = event[1]
        temp_list = []
        time_end = datetime.time(23, 59)

        for i in range(delta):
# Добавление индекса разбирым по суткам процессам
#             temp_list.append([
#                 (event[0] + '_' + str(i+1)),
#                 point,
#                 datetime.datetime.combine(point.date(), time_end)])
            temp_list.append([
                event[0],
                point,
                datetime.datetime.combine(point.date(), time_end)])
    
            point = datetime.datetime.combine(
                point.date(), time_end
            ) + datetime.timedelta(minutes=1)
# Добавление индекса разбирым по суткам процессам
#         temp_list.append([(event[0] + '_' + str(i+2)), point, event[2]])
        temp_list.append([event[0], point, event[2]])
    
        return temp_list
    return event


def main(process_list: list) -> list:
    for index, value in enumerate(process_list):
        process_list[index] = partition_proc(value)
    process_list = unpack_lists(process_list)
    return sorted(process_list, key=lambda x: x[1])


# In[ ]:


def diagram_drow_in_file(day_proc: list):
    # Рисует диаграмму Ганта и сохраняет ее в файл
    
    DF=pd.DataFrame(columns=['Process','Start','End'])
    diagram_title = str(day_proc[0][1].date().strftime('%d.%m.%Y'))
    for i, data in enumerate(day_proc[::-1]):
        DF.loc[i] = data
    G=figure(
        title=diagram_title,
        x_axis_type='datetime',
        width=350,
        height=150,
        y_range=DF.Process.tolist(),
        x_range=Range1d(
            DF.Start.min() - datetime.timedelta(hours=1),
            DF.End.max() + datetime.timedelta(hours=1))
    )
    DF['ID']=DF.index+0.75
    DF['ID1']=DF.index+0.25
    CDS=ColumnDataSource(DF)
    G.quad(
        left='Start',
        right='End',
        bottom='ID',
        top='ID1',
        source=CDS,
        line_width=3)
    output_file(url)
    show(G)


def parsing_file():
    with open(url) as html:
        diagram = {}
        soup = BeautifulSoup(html)
#         diagram['head'] = str(soup.head.contents[7]) + str(soup.head.contents[9])
        diagram['body'] = str(soup.body.find_all(['div', 'script']))[1:-1]
    return diagram


# In[ ]:





# ### Запуск тела программы

# In[ ]:


if __name__ == '__main__':
    
    url = '/home/kain/gant1.html'
    diagrams_list = []
    correct_process_list = main(process_list)
    correct_process_list = [
        list(elem) for _, elem in groupby(correct_process_list, lambda x: x[1].day)
    ]
    
#     Проверка вывода процессов
#     for i in correct_process_list:
#         for k in i:
#             print(k)
    
    for day_proc in correct_process_list:
        diagram_drow_in_file(day_proc)
        time.sleep(0.5)
        diagram = parsing_file()
        diagrams_list.append(diagram)


# In[ ]:


#diagrams_list


# In[ ]:





# In[ ]:





# #### Просмотр результатов вывода в файле (можно кидать в html-документ)

# In[ ]:


#with open('result_parse.txt', 'w') as file:
##     file.write('<HEAD>:\n', diagrams_list[0]['head'], '\n</HEAD>')
#    for i in range(len(diagrams_list)):
#        file.write(diagrams_list[i]['body'])


# In[ ]:





# In[ ]:




