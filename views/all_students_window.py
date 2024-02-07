import tkinter as tk
from tkinter import ttk


class AllStudentsWindow(tk.Toplevel):
    def __init__(self, parent, course_id=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Student hinzufügen")

        # Tabelle für die Anzeige der Studenten erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Vorname", "Nachname", "E-Mail","Firma", "Matr.-Nr.","Eingeschrieben", "Erstelldatum"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
        self.tree.heading("Vorname", text="Vorname", command=lambda: self.sort_column("Vorname"))
        self.tree.heading("Nachname", text="Nachname", command=lambda: self.sort_column("Nachname"))
        self.tree.heading("E-Mail", text="E-Mail", command=lambda: self.sort_column("E-Mail"))
        self.tree.heading("Firma", text="Firma", command=lambda: self.sort_column("Firma"))
        self.tree.heading("Matr.-Nr.", text="Matr.-Nr.", command=lambda: self.sort_column("Matr.-Nr."))
        self.tree.heading("Eingeschrieben", text="Eingeschrieben", command=lambda: self.sort_column("Eingeschrieben"))        
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

        # Knöpfe zum Hinzufügen, Löschen und Ändern von Studenten erstellen
        add_button = tk.Button(self, text="Studenten hinzufügen", command=lambda: self.add_student_to_course(parent,course_id))
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        cancel_button = tk.Button(self, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)


        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, course_id, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.add_student_to_course(self,course_id)

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def add_student_to_course(self,parent, course_id):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Studentendaten aus der ausgewählten Zeile
        student_id = self.tree.item(selected_item, "values")[0]

        self.master.master.controller.add_student_to_course(student_id,course_id)

        # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
        self.destroy()



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
        students = self.master.master.controller.read_all_students()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in students:
            self.tree.insert("", tk.END, values=(student.student_id, student.first_name, student.last_name, student.email, student.company, student.mat_number, "Ja" if student.enrolled else "Nein", student.creation_date))
