import tkinter as tk
from tkinter import ttk, messagebox
from views.confirmationDialogDeleteEnrollment import ConfirmationDialogDeleteEnrollment

class EnrollmentsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.titleLabel = tk.Label(self, text= "Verwaltung Einschreibungen", font=('Arial', 14, 'bold'))
        self.titleLabel.pack()
        # Tabelle für die Anzeige der Kurse erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Kursname", "Vorname Student", "Nachname Student"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sortColumn("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Kursname", text="Kursname", command=lambda: self.sortColumn("Kursname"))
        self.tree.heading("Vorname Student", text="Vorname Student", command=lambda: self.sortColumn("Vorname Student"))
        self.tree.heading("Nachname Student", text="Nachname Student", command=lambda: self.sortColumn("Nachname Student"))

        # Vertikale Scrollbar hinzufügen
        yscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)
        
        self.refreshTable()

        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

         # Suchfeld hinzufügen
        self.searchLabel = tk.Label(self, text="Suche", font=('Arial', 10), fg='grey')
        self.searchLabel.pack(side=tk.RIGHT, padx=5, pady=5)

        self.searchVar = tk.StringVar()
        searchEntry = tk.Entry(self, textvariable=self.searchVar)
        searchEntry.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.X)
        searchEntry.bind("<KeyRelease>", self.search)  # Suche bei Tastenfreigabe

        deleteButton = tk.Button(self, text="Einschreibung löschen", command=self.deleteSelectedEnrollment)
        deleteButton.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.closeFrame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

    def sortColumn(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def deleteSelectedEnrollment(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        enrollmentId = self.tree.item(selectedItem, "values")[0]
        enrollmentToDelete = self.master.controller.readEnrollmentById(enrollmentId)

        # Erstelle eine Bestätigungsdialogbox
        confirmationDialog = ConfirmationDialogDeleteEnrollment(self, enrollmentToDelete, lambda: self.confirmDeleteEnrollment(selectedItem))
        confirmationDialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmationDialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird
        
    def confirmDeleteEnrollment(self, selectedItem):
        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        enrollmentId = self.tree.item(selectedItem, "values")[0]

        # Lösche den ausgewählten Kurs aus der Datenbank
        self.master.controller.deleteEnrollment(enrollmentId)

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
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
        enrollments = self.master.controller.readAllEnrollments()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for enrollment in enrollments:
            # zugehoerigen Kurs lesen
            course = self.master.controller.readCourseById(enrollment.courseId)
            if course:
                # zugehoerigen Studenten lesen
                student = self.master.controller.readStudentById(enrollment.studentId)
                if student:
                    #Zeile fuellen 
                    self.tree.insert("", tk.END, values=(enrollment.enrollmentId, course.courseName, student.firstName, student.lastName))
