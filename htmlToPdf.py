import mysql.connector
import argparse
from datetime import date
import os
import sys
from pyhtml2pdf import converter


"""
Installeren mysql database:
https://dev.mysql.com/downloads/file/?id=523159

Installeren mysql-connector-python en pyhtml2pdf:
	pip install mysql-connector-python
	pip install pyhtml2pdf


Aan te roepen met "python htmlToPdf.py -id 1"

Simpel voorbeeld om uit te zoeken of dit werkt op deze manier, kan nog genoeg aangepast worden.
"""


# Simpele args setup. 
parser = argparse.ArgumentParser(description="Just an example", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-id", "--factuurId", help="Factuur id")                                 
args = vars(parser.parse_args())
                        

def setup_database():
	# Creating connection object
	mydb = mysql.connector.connect(
		host = "localhost",
		user = "username",
		password = "password"
	)
	print(mydb)
	
	cursor = mydb.cursor()
	cursor.execute("CREATE DATABASE peroFactuur")
	
	cursor.execute("SHOW DATABASES")
	
	for x in cursor:
		print(x)
	
	
	# Open database
	mydb = mysql.connector.connect(
		host = "localhost",
		user = "username",
		password = "password",
		database="peroFactuur"
	)
	cursor = mydb.cursor()
	# Create testset
	cursor.execute("CREATE TABLE testset (id MEDIUMINT NOT NULL AUTO_INCREMENT, bedrijfsnaam VARCHAR(255), uurtarief INTEGER, teBetalen INTEGER, PRIMARY KEY (id))")
	
	cursor.execute("INSERT INTO testset (id,bedrijfsnaam,uurtarief,teBetalen) VALUES(0,'bedrijf1',20,200);")
	cursor.execute("INSERT INTO testset (id,bedrijfsnaam,uurtarief,teBetalen) VALUES(NULL,'bedrijf2',20,250);")
	cursor.execute("INSERT INTO testset (id,bedrijfsnaam,uurtarief,teBetalen) VALUES(NULL,'bedrijf3',20,1500);")
	mydb.commit()
	
	cursor.execute("SELECT * FROM testset;")
	
	for x in cursor:
	  print(x)
	
def connectToDb():
	print("Connecting to db")
	
	# Creating connection object
	global mydb
	mydb = mysql.connector.connect(
		host = "localhost",
		user = "username",
		password = "password",
		database="peroFactuur"
	)

	cursor = mydb.cursor()

	# Show existing tables
	cursor.execute("SHOW TABLES")

	print("Tabellen gevonden: ")
	for x in cursor:
	  print(x)
	
	cursor.execute("SELECT * FROM testset;")
	
	print("Data in testset: ")
	for x in cursor:
	  print(x)
	
	print("end")


placeholders={"{{FACTUUR_ID}}": "id", "{{DATUM}}":"date", "{{TE_BETALEN}}":"teBetalen", "{{UURTARIEF}}":"uurtarief" }


def getData():
	factuurId = args['factuurId']
	print("Getting data from factuurId: " + factuurId)
	
	cursor = mydb.cursor()
	cursor.execute("SELECT id,bedrijfsnaam,uurtarief,teBetalen FROM testset WHERE id = '" + factuurId + "';")
	record = cursor.fetchone()
	
	items = ["id","bedrijfsnaam","uurtarief","teBetalen"]
	itemWithValue={}
	index = 0;
	for item in record:
		itemWithValue[items[index]] = item
		index+=1
	itemWithValue["date"] = date.today()
	
	return itemWithValue
	
def openHtmlFile():
	itemsWithValue = getData()
	factuurId = args['factuurId']
	
	with open('simple-factuur.html', 'r') as file: 
		html = file.read()
		
		for k, v in placeholders.items():
			if v in itemsWithValue.keys():
				html = html.replace(k, str(itemsWithValue[v]))
		
		# Create html file
		with open('Factuur_' + factuurId + '.html', 'w+') as f:
			f.write(html)
		
		# Convert html file to pdf
		path = os.path.abspath('Factuur_' + factuurId + '.html')
		converter.convert(f'file:///{path}', 'Factuur_'+factuurId+'.pdf')
		
		#Remove temp html factuur
		os.remove('Factuur_' + factuurId + '.html')

	
def main():
	#Run once:
	#setup_database()
	
	if not args['factuurId']:
		print("Error, geen factuurId meegegeven!")
		sys.exit()
		
	connectToDb()
	
	openHtmlFile()
	
	
if __name__ == "__main__":
	main()
