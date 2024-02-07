import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from views.oneStudentFrame import OneStudentWindow
from views.confirmationDialogDeleteStudent import ConfirmationDialogDeleteStudent
from views.confirmationDialogDeletePerson import ConfirmationDialogDeletePerson

class StudentsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.titleLabel = tk.Label(self, text= "Verwaltung Studenten", font=('Arial', 14, 'bold'))
        self.titleLabel.pack()
        # Tabelle für die Anzeige der Studenten erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Vorname", "Nachname", "E-Mail", "Firma", "Matr.-Nr.","Eingeschrieben", "Erstelldatum"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sortColumn("ID"))
        self.tree.column("ID", width=30)
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

        # Knöpfe zum Hinzufügen, Löschen und Ändern von Studenten erstellen
        add_button = tk.Button(self, text="Neuen Studenten hinzufügen", command=lambda: self.openAddStudentWindow(parent))
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self, text="Studenten löschen", command=self.deleteSelectedStudent)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = tk.Button(self, text="Studenten ändern", command=self.updateSelectedStudent)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.closeFrame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.onDoubleClick)

    def onDoubleClick(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.updateSelectedStudent()

    def sortColumn(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def openAddStudentWindow(self, parent):
        # Öffne das Fenster zum Hinzufügen eines neuen Studenten
        addStudentWindow = OneStudentWindow(self.master)
        addStudentWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addStudentWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refreshTable()

    def deleteSelectedStudent(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Studentendaten aus der ausgewählten Zeile
        studentId = self.tree.item(selectedItem, "values")[0]

        # Überprüfen, ob Student noch in Untertabellen verwendet wird
        if not self.isStudentUsedInSubtables(studentId):
            studentToDelete = self.master.controller.readStudentById(studentId)

            # Erstelle eine Bestätigungsdialogbox
            confirmationDialog = ConfirmationDialogDeleteStudent(self, studentToDelete, lambda: self.confirmDeleteStudent(selectedItem))
            confirmationDialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
            confirmationDialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird
        else:
        # Zeige eine Meldung an, dass die Person in untergeordneten Tabellen verwendet wird
            messagebox.showwarning("Warnung", "Student kann nicht gelöscht werden, da der Datensatz noch in untergeordneten Tabellen verwendet wird.")

    def isStudentUsedInSubtables(self, studentId):
    # Überprüfe, ob Student noch in Kurs eingeschrieben
        enrollments = self.master.controller.readAllEnrollmentsByStudentId(studentId)

        if enrollments:
            return True
        else:
            return False


    def confirmDeleteStudent(self, selectedItem):
        # Extrahiere die Studentendaten aus der ausgewählten Zeile
        studentId = self.tree.item(selectedItem, "values")[0]
        student = self.master.controller.readStudentById(studentId)

        # Lösche den ausgewählten Studenten aus der Datenbank
        self.master.controller.deleteStudent(studentId)

        # Nachfrage ob auch die Person geloescht werden soll
        confirmationDialogPerson = ConfirmationDialogDeletePerson(self,student, lambda: self.confirmDeletePerson(student.personId))
        confirmationDialogPerson.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmationDialogPerson.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refreshTable()

    def confirmDeletePerson(self, personId):
        # loesche die Person
        self.master.controller.deletePerson(personId)


    def updateSelectedStudent(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Studentendaten aus der ausgewählten Zeile
        studentId = self.tree.item(selectedItem, "values")[0]

        student = self.master.controller.readStudentById(studentId)


        # Öffne das Fenster zum Hinzufügen oder Ändern eines neuen Studenten
        addStudentWindow = OneStudentWindow(self.master, student)
        addStudentWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addStudentWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
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
        # Logik zum Aktualisieren der Tabelle hinzufügen
        students = self.master.controller.readAllStudents()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in students:
            self.tree.insert("", tk.END, values=(student.studentId, student.firstName, student.lastName, student.email, student.company, student.matNumber, "Ja" if student.enrolled else "Nein", student.creationDate))
