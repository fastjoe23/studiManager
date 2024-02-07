import tkinter as tk
from tkinter import ttk
from views.oneLecturerFrame import OneLecturerWindow
from views.confirmationDialogDeleteLecturer import ConfirmationDialogDeleteLecturer
from views.confirmationDialogDeletePerson import ConfirmationDialogDeletePerson

class LecturersFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.titleLabel = tk.Label(self, text= "Verwaltung Dozenten / Gutachter", font=('Arial', 14, 'bold'))
        self.titleLabel.pack()
        # Tabelle für die Anzeige der Dozenten erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Vorname", "Nachname", "E-Mail", "Firma", "Erstelldatum"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sortColumn("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Vorname", text="Vorname", command=lambda: self.sortColumn("Vorname"))
        self.tree.heading("Nachname", text="Nachname", command=lambda: self.sortColumn("Nachname"))
        self.tree.heading("E-Mail", text="E-Mail", command=lambda: self.sortColumn("E-Mail"))
        self.tree.heading("Firma", text="Firma", command=lambda: self.sortColumn("Firma"))
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

        # Knöpfe zum Hinzufügen, Löschen und Ändern von Dozenten erstellen
        add_button = tk.Button(self, text="Neuen Dozenten hinzufügen", command=lambda: self.openAddLecturerWindow(parent))
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self, text="Dozenten löschen", command=self.deleteSelectedLecturer)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = tk.Button(self, text="Dozenten ändern", command=self.updateSelectedLecturer)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.closeFrame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.onDoubleClick)

    def onDoubleClick(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.updateSelectedLecturer()

    def sortColumn(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def openAddLecturerWindow(self, parent):
        # Öffne das Fenster zum Hinzufügen eines neuen Dozenten
        addLecturerWindow = OneLecturerWindow(self.master)
        addLecturerWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addLecturerWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refreshTable()

    def deleteSelectedLecturer(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Dozentendaten aus der ausgewählten Zeile
        lecturerId = self.tree.item(selectedItem, "values")[0]
        lecturerToDelete = self.master.controller.readLecturerById(lecturerId)

        # Erstelle eine Bestätigungsdialogbox
        confirmationDialog = ConfirmationDialogDeleteLecturer(self, lecturerToDelete, lambda: self.confirmDeleteLecturer(selectedItem))
        confirmationDialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmationDialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird

    def confirmDeleteLecturer(self, selectedItem):
        # Extrahiere die Dozentendaten aus der ausgewählten Zeile
        lecturerId = self.tree.item(selectedItem, "values")[0]
        lecturer = self.master.controller.readLecturerById(lecturerId)

        # Lösche den ausgewählten Dozenten aus der Datenbank
        self.master.controller.deleteLecturer(lecturerId)

        # Nachfrage ob auch die Person geloescht werden soll
        confirmationDialogPerson = ConfirmationDialogDeletePerson(self, lecturer, lambda: self.confirmDeletePerson(lecturer.personId))
        confirmationDialogPerson.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmationDialogPerson.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refreshTable()

    def confirmDeletePerson(self, personId):
        # loesche die Person
        self.master.controller.deletePerson(personId)

    def updateSelectedLecturer(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Dozentendaten aus der ausgewählten Zeile
        lecturerId = self.tree.item(selectedItem, "values")[0]

        lecturer = self.master.controller.readLecturerById(lecturerId)

        # Öffne das Fenster zum Hinzufügen oder Ändern eines neuen Dozenten
        addLecturerWindow = OneLecturerWindow(self.master, lecturer)
        addLecturerWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addLecturerWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
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
        lecturers = self.master.controller.readAllLecturers()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for lecturer in lecturers:
            self.tree.insert("", tk.END, values=(lecturer.lecturerId, lecturer.firstName, lecturer.lastName, lecturer.email, lecturer.company, lecturer.creationDate))
