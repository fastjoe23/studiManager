import tkinter as tk
from tkinter import ttk
from views.one_note_frame import OneNoteWindow
from views.confirmation_dialog_delete_note import ConfirmationDialogDeleteNote

class NotesFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.title_label = tk.Label(self, text="Verwaltung Notizen", font=('Arial', 14, 'bold'))
        self.title_label.pack()

        # Tabelle für die Anzeige der Notizen erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Titel", "Kurzfassung", "Typ", "Name", "Erstelldatum", "Letzte Änderung"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Titel", text="Titel", command=lambda: self.sort_column("Titel"))
        self.tree.heading("Kurzfassung", text="Kurzfassung", command=lambda: self.sort_column("Kurzfassung"))
        self.tree.heading("Typ", text="Typ", command=lambda: self.sort_column("Typ"))
        self.tree.heading("Name", text="Name", command=lambda: self.sort_column("Name"))                
        self.tree.heading("Erstelldatum", text="Erstelldatum", command=lambda: self.sort_column("Erstelldatum"))
        self.tree.heading("Letzte Änderung", text="Letzte Änderung", command=lambda: self.sort_column("Letzte Änderung"))

        # Vertikale Scrollbar hinzufügen
        yscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)

        self.refresh_table()

        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Suchfeld hinzufügen
        self.search_label = tk.Label(self, text="Suche", font=('Arial', 10), fg='grey')
        self.search_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.X)
        search_entry.bind("<KeyRelease>", self.search)  # Suche bei Tastenfreigabe

        # Knöpfe zum Löschen und Ändern von Notizen erstellen
        delete_button = tk.Button(self, text="Notiz löschen", command=self.delete_selected_note)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = tk.Button(self, text="Notiz ändern", command=self.update_selected_note)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schließen", command=self.close_frame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.update_selected_note()

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def delete_selected_note(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Notizendaten aus der ausgewählten Zeile
        note_id = self.tree.item(selected_item, "values")[0]
        note = self.master.controller.read_note_by_id(note_id)

        # Erstelle eine Bestätigungsdialogbox
        confirmation_dialog = ConfirmationDialogDeleteNote(self, note, lambda: self.confirm_delete_note(selected_item))
        confirmation_dialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmation_dialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird

    def confirm_delete_note(self, selected_item):
        # Extrahiere die Notizendaten aus der ausgewählten Zeile
        note_id = self.tree.item(selected_item, "values")[0]

        # Lösche die ausgewählte Notiz aus der Datenbank
        self.master.controller.delete_note_by_id(note_id)

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refresh_table()

    def update_selected_note(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Notizendaten aus der ausgewählten Zeile
        note_id = self.tree.item(selected_item, "values")[0]
        note = self.master.controller.read_note_by_id(note_id)

        # Öffne das Fenster zum Hinzufügen oder Ändern einer neuen Notiz
        add_note_window = OneNoteWindow(self.master, note_type= note.note_type, related_id= note.related_id, note_id= note.note_id)
        add_note_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_note_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refresh_table()

    def close_frame(self):
        self.master.show_main_frame()

    def search(self, event):
        # Suche nach dem eingegebenen Text und markiere die gefundenen Zeilen
        search_query = self.search_var.get().lower()

        # Entferne zuvor gesetzte Tags
        for item in self.tree.get_children():
            self.tree.item(item, tags=[])

        # Schalter um ersten Eintrag zu speichern und später sichtbar zu schalten
        first_itemfound = False
        first_item = self.tree.get_children()[0]
        
        if search_query:
        # Durchsuche alle Zeilen im Treeview
            for item in self.tree.get_children():
                values = [value.lower() for value in self.tree.item(item, "values")]
                if any(search_query in value for value in values):
                # Markiere gefundene Zeilen mit dem "found" Tag
                    if not first_itemfound:
                        first_item = item
                        first_itemfound = True

                    self.tree.item(item, tags=["found"])
            self.tree.see(first_item)

        # Konfiguriere das Tag "found" für die Anzeige
        self.tree.tag_configure("found", background="yellow", foreground="black")

    def refresh_table(self):
        #Logik zum Aktualisieren der Tabelle hinzu
        notes = self.master.controller.read_all_notes()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for note in notes:
            if note.note_type == "student":
                student = self.master.controller.read_student_by_id(note.related_id)
                name = f"{student.last_name}, {student.first_name}"
            elif note.note_type == "course":
                course = self.master.controller.read_course_by_id(note.related_id)
                name = course.course_name
            elif note.note_type == "lecturer":
                lecturer = self.master.controller.read_lecturer_by_id(note.related_id)
                name = f"{lecturer.last_name}, {lecturer.first_name}"
            else:
                name = ""

            self.tree.insert("", tk.END, values=(note.note_id, note.note_title, note.note[:25], note.note_type, name,  note.creation_date, note.last_modification_date))

