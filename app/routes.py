import os
import csv
import xlsxwriter
import math
from flask import render_template, send_file, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',  title='Home')

@app.route('/data/')
def return_files(filename='static/files/default.csv'):
    try:
        return send_file(filename)
    except Exception as e:
        return str(e)

#Reads in CSV file returns an array
@app.route('/load-csv')
def load_csv(file='app/static/files/default.csv'):
    dataset = []
    with open(file) as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
        dataset = [row for row in datareader]
    reverse_save(dataset)
    alter_save(dataset)
    return render_template('load-csv.html',  title='Results')

# Saves a excel  version of the list with the columns in reverse order
def reverse_save(data, filename='app/static/files/reversed_columns.xlsx'):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    for i in range(len(data)):
        for j in range(len(data[0])):
            worksheet.write(i,len(data[0])-j-1,data[i][j])
    workbook.close()

# Saves a excel version of the list with every other column ommited
def alter_save(data, filename='app/static/files/alternate_columns.xlsx'):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    for i in range(len(data)):
        for j in range(math.ceil(len(data[0])/2)):
            worksheet.write(i,j,data[i][j*2])
    workbook.close()
