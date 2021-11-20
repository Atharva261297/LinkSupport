
from django.shortcuts import render
from django.http import HttpResponse
import csv
import numpy as np
from datetime import date
from pprint import pp, pprint
from django import forms
import re

start_date = date(2021, 11, 8)
pattern1 = "^[0-9]*/Sp[0-9]*"
pattern2 = "^Sp[0-9]*/[0-9]*"

def addIndices(names_array) :
    new_array = []
    for i in range(len(names_array)) :
        new_array.append(names_array[i][0] + ' (' + str(i+1) + ')')
    return new_array

def getLpm(diff):
    lpm_names_reader = csv.reader(open('lpm-names.csv', encoding='UTF-8'))
    lpm_names_out = [row for row in lpm_names_reader]

    lpm_current_names = np.roll(lpm_names_out, diff[0])
    numbered_lpm_names = addIndices(lpm_current_names)

    lpm_reader = csv.reader(open('lpm.csv', encoding='UTF-8'))
    lpm_out = [row for row in lpm_reader]
    
    lpm_day_with_names = []

    for i in range(len(lpm_names_out)):
        lpm_day_with_names.append({'name': numbered_lpm_names[i].replace(" ", ""), 'link' : lpm_out[i][diff[1]].replace(" ", "")})

    return lpm_day_with_names

def getCoLpm(diff):
    colpm_names_reader = csv.reader(open('colpm-names.csv', encoding='UTF-8'))
    colpm_names_out = [row for row in colpm_names_reader]

    colpm_current_names = np.roll(colpm_names_out, diff[0])
    numbered_colpm_names = addIndices(colpm_current_names)

    colpm_reader = csv.reader(open('colpm.csv', encoding='UTF-8'))
    colpm_out = [row for row in colpm_reader]
    
    colpm_day_with_names = []

    for i in range(len(colpm_names_out)):
        colpm_day_with_names.append({'name': numbered_colpm_names[i].replace(" ", ""), 'link' : colpm_out[i][diff[1]].replace(" ", "")})

    return colpm_day_with_names

def find(links, link_to_find):
    for l in links:
        if l['link'].lower() == link_to_find.lower() :
            return l
    return None

def findPartial(links, link_to_find, type: int):
    actual_link = link_to_find.split("/")[type]
    for l in links:
        if "/" in l['link']:
            if l['link'].split("/")[type].lower() == actual_link.lower() :
                return l
    return None

def join(lpm_link, colpm_link):
    joined_link = []
    rest_drivers_lpm = []
    rest_drivers_colpm = []
    none_link = []

    for lpm in lpm_link:
        if lpm['link'].lower() == 'REST'.lower():
            rest_drivers_lpm.append(lpm['name'])

    for colpm in colpm_link:
        if colpm['link'].lower() == 'REST'.lower():
            rest_drivers_colpm.append(colpm['name'])


    for lpm in lpm_link :
        if lpm['link'] != 'REST':
            colpm = find(colpm_link, lpm['link'])
            if colpm != None :
                joined_link.append({'link': lpm['link'], 'lpm': lpm['name'], 'colpm': colpm['name']})
            elif re.match(pattern1, lpm['link']) :
                colpm = findPartial(colpm_link, lpm['link'], 0)
                if colpm != None :
                    joined_link.append({'link': lpm['link'] + ' with ' + colpm['link'], 'lpm': lpm['name'], 'colpm': colpm['name']})
            elif re.match(pattern2, lpm['link']) :
                colpm = findPartial(colpm_link, lpm['link'], 1)
                if colpm != None :
                    joined_link.append({'link': lpm['link'] + ' with ' + colpm['link'], 'lpm': lpm['name'], 'colpm': colpm['name']})
            else :
                none_link.append(lpm)

            
    return (joined_link, rest_drivers_lpm, rest_drivers_colpm, none_link)

def index(request):
    joined_links = [[],[],[], []]
    req_view_date = request.GET.get('view_date', '')
    if req_view_date != '' :
        split_date = req_view_date.split("-")
        view_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
        # pprint(start_date)
        # pprint(view_date)
        # pprint(form.data.get('view_datex'))
        # view_date = date(2021, 11, 29)
        diff_days = (view_date - start_date).days
        diff = divmod(diff_days, 7)

        lpm_link = getLpm(diff)
        colpm_link = getCoLpm(diff)

        joined_links = join(lpm_link, colpm_link)

        # pprint(lpm_link)
        # pprint(colpm_link)
    # else:
    #     form = DateForm()
    # view_data = datetime.datetime(2021, 11, 20)
    # print(view_data - start_data)
    # lpm_df = pandas.read_csv('lpm.csv')
    # colpm_df = pandas.read_csv('colpm.csv')
    # lpm_reader = csv.reader(open('lpm.csv', encoding='UTF-8'))
    # lpm_out = [row for row in lpm_reader]

    # colpm_reader = csv.reader(open('colpm.csv', encoding='UTF-8'))
    # colpm_out = [row for row in colpm_reader]

    # lpm_names_reader = csv.reader(open('lpm-names.csv', encoding='UTF-8'))
    # lpm_names_out = [row for row in lpm_names_reader]

    # colpm_names_reader = csv.reader(open('colpm-names.csv', encoding='UTF-8'))
    # colpm_names_out = [row for row in colpm_names_reader]
    # lpm_df.r

    # print(colpm_out)

    return render(request, 'find-index.html', {'data': joined_links[0], 'rest_data_lpm': joined_links[1], 'rest_data_colpm': joined_links[2], 'error_data': joined_links[3]})

# def findLinks(request):
#     pprint(start_date)
#     pprint(request)
#     # view_date = date(2021, 11, 29)
#     # diff_days = (view_date - start_date).days
#     # diff = divmod(diff_days, 7)

#     # lpm_link = getLpm(diff)
#     # colpm_link = getCoLpm(diff)

#     # joined_links = join(lpm_link, colpm_link)

#     # pprint(lpm_link)
#     # pprint(colpm_link)

#     pprint(joined_links)
class DateForm(forms.Form):
    view_date = forms.DateField(label='Date to find schedule')