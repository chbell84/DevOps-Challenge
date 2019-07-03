#!/usr/bin/python3.x
"""Author: Charles Bell
    Challenge D1 - Basic Python Skills
    1   Create a python script that  reads the titanic data set from Kaggle
        and performs the following actions
    2   Read the file and write it two files, the first reversing the order
        of the columns, the second creates a file that contains every other columns
    3   Create a python script that pulls data from the 'Yahoo Finance API' calling
        market get movers API and creates a xlsx file that you can open in excel
    4   create a python flask server that implements a UI for  #2 and #3"""

import os
import csv
import math
import urllib
import json
import xlsxwriter
from flask import request, render_template, send_file
from werkzeug.utils import secure_filename
from app import app

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    """Renders the UI for reading files from the Titanic dataset
        or for pulling Historical Market Data from the
        World Trading Data API"""
    if request.method == 'POST':
        file = request.files['file']
        filename = 'input.csv'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return titanic(filename)
    return render_template('index.html', title='Home')

@app.route('/data/')
@app.route('/data/<filename>')
def return_files(filename=None):
    """Delivers static files from the files directory on teh flask instance.
        if no filename is specified, it delivers the 'default.csv' file"""
    if filename is None:
        filepath = os.path.join(app.config['UPLOAD_FOLDER_SF'], 'default.csv')
    else:
        filepath = os.path.join(app.config['UPLOAD_FOLDER_SF'], secure_filename(filename))
    return send_file(filepath)

@app.route('/finance/', methods=['GET', 'POST'])
def finance():
    """Renders the UI for pulling Historical Market Data from the
        World Trading Data API"""
    if request.method == 'POST':
        symbol = request.form['symbol']
        symbol = symbol.upper()
        filename = "market_history.xlsx"
        json_data = stock_history(symbol)
        if 'Message' in json_data:
            return render_template('api_error.html', message=json_data['Message'])
        dataset = parse_stock(json_data['history'])
        excel_save(dataset, os.path.join(app.config['UPLOAD_FOLDER'], filename), symbol)
        return render_template('api_success.html', title=filename, filename=filename)
    return render_template('finance.html', title='Finance API')

def stock_history(symbol):
    """Takes a stock symbols as a sting and pulls the Historical Market
        Data for that symbol from the World Trading Data API and returns
        a dictionary object"""
    api_key = app.config['API_KEY']
    output = 'json'
    url = ("https://api.worldtradingdata.com/api/v1/history?symbol=%s&sort=newest&output=%s&api_token=%s"
           % (symbol, output, api_key))
    page = urllib.request.urlopen(url)
    rawdata = page.read()
    return json.loads(rawdata)

def parse_stock(history):
    """Takes the history attribute from the Historical Market Data API call
        and returns a two-dimensional list"""
    dates = list(history.keys())
    columns = list(history[dates[0]].keys())
    table = [['Date'] + columns]
    for date in dates:
        row = [history[date][key] for key in columns]
        row = [date]+row
        table += [row]
    return table

@app.route('/titanic/')
@app.route('/titanic/<filename>')
def titanic(filename=None):
    """Reads a .csv file from the Titanic dataset saved to the uploads folder
        and creates two excel files. The first saves only every other column.
        The second saves the columns in reverse order"""
    if filename is None:
        source_file = os.path.join(app.config['UPLOAD_FOLDER'], 'default.csv')
    else:
        source_file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    alter_file = os.path.join(app.config['UPLOAD_FOLDER'], 'alternate_columns.xlsx')
    reverse_file = os.path.join(app.config['UPLOAD_FOLDER'], 'reversed_columns.xlsx')
    dataset = load_csv(source_file)
    excel_save(reverse_columns(dataset), reverse_file, 'Titanic')
    excel_save(alternate_columns(dataset), alter_file, 'Titanic')
    return render_template('titanic.html', title='Titanic Dataset')

def load_csv(file):
    """loads a csv file specifiled in the file parameter and returns the data as a list"""
    dataset = []
    with open(file) as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
        dataset = [row for row in datareader]
    return dataset

def reverse_columns(data):
    """Takes a two-dimensional list as a parameter and returns a list
        with the columns in inverted order"""
    new_data = []
    for row in data:
        new_row = [row[len(row)-j-1] for j in range(len(row))]
        new_data += [new_row]
    return new_data

def alternate_columns(data):
    """Takes a two-dimensional list as a parameter and returns a list with
        every other column removed"""
    new_data = []
    for row in data:
        new_row = [row[j*2] for j in range(math.ceil(len(row)/2))]
        new_data += [new_row]
    return new_data

def excel_save(data, file, name):
    """Takes a list, a file path sting and a name sting. The list is saved
        as an excel file a the location defined by the second parameter.
        The third parameter names the sheet of the workbook."""
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet(name)
    for i in range(len(data)):
        for j in range(len(data[0])):
            worksheet.write(i, j, data[i][j])
    workbook.close()
