import tkinter as tk
from tkinter import ttk


class AllStudentsWindow(tk.Toplevel):
    def __init__(self, parent, courseId=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Student hinzufügen")

        # Tabelle für die Anzeige der Studenten erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Vorname", "Nachname", "E-Mail","Firma", "Matr.-Nr.","Eingeschrieben", "Erstelldatum"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sortColumn("ID"))
        self.tree.heading("Vorname", text="Vorname", command=lambda: self.sortColumn("Vorname"))
        self.tree.heading("Nachname", text="Nachname", command=lambda: self.sortColumn("Nachname"))
        self.tree.heading("E-Mail", text="E-Mail", command=lambda: self.sortColumn("E-Mail"))
        self.tree.heading("Firma", text="Firma", command=lambda: self.sortColumn("Firma"))
        self.tree.heading("Matr.-Nr.", text="Matr.-Nr.", command=lambda: self.sortColumn("Matr.-Nr."))
        self.tree.heading("Eingeschrieben", text="Eingeschrieben", command=lambda: self.sortColumn("Eingeschrieben"))        
        self.tree.heading("Erstelldatum", text="Erstelldatum", command=lambda: self.sortColumn("Erstelldatum"))

        # Querer Scrollbar hinzufügen
        xscrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand=xscrollbar.set)

        self.refreshTable()

        self.tree.pack(fill=tk.BOTH, expand=True)
        xscrollbar.pack(fill=tk.X)

         # Suchfeld hinzufügen
        self.searchLabel = tk.Label(self, text="Suche", font=('Arial', 10), fg='grey')
        self.searchLabel.pack(side=tk.RIGHT, padx=5, pady=5)

        self.searchVar = tk.StringVar()
        searchEntry = tk.Entry(self, textvariable=self.searchVar)
        searchEntry.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.X)
        searchEntry.bind("<KeyRelease>", self.search)  # Suche bei Tastenfreigabe

        # Knöpfe zum Hinzufügen, Löschen und Ändern von Studenten erstellen
        add_button = tk.Button(self, text="Studenten hinzufügen", command=lambda: self.AddStudentToCourse(parent,courseId))
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        cancel_button = tk.Button(self, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)


        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.onDoubleClick)

    def onDoubleClick(self, courseId, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.AddStudentToCourse(self,courseId)

    def sortColumn(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def AddStudentToCourse(self,parent, courseId):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Studentendaten aus der ausgewählten Zeile
        studentId = self.tree.item(selectedItem, "values")[0]

        self.master.master.controller.AddStudentToCourse(studentId,courseId)

        # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
        self.destroy()



    def search(self, event):
        # Suche nach dem eingegebenen Text und markiere die gefundenen Zeilen
        searchQuery = self.searchVar.get().lower()

        # Entferne zuvor gesetzte Tags
        for item in self.tree.get_children():
            self.tree.item(item, tags=[])

        # Schalter um ersten Eintrag zu speichern und später sichtbar zu schalten
        firstItemfound = False
        firstItem = self.tree.get_children()[0]
        
        if searchQuery:
        # Durchsuche alle Zeilen im Treeview
            for item in self.tree.get_children():
                values = [value.lower() for value in self.tree.item(item, "values")]
                if any(searchQuery in value for value in values):
                # Markiere gefundene Zeilen mit dem "found" Tag
                    if not firstItemfound:
                        firstItem = item
                        firstItemfound = True

                    self.tree.item(item, tags=["found"])
            self.tree.see(firstItem)

        # Konfiguriere das Tag "found" für die Anzeige
        self.tree.tag_configure("found", background="yellow", foreground="black")

    def refreshTable(self):
        # Logik zum Aktualisieren der Tabelle hinzufügen
        students = self.master.master.controller.readAllStudents()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in students:
            self.tree.insert("", tk.END, values=(student.studentId, student.firstName, student.lastName, student.email, student.company, student.matNumber, "Ja" if student.enrolled else "Nein", student.creationDate))
