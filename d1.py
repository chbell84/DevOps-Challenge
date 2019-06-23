#Author: Charles Bell commit test
#Challenge D1 - Basic Python Skills
#	Create a python script that  reads the titanic data set from Kaggle and performs the following actions
#	Read the file and write it two files, the first reversing the order of the columns, the second creates a file that contains every other columns
#   Create a python script that pulls data from the 'Yahoo Finance API' calling market get movers API and creates a xlsx file that you can open in excel
#	create a python flask server that implements a UI for  #2 and #3
import argparse
import csv
import xlsxwriter

#Reads in CSV file returns an array
def loadcsv(file):
    dataset = []
    with open(file, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
        dataset = [row for row in datareader]
        #dataset = [row[0].split(',') for row in dataset]
        return dataset

def makeDict(list):
    excelDict = {}
    for i in range(len(list[0])):
        excelDict.update({list[0][i] : [list[j+1][i] for j in range(len(list)-1)]})
        print (list[0][i])
    return excelDict

# Saves a excel  version of the list with the columns in reverse order
def reverseSave(filename, data):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    for i in range(len(data)):
        for j in range(len(data[0])):
            worksheet.write(i,len(data[0])-j-1,data[i][j])
    workbook.close()

# Saves a excel version of the list with every other column ommited
def alterSave(filename, data):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    for i in range(len(data)):
        for j in range(len(data[0])/2):
            worksheet.write(i,j,data[i][j*2])
    workbook.close()


testFile = 'train.csv'
data = loadcsv(testFile)
reverseSave('train_reversed.xlsx', data)
alterSave('train_alternate.xlsx', data)
