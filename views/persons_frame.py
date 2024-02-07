import tkinter as tk
from tkinter import ttk, messagebox
from views.one_person_frame import OnePersonWindow
from views.confirmation_dialog_delete_person import ConfirmationDialogDeletePerson

class PersonsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.title_label = tk.Label(self, text= "Verwaltung Personen", font=('Arial', 14, 'bold'))
        self.title_label.pack()
        # Tabelle für die Anzeige der Personen erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Vorname", "Nachname", "E-Mail","Erstelldatum"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Vorname", text="Vorname", command=lambda: self.sort_column("Vorname"))
        self.tree.heading("Nachname", text="Nachname", command=lambda: self.sort_column("Nachname"))
        self.tree.heading("E-Mail", text="E-Mail", command=lambda: self.sort_column("E-Mail"))
        self.tree.heading("Erstelldatum", text="Erstelldatum", command=lambda: self.sort_column("Erstelldatum"))

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

        # Knöpfe zum Hinzufügen, Löschen und Ändern von Personen erstellen
        add_button = tk.Button(self, text="Neue Person hinzufügen", command=lambda : self.open_add_person_window(parent))
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self, text="Person löschen", command=self.delete_selected_person)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = tk.Button(self, text="Person ändern", command=self.update_selected_person)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.close_frame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.update_selected_person()

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def open_add_person_window(self, parent):
        # Öffne das Fenster zum Hinzufügen einer neuen Person
        add_person_window = OnePersonWindow(self.master)
        add_person_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_person_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refresh_table()


    def delete_selected_person(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Personendaten aus der ausgewählten Zeile
        person_id = self.tree.item(selected_item, "values")[0]

        # Überprüfe, ob die Person in keiner untergeordneten Tabelle vorhanden ist
        if not self.is_person_used_in_subtables(person_id):
            person_to_delete = self.master.controller.read_person_by_id(person_id)

        # Erstelle eine Bestätigungsdialogbox
            confirmation_dialog = ConfirmationDialogDeletePerson(self, person_to_delete, lambda: self.confirm_delete_person(selected_item))
            confirmation_dialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
            confirmation_dialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird
        else:
        # Zeige eine Meldung an, dass die Person in untergeordneten Tabellen verwendet wird
            messagebox.showwarning("Warnung", "Die Person kann nicht gelöscht werden, da sie in untergeordneten Tabellen noch verwendet wird.")

    def is_person_used_in_subtables(self, person_id):
    # Überprüfe, ob die Person in der Studenten- oder Dozententabelle vorhanden ist
        student = self.master.controller.read_student_by_person_id(person_id)
        lecturer = self.master.controller.read_lecturer_by_person_id(person_id)

        if student or lecturer:
            return True
        else:
            return False

    def confirm_delete_person(self, selected_item):
        # Extrahiere die Personendaten aus der ausgewählten Zeile
        person_id = self.tree.item(selected_item, "values")[0]

        # Lösche die ausgewählte Person aus der Datenbank
        self.master.controller.delete_person(person_id)

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refresh_table()

    def update_selected_person(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Personendaten aus der ausgewählten Zeile
        person_id = self.tree.item(selected_item, "values")[0]

        # Öffne das Fenster zum Hinzufügen oder Ändern einer neuen Person
        add_person_window = OnePersonWindow(self.master,person_id)
        add_person_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_person_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
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
        persons = self.master.controller.read_all_persons()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for person in persons:
            self.tree.insert("", tk.END, values=(person.person_id, person.first_name, person.last_name, person.email, person.creation_date))

