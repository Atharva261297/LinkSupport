from django.shortcuts import render
from django.http import HttpResponse
import csv

def index(request):
    # lpm_df = pandas.read_csv('lpm.csv')
    # colpm_df = pandas.read_csv('colpm.csv')
    lpm_reader = csv.reader(open('lpm.csv', encoding='UTF-8'))
    lpm_out = [row for row in lpm_reader]

    colpm_reader = csv.reader(open('colpm.csv', encoding='UTF-8'))
    colpm_out = [row for row in colpm_reader]

    lpm_names_reader = csv.reader(open('lpm-names.csv', encoding='UTF-8'))
    lpm_names_out = [row for row in lpm_names_reader]

    colpm_names_reader = csv.reader(open('colpm-names.csv', encoding='UTF-8'))
    colpm_names_out = [row for row in colpm_names_reader]
    # lpm_df.r

    # print(colpm_out)

    return render(request, 'data-index.html', {'lpm_data' : lpm_out, 'colpm_data' : colpm_out, 'lpm_names_data' : lpm_names_out, 'colpm_names_data' : colpm_names_out})
