from app import app
"""Author: Charles Bell
    Challenge D1 - Basic Python Skills
    1   Create a python script that  reads the titanic data set from Kaggle
    and performs the following actions
    2   Read the file and write it two files, the first reversing the order
    of the columns, the second creates a file that contains every other columns
    3   Create a python script that pulls data from the 'Yahoo Finance API' calling
    market get movers API and creates a xlsx file that you can open in excel
    4   create a python flask server that implements a UI for  #2 and #3
    This just imports the app and routs from the app/ directorty and sets up the
    server to run"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
