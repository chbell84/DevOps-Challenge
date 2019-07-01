import os
import csv
import xlsxwriter
import math
from flask import Flask, request, render_template, send_file
from app import app
from werkzeug.utils import secure_filename

#DEFAULT_FILE = os.path.join(app.config['UPLOAD_FOLDER_SF'],'default.csv')

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index')
def index():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)
        return load_csv(filename)
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

#Reads in CSV file returns an array
@app.route('/load-csv/')
@app.route('/load-csv/<filename>')
def load_csv(filename=None):
    if filename is None:
        file = os.path.join(app.config['UPLOAD_FOLDER'],'default.csv')
    else:
        file = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(filename))
    dataset = []
    with open(file) as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
        dataset = [row for row in datareader]
    reverse_save(dataset)
    alter_save(dataset)
    return render_template('load-csv.html',  title='File Downloads')

# Saves a excel  version of the list with the columns in reverse order
def reverse_save(data, file=os.path.join(app.config['UPLOAD_FOLDER'],'reversed_columns.xlsx')):
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    for i in range(len(data)):
        for j in range(len(data[0])):
            worksheet.write(i,len(data[0])-j-1,data[i][j])
    workbook.close()

# Saves a excel version of the list with every other column ommited
def alter_save(data, file=os.path.join(app.config['UPLOAD_FOLDER'],'alternate_columns.xlsx')):
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    for i in range(len(data)):
        for j in range(math.ceil(len(data[0])/2)):
            worksheet.write(i,j,data[i][j*2])
    workbook.close()
