import tkinter as tk
from tkinter import ttk
from views.confirmation_dialog_delete_assignment import ConfirmationDialogDeleteAssignment
from views.one_assignment_frame import OneAssignmentWindow

class AssignmentsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.title_label = tk.Label(self, text= "Verwaltung studentischer Arbeiten", font=('Arial', 14, 'bold'))
        self.title_label.pack()
        # Tabelle für die Anzeige der stud. Arbeiten erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Typ", "Vorname Student", "Nachname Student", "Vorname Gutachter", "Nachname Gutachter", "Thema", "Note", "Datum", "Uhrzeit"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Typ", text="Typ", command=lambda: self.sort_column("Typ"))
        self.tree.heading("Vorname Student", text="Vorname Student", command=lambda: self.sort_column("Vorname Student"))
        self.tree.heading("Nachname Student", text="Nachname Student", command=lambda: self.sort_column("Nachname Student"))
        self.tree.heading("Vorname Gutachter", text="Vorname Gutachter", command=lambda: self.sort_column("Vorname Gutachter"))
        self.tree.heading("Nachname Gutachter", text="Nachname Gutachter", command=lambda: self.sort_column("Nachname Gutachter"))
        self.tree.heading("Thema", text="Thema", command=lambda: self.sort_column("Thema"))
        self.tree.heading("Note", text="Note", command=lambda: self.sort_column("Note"))
        self.tree.heading("Datum", text="Datum", command=lambda: self.sort_column("Datum"))
        self.tree.heading("Uhrzeit", text="Uhrzeit", command=lambda: self.sort_column("Uhrzeit"))

        # Querer Scrollbar hinzufügen
        xscrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand=xscrollbar.set)

        # Vertikale Scrollbar hinzufügen
        yscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)
        
        self.refresh_table()

        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        xscrollbar.pack(fill=tk.X)

         # Suchfeld hinzufügen
        self.search_label = tk.Label(self, text="Suche", font=('Arial', 10), fg='grey')
        self.search_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.X)
        search_entry.bind("<KeyRelease>", self.search)  # Suche bei Tastenfreigabe

        add_button = tk.Button(self, text="Neue Arbeit hinzufügen", command=self.add_assignment)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = tk.Button(self, text="Arbeit ändern", command=self.update_selected_assignment)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self, text="Arbeit löschen", command=self.delete_selected_assignment)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.close_frame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.update_selected_assignment()

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def delete_selected_assignment(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        assignment_id = self.tree.item(selected_item, "values")[0]
        assignment_to_delete = self.master.controller.read_assignment_by_id(assignment_id)

        # Erstelle eine Bestätigungsdialogbox
        confirmation_dialog = ConfirmationDialogDeleteAssignment(self, assignment_to_delete, lambda: self.confirm_delete_assignment(selected_item))
        confirmation_dialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmation_dialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird
        
    def confirm_delete_assignment(self, selected_item):
        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        assignment_id = self.tree.item(selected_item, "values")[0]

        # Lösche den ausgewählten Kurs aus der Datenbank
        self.master.controller.delete_assignment(assignment_id)

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refresh_table()

    def add_assignment(self):
        # Öffne das Fenster zum Hinzufügen eines neuen Assignments
        add_assignment_window = OneAssignmentWindow(self.master)
        add_assignment_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_assignment_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refresh_table()

    def update_selected_assignment(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Daten aus der ausgewählten Zeile
        assignment_id = self.tree.item(selected_item, "values")[0]

        assignment = self.master.controller.read_assignment_by_id(assignment_id)


        # Öffne das Fenster zum Hinzufügen oder Ändern eines Assignments
        add_assignment_window = OneAssignmentWindow(self.master, assignment)
        add_assignment_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_assignment_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
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
        # Logik zum Aktualisieren der Tabelle hinzu
        assignments = self.master.controller.read_all_assignments()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for assignment in assignments:
            # zugehoerigen Studenten lesen
            student = self.master.controller.read_student_by_id(assignment.student_id)
            if student:
                # zugehoerigen Gutachter lesen
                lecturer = self.master.controller.read_lecturer_by_id(assignment.lecturer_id)
                if lecturer:
                    #Zeile fuellen 
                    self.tree.insert("", tk.END, values=(assignment.assignment_id, assignment.type, student.first_name, student.last_name, lecturer.first_name, lecturer.last_name, assignment.topic, assignment.grade, assignment.date, assignment.time))
