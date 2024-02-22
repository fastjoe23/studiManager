import sqlite3
DATABASE_NAME = 'studimanagerDatabase.db' #configs.data_base_Name

def create_database():
    # Verbindung zur Datenbank herstellen (dies erstellt die Datenbank, wenn sie nicht vorhanden ist)
    conn = sqlite3.connect(DATABASE_NAME)

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
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(person_id)
        )
    ''')

    # Tabelle für Studenten erstellen (erbt von Personen)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER UNIQUE,
            company TEXT,
            mat_number INTEGER,
            enrolled INTEGER,
            creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (person_id) REFERENCES persons (person_id) ON DELETE CASCADE
        )
    ''')

    # Tabelle für Kurse erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT,
            start_date TEXT,
            creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabelle für Gutachter / Dozenten erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lecturers (
            lecturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER UNIQUE,
            company TEXT,
            creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (person_id) REFERENCES persons (person_id)
        )
    ''')

        # Tabelle für studentische Arbeiten erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            lecturer_id INTEGER,
            type TEXT, 
            topic TEXT,
            grade REAL,
            date TEXT,
            time TEXT,
            creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (lecturer_id) REFERENCES lecturers (lecturer_id)
        )
    ''')

    # enrollments Tabelle 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (course_id) REFERENCES courses (course_id)
        )
    ''')

    # lastUsedItems tabelle
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lastUsedItems (
                   type TEXT,
                   elements TEXT
            )           
        ''')

    # Tabelle für Notizen
    cursor.execute('''
        CREATE TABLE notes (
        note_id INTEGER PRIMARY KEY,
        note_type TEXT,
        related_id INTEGER,
        note_title TEXT,
        note TEXT,
        creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_modification_date TIMESTAMP DEFAULT NULL
        )
    ''')

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
