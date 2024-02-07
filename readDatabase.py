import sqlite3
from config import Config

# get config infos
#configs = Config()
databaseName = 'studiManagerDatabase.db' #configs.dataBaseName
# Verbindung zur Datenbank herstellen (dies erstellt die Datenbank, wenn sie nicht vorhanden ist)
conn = sqlite3.connect(databaseName)

# Cursor erstellen
cursor = conn.cursor()

print("Vorm Löschen")
cursor.execute('SELECT * FROM config')
resultList = cursor.fetchall()
for row in resultList:
    print(row)

#cursor.execute('DELETE FROM config')

print("Nach dem Löschen")
cursor.execute('SELECT * FROM config')
resultList = cursor.fetchall()
for row in resultList:
    print(row)

conn.commit()
