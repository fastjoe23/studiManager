import tkinter as tk
from tkinter import ttk
from views.one_lecturer_frame import OneLecturerWindow
from views.confirmation_dialog_delete_lecturer import ConfirmationDialogDeleteLecturer
from views.confirmation_dialog_delete_person import ConfirmationDialogDeletePerson

class LecturersFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.title_label = tk.Label(self, text= "Verwaltung Dozenten / Gutachter", font=('Arial', 14, 'bold'))
        self.title_label.pack()
        # Tabelle für die Anzeige der Dozenten erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Vorname", "Nachname", "E-Mail", "Firma", "Erstelldatum"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Vorname", text="Vorname", command=lambda: self.sort_column("Vorname"))
        self.tree.heading("Nachname", text="Nachname", command=lambda: self.sort_column("Nachname"))
        self.tree.heading("E-Mail", text="E-Mail", command=lambda: self.sort_column("E-Mail"))
        self.tree.heading("Firma", text="Firma", command=lambda: self.sort_column("Firma"))
        self.tree.heading("Erstelldatum", text="Erstelldatum", command=lambda: self.sort_column("Erstelldatum"))

        # Querer Scrollbar hinzufügen
        xscrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand=xscrollbar.set)

        self.refresh_table()

        self.tree.pack(fill=tk.BOTH, expand=True)
        xscrollbar.pack(fill=tk.X)

         # Suchfeld hinzufügen
        self.search_label = tk.Label(self, text="Suche", font=('Arial', 10), fg='grey')
        self.search_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.X)
        search_entry.bind("<KeyRelease>", self.search)  # Suche bei Tastenfreigabe

        # Knöpfe zum Hinzufügen, Löschen und Ändern von Dozenten erstellen
        add_button = tk.Button(self, text="Neuen Dozenten hinzufügen", command=lambda: self.open_add_lecturer_window(parent))
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self, text="Dozenten löschen", command=self.delete_selected_lecturer)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = tk.Button(self, text="Dozenten ändern", command=self.update_selected_lecturer)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.close_frame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.update_selected_lecturer()

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def open_add_lecturer_window(self, parent):
        # Öffne das Fenster zum Hinzufügen eines neuen Dozenten
        add_lecturer_window = OneLecturerWindow(self.master)
        add_lecturer_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_lecturer_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refresh_table()

    def delete_selected_lecturer(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Dozentendaten aus der ausgewählten Zeile
        lecturer_id = self.tree.item(selected_item, "values")[0]
        lecturer_to_delete = self.master.controller.read_lecturer_by_id(lecturer_id)

        # Erstelle eine Bestätigungsdialogbox
        confirmation_dialog = ConfirmationDialogDeleteLecturer(self, lecturer_to_delete, lambda: self.confirm_delete_lecturer(selected_item))
        confirmation_dialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmation_dialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird

    def confirm_delete_lecturer(self, selected_item):
        # Extrahiere die Dozentendaten aus der ausgewählten Zeile
        lecturer_id = self.tree.item(selected_item, "values")[0]
        lecturer = self.master.controller.read_lecturer_by_id(lecturer_id)

        # Lösche den ausgewählten Dozenten aus der Datenbank
        self.master.controller.delete_lecturer(lecturer_id)

        # Nachfrage ob auch die Person geloescht werden soll
        confirmation_dialog_person = ConfirmationDialogDeletePerson(self, lecturer, lambda: self.confirm_delete_person(lecturer.person_id))
        confirmation_dialog_person.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmation_dialog_person.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refresh_table()

    def confirm_delete_person(self, person_id):
        # loesche die Person
        self.master.controller.delete_person(person_id)

    def update_selected_lecturer(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Dozentendaten aus der ausgewählten Zeile
        lecturer_id = self.tree.item(selected_item, "values")[0]

        lecturer = self.master.controller.read_lecturer_by_id(lecturer_id)

        # Öffne das Fenster zum Hinzufügen oder Ändern eines neuen Dozenten
        add_lecturer_window = OneLecturerWindow(self.master, lecturer)
        add_lecturer_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_lecturer_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
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
        # Logik zum Aktualisieren der Tabelle hinzufügen
        lecturers = self.master.controller.read_all_lecturers()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for lecturer in lecturers:
            self.tree.insert("", tk.END, values=(lecturer.lecturer_id, lecturer.first_name, lecturer.last_name, lecturer.email, lecturer.company, lecturer.creation_date))
