# Skript zur Migration der Datenbank von Version 0.1 auf 0.2
# In der Tabelle lecturers wird ein Reviewer-Flag hinzugefügt
import sqlite3

DATABASE_NAME = "studimanagerDatabase.db"

def migrate_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # 1. Backup
    export_table_to_txt(cursor, "lecturers")

    # 2. Neue Spalte hinzufügen (falls noch nicht vorhanden)
    try:
        cursor.execute(
            "ALTER TABLE lecturers ADD COLUMN is_reviewer BOOLEAN NOT NULL DEFAULT FALSE;"
        )
        print("[INFO] Spalte 'is_reviewer' hinzugefügt.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("[WARN] Spalte 'is_reviewer' existiert bereits, überspringe ALTER TABLE.")
        else:
            raise

    # 3. Bei allen bisherigen Dozenten Flag auf TRUE setzen
    cursor.execute("UPDATE lecturers SET is_reviewer = TRUE;")
    print("[INFO] Alle bisherigen Dozenten als Gutachter markiert.")

    # 4. Änderungen speichern
    conn.commit()
    conn.close()
    print("[SUCCESS] Migration abgeschlossen.")

def export_table_to_txt(cursor, table_name):
    """Exportiert die komplette Tabelle in eine TXT-Datei"""
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    with open(f"{table_name}_backup.txt", "w", encoding="utf-8") as f:
        for row in rows:
            f.write(f"{row}\n")
    print(f"[INFO] Backup der Tabelle '{table_name}' in {table_name}_backup.txt erstellt.")

if __name__ == "__main__":
    migrate_database()
