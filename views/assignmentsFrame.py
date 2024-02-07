import tkinter as tk
from tkinter import ttk, messagebox
from views.confirmationDialogDeleteAssignment import ConfirmationDialogDeleteAssignment
from views.oneAssignmentFrame import OneAssignmentWindow

class AssignmentsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.titleLabel = tk.Label(self, text= "Verwaltung studentischer Arbeiten", font=('Arial', 14, 'bold'))
        self.titleLabel.pack()
        # Tabelle für die Anzeige der stud. Arbeiten erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Typ", "Vorname Student", "Nachname Student", "Vorname Gutachter", "Nachname Gutachter", "Thema", "Note", "Datum", "Uhrzeit"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sortColumn("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Typ", text="Typ", command=lambda: self.sortColumn("Typ"))
        self.tree.heading("Vorname Student", text="Vorname Student", command=lambda: self.sortColumn("Vorname Student"))
        self.tree.heading("Nachname Student", text="Nachname Student", command=lambda: self.sortColumn("Nachname Student"))
        self.tree.heading("Vorname Gutachter", text="Vorname Gutachter", command=lambda: self.sortColumn("Vorname Gutachter"))
        self.tree.heading("Nachname Gutachter", text="Nachname Gutachter", command=lambda: self.sortColumn("Nachname Gutachter"))
        self.tree.heading("Thema", text="Thema", command=lambda: self.sortColumn("Thema"))
        self.tree.heading("Note", text="Note", command=lambda: self.sortColumn("Note"))
        self.tree.heading("Datum", text="Datum", command=lambda: self.sortColumn("Datum"))
        self.tree.heading("Uhrzeit", text="Uhrzeit", command=lambda: self.sortColumn("Uhrzeit"))

        # Querer Scrollbar hinzufügen
        xscrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand=xscrollbar.set)

        # Vertikale Scrollbar hinzufügen
        yscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)
        
        self.refreshTable()

        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        xscrollbar.pack(fill=tk.X)

         # Suchfeld hinzufügen
        self.searchLabel = tk.Label(self, text="Suche", font=('Arial', 10), fg='grey')
        self.searchLabel.pack(side=tk.RIGHT, padx=5, pady=5)

        self.searchVar = tk.StringVar()
        searchEntry = tk.Entry(self, textvariable=self.searchVar)
        searchEntry.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.X)
        searchEntry.bind("<KeyRelease>", self.search)  # Suche bei Tastenfreigabe

        addButton = tk.Button(self, text="Neue Arbeit hinzufügen", command=self.addAssignment)
        addButton.pack(side=tk.LEFT, padx=5, pady=5)

        updateButton = tk.Button(self, text="Arbeit ändern", command=self.updateSelectedAssignment)
        updateButton.pack(side=tk.LEFT, padx=5, pady=5)

        deleteButton = tk.Button(self, text="Arbeit löschen", command=self.deleteSelectedAssignment)
        deleteButton.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.closeFrame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.onDoubleClick)

    def onDoubleClick(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.updateSelectedAssignment()

    def sortColumn(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def deleteSelectedAssignment(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        assignmentId = self.tree.item(selectedItem, "values")[0]
        assignmentToDelete = self.master.controller.readAssignmentById(assignmentId)

        # Erstelle eine Bestätigungsdialogbox
        confirmationDialog = ConfirmationDialogDeleteAssignment(self, assignmentToDelete, lambda: self.confirmDeleteAssignment(selectedItem))
        confirmationDialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmationDialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird
        
    def confirmDeleteAssignment(self, selectedItem):
        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        assignmentId = self.tree.item(selectedItem, "values")[0]

        # Lösche den ausgewählten Kurs aus der Datenbank
        self.master.controller.deleteAssignment(assignmentId)

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refreshTable()

    def addAssignment(self):
        # Öffne das Fenster zum Hinzufügen eines neuen Assignments
        addAssignmentWindow = OneAssignmentWindow(self.master)
        addAssignmentWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addAssignmentWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refreshTable()

    def updateSelectedAssignment(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Daten aus der ausgewählten Zeile
        assignmentId = self.tree.item(selectedItem, "values")[0]

        assignment = self.master.controller.readAssignmentById(assignmentId)


        # Öffne das Fenster zum Hinzufügen oder Ändern eines Assignments
        addAssignmentWindow = OneAssignmentWindow(self.master, assignment)
        addAssignmentWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addAssignmentWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refreshTable()

    def closeFrame(self):
        self.master.showMainFrame()

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
        # Logik zum Aktualisieren der Tabelle hinzu
        assignments = self.master.controller.readAllAssignments()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for assignment in assignments:
            # zugehoerigen Studenten lesen
            student = self.master.controller.readStudentById(assignment.studentId)
            if student:
                # zugehoerigen Gutachter lesen
                lecturer = self.master.controller.readLecturerById(assignment.lecturerId)
                if lecturer:
                    #Zeile fuellen 
                    self.tree.insert("", tk.END, values=(assignment.assignmentId, assignment.type, student.firstName, student.lastName, lecturer.firstName, lecturer.lastName, assignment.topic, assignment.grade, assignment.date, assignment.time))
