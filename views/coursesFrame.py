import tkinter as tk
from tkinter import ttk, messagebox
from views.oneCourseFrame import OneCourseWindow
from views.confirmationDialogDeleteCourse import ConfirmationDialogDeleteCourse

class CoursesFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.titleLabel = tk.Label(self, text= "Verwaltung Kurse", font=('Arial', 14, 'bold'))
        self.titleLabel.pack()
        # Tabelle für die Anzeige der Kurse erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Kursname", "Startdatum", "Erstelldatum"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sortColumn("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Kursname", text="Kursname", command=lambda: self.sortColumn("Kursname"))
        self.tree.heading("Startdatum", text="Startdatum", command=lambda: self.sortColumn("Startdatum"))
        self.tree.heading("Erstelldatum", text="Erstelldatum", command=lambda: self.sortColumn("Erstelldatum"))

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

        # Knöpfe zum Hinzufügen, Löschen und Ändern von Kursen erstellen
        addButton = tk.Button(self, text="Neuer Kurs hinzufügen", command=lambda: self.openAddCourseWindow(parent))
        addButton.pack(side=tk.LEFT, padx=5, pady=5)

        deleteButton = tk.Button(self, text="Kurs löschen", command=self.deleteSelectedCourse)
        deleteButton.pack(side=tk.LEFT, padx=5, pady=5)

        updateButton = tk.Button(self, text="Kurs ändern", command=self.updateSelectedCourse)
        updateButton.pack(side=tk.LEFT, padx=5, pady=5)

        manageButton = tk.Button(self, text="Kurs verwalten", command=self.manageSelectedCourse)
        manageButton.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.closeFrame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.onDoubleClick)

    def onDoubleClick(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        # Hole das selektierte Item
        self.manageSelectedCourse()

    def sortColumn(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def openAddCourseWindow(self, parent):
        # Öffne das Fenster zum Hinzufügen eines neuen Kurses
        addCourseWindow = OneCourseWindow(self.master)  # Annahme: Du hast eine OneCourseWindow-Klasse für die Kurse
        addCourseWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addCourseWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refreshTable()

    def deleteSelectedCourse(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        courseId = self.tree.item(selectedItem, "values")[0]
        courseToDelete = self.master.controller.readCourseById(courseId)

        # Überprüfe, ob die Person in keiner untergeordneten Tabelle vorhanden ist
        if not self.areStudentsEnrolledinCourse(courseToDelete):
            # Erstelle eine Bestätigungsdialogbox
            confirmationDialog = ConfirmationDialogDeleteCourse(self, courseToDelete, lambda: self.confirmDeleteCourse(selectedItem))
            confirmationDialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
            confirmationDialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird
        else:
        # Zeige eine Meldung an, dass die Person in untergeordneten Tabellen verwendet wird
            messagebox.showwarning("Warnung", "Der Kurs kann nicht gelöscht werden, da noch Studenten eingeschrieben sind.")

    def areStudentsEnrolledinCourse(self, course):
        # alle Eintraege aus Enrollment holen
        enrolledStudents = course.readAllEnrolledStudents()

        return len(enrolledStudents) > 0
        
        
    def confirmDeleteCourse(self, selectedItem):
        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        courseId = self.tree.item(selectedItem, "values")[0]

        # Lösche den ausgewählten Kurs aus der Datenbank
        self.master.controller.deleteCourse(courseId)

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refreshTable()

    def updateSelectedCourse(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        courseId = self.tree.item(selectedItem, "values")[0]

        # Öffne das Fenster zum Hinzufügen oder Ändern eines neuen Kurses
        updateCourseWindow = OneCourseWindow(self.master, courseId)  # Annahme: Du hast eine OneCourseWindow-Klasse für die Kurse
        updateCourseWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        updateCourseWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refreshTable()

    def manageSelectedCourse(self):
        selected_item = self.tree.selection()

        if selected_item:
            # Extrahiere die Kursdaten aus der ausgewählten Zeile
            courseId = self.tree.item(selected_item, "values")[0]

            # Rufe die Funktion im Hauptfenster auf, um zur Kursverwaltung zu wechseln
            self.master.switchToCourseManagement(courseId)

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
        courses = self.master.controller.readAllCourses()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for course in courses:
            self.tree.insert("", tk.END, values=(course.courseId, course.courseName, course.startDate, course.creationDate))
