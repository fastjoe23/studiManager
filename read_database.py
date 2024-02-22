import sqlite3


DATABASE_NAME = 'studimanagerDatabase.db' #configs.data_base_Name
# Verbindung zur Datenbank herstellen (dies erstellt die Datenbank, wenn sie nicht vorhanden ist)
conn = sqlite3.connect(DATABASE_NAME)

# Cursor erstellen
cursor = conn.cursor()

print("Vorm Löschen")
cursor.execute('SELECT * FROM notes')
result_list = cursor.fetchall()
for row in result_list:
    print(row)

print("Löschen")
cursor.execute("Delete from notes where note_id = 28")

print("Nach dem Löschen")
cursor.execute('SELECT * FROM notes')
result_list = cursor.fetchall()
for row in result_list:
    print(row)

conn.commit()
