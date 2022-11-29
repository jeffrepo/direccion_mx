# Convert .csv to .xml
# Christian J. Gibbs - 05/10/2015
# The first row of the .csv file must be headers
import os, os.path
import glob
import shutil
import csv
import datetime
now = datetime.datetime.now()

# Check for files in /raw folder
files = glob.glob("raw/res.country.state.ciudad.csv")
file_count = len(files)
dir = "raw/"

def ConvertToXML():
    for i in range(len(files)):

        # Take input.csv and set the file output to have a unique name
        csvFile = files[i]
        xmlFile = 'res_country_state_ciudad.xml'

        # Remove directorry
        file = csvFile.strip(dir)

        # Open the csv file to read
        csvData = csv.reader(open(csvFile),delimiter=',',quotechar='"')

        # Open xml file created earlier and write a header
        xmlData = open(xmlFile, 'w')
        xmlData.write('<?xml version="1.0" encoding="ISO-8859-1" ?>' + "\n")
        xmlData.write('<odoo>' + "\n")
        xmlData.write("\t"+'<data noupdate="1">' + "\n")

        for row in csvData:
                print(row)
                xmlData.write("\t\t"+'<record id ="' +row[0]+'" model="res.country.state.ciudad" forcecreate="0">\n')
                xmlData.write("\t\t\t"+'<field name="name">' + row[1]+"</field>\n")
                xmlData.write("\t\t\t"+'<field name="state_id" ref="'+row[2]+'"/>'+"\n")
                xmlData.write("\t\t"+'</record>' + "\n")

        xmlData.write("\t"+'</data>' + "\n")
        xmlData.write('</odoo>' + "\n")

        xmlData.close()

ConvertToXML()
