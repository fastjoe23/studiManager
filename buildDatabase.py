import sqlite3
from config import Config

# get config infos
#configs = Config()
databaseName = 'studiManagerDatabase.db' #configs.dataBaseName

def create_database():
    # Verbindung zur Datenbank herstellen (dies erstellt die Datenbank, wenn sie nicht vorhanden ist)
    conn = sqlite3.connect(databaseName)

    # Cursor erstellen
    cursor = conn.cursor()

    # Tabelle für Konfigurationsdaten erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            attribute TEXT NOT NULL PRIMARY KEY,
            value TEXT
        )
    ''')   

    # Tabelle für Personen erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            personId INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT,
            lastName TEXT,
            email TEXT,
            creationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(personId)
        )
    ''')

    # Tabelle für Studenten erstellen (erbt von Personen)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            studentId INTEGER PRIMARY KEY AUTOINCREMENT,
            personId INTEGER UNIQUE,
            company TEXT,
            matNumber INTEGER,
            enrolled INTEGER,
            creationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (personId) REFERENCES persons (personId) ON DELETE CASCADE
        )
    ''')

    # Tabelle für Kurse erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            courseId INTEGER PRIMARY KEY AUTOINCREMENT,
            courseName TEXT,
            startDate TEXT,
            creationDate DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabelle für Gutachter / Dozenten erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lecturers (
            lecturerId INTEGER PRIMARY KEY AUTOINCREMENT,
            personId INTEGER UNIQUE,
            company TEXT,
            creationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (personId) REFERENCES persons (personId)
        )
    ''')

        # Tabelle für studentische Arbeiten erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            assignmentId INTEGER PRIMARY KEY AUTOINCREMENT,
            studentId INTEGER,
            lecturerId INTEGER,
            type TEXT, 
            topic TEXT,
            grade REAL,
            date TEXT,
            time TEXT,
            creationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (studentId) REFERENCES students (studentId),
            FOREIGN KEY (lecturerId) REFERENCES lecturers (lecturerId)
        )
    ''')

    # enrollments Tabelle 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollmentId INTEGER PRIMARY KEY AUTOINCREMENT,
            studentId INTEGER,
            courseId INTEGER,
            FOREIGN KEY (studentId) REFERENCES students (studentId),
            FOREIGN KEY (courseId) REFERENCES courses (courseId)
        )
    ''')

    # lastUsedItems tabelle
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lastUsedItems (
                   type TEXT,
                   elements TEXT
            )           
        ''')

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
