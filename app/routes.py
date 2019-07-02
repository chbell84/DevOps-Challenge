import os
import csv
import xlsxwriter
import math
import urllib
import json
from flask import Flask, request, render_template, send_file
from app import app
from werkzeug.utils import secure_filename

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index')
def index():
    if request.method == 'POST':
        file = request.files['file']
        filename = 'input.csv'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)
        return titanic(filename)
    return render_template('index.html',  title='Home')

@app.route('/data/')
@app.route('/data/<filename>')
def return_files(filename=None):
    if filename is None:
        filepath = os.path.join(app.config['UPLOAD_FOLDER_SF'],'default.csv')
    else:
        filepath = os.path.join(app.config['UPLOAD_FOLDER_SF'],secure_filename(filename))
    try:
        return send_file(filepath)
    except Exception as e:
        return str(e)

@app.route('/finance/', methods = ['GET', 'POST'])
def finance():
    if request.method == 'POST':
        symbol = request.form['symbol']
        symbol = symbol.upper()
        filename = "market_history.xlsx"
        json_data = stock_history(symbol)
        if 'Message' in json_data:
            return render_template('api_error.html', message=json_data['Message'])
        dataset = parse_stock(json_data['history'])
        excel_save(dataset, os.path.join(app.config['UPLOAD_FOLDER'],filename), symbol)
        return render_template('api_success.html', title=filename, filename=filename)
    return render_template('finance.html',  title='Finance API')

def stock_history(symbol):
    api_key = app.config['API_KEY']
    output = 'json'
    url = ("https://api.worldtradingdata.com/api/v1/history?symbol=%s&sort=newest&output=%s&api_token=%s" % (symbol,output,api_key))
    page = urllib.request.urlopen(url)
    rawdata = page.read()
    return(json.loads(rawdata))

def parse_stock(history):
    dates = list(history.keys())
    columns = list(history[dates[0]].keys())
    table = [['Date'] + columns]
    for date in dates:
        row = [history[date][key] for key in columns]
        row = [date]+row
        table += [row]
    return table

# By default, this reads in the default.csv file saved to the uploads folder. Otherwise, it reads the csv file uploaded by the user and defined by the filename paramater. The resulting data is sent to the reverse_save and alter_save functions to create excel files.
@app.route('/titanic/')
@app.route('/titanic/<filename>')
def titanic(filename=None):
    if filename is None:
        source_file = os.path.join(app.config['UPLOAD_FOLDER'],'default.csv')
    else:
        source_file = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(filename))
    alter_file=os.path.join(app.config['UPLOAD_FOLDER'],'alternate_columns.xlsx')
    reverse_file=os.path.join(app.config['UPLOAD_FOLDER'],'reversed_columns.xlsx')
    dataset = load_csv(source_file)
    excel_save(reverse_columns(dataset), reverse_file, 'Titanic')
    excel_save(alternate_columns(dataset), alter_file, 'Titanic')
    return render_template('titanic.html',  title='Titanic Dataset')

# loads a csv file specifiled in the file parameter and returns the data as a list
def load_csv(file):
    dataset = []
    with open(file) as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
        dataset = [row for row in datareader]
    return dataset

# Saves an excel version of the list with the columns in reverse order
def reverse_columns(data):
    new_data = []
    for row in data:
        new_row = [row[len(row)-j-1] for j in range(len(row))]
        new_data += [new_row]
    return(new_data)

# Saves an excel version of the list with every other column ommited
def alternate_columns(data):
    new_data = []
    for row in data:
        new_row = [row[j*2] for j in range(math.ceil(len(row)/2))]
        new_data += [new_row]
    return(new_data)

def excel_save(data, file, name):
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet(name)
    for i in range(len(data)):
        for j in range(len(data[0])):
            worksheet.write(i,j,data[i][j])
    workbook.close()

