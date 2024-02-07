import tkinter as tk
from tkinter import ttk, messagebox
from views.onePersonFrame import OnePersonWindow
from views.confirmationDialogDeletePerson import ConfirmationDialogDeletePerson

class PersonsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.titleLabel = tk.Label(self, text= "Verwaltung Personen", font=('Arial', 14, 'bold'))
        self.titleLabel.pack()
        # Tabelle für die Anzeige der Personen erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Vorname", "Nachname", "E-Mail","Erstelldatum"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sortColumn("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Vorname", text="Vorname", command=lambda: self.sortColumn("Vorname"))
        self.tree.heading("Nachname", text="Nachname", command=lambda: self.sortColumn("Nachname"))
        self.tree.heading("E-Mail", text="E-Mail", command=lambda: self.sortColumn("E-Mail"))
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

        # Knöpfe zum Hinzufügen, Löschen und Ändern von Personen erstellen
        add_button = tk.Button(self, text="Neue Person hinzufügen", command=lambda : self.openAddPersonWindow(parent))
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self, text="Person löschen", command=self.deleteSelectedPerson)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = tk.Button(self, text="Person ändern", command=self.updateSelectedPerson)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.closeFrame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.onDoubleClick)

    def onDoubleClick(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.updateSelectedPerson()

    def sortColumn(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def openAddPersonWindow(self, parent):
        # Öffne das Fenster zum Hinzufügen einer neuen Person
        addPersonWindow = OnePersonWindow(self.master)
        addPersonWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addPersonWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refreshTable()


    def deleteSelectedPerson(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Personendaten aus der ausgewählten Zeile
        personId = self.tree.item(selectedItem, "values")[0]

        # Überprüfe, ob die Person in keiner untergeordneten Tabelle vorhanden ist
        if not self.isPersonUsedInSubtables(personId):
            personToDelete = self.master.controller.readPersonById(personId)

        # Erstelle eine Bestätigungsdialogbox
            confirmationDialog = ConfirmationDialogDeletePerson(self, personToDelete, lambda: self.confirmDeletePerson(selectedItem))
            confirmationDialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
            confirmationDialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird
        else:
        # Zeige eine Meldung an, dass die Person in untergeordneten Tabellen verwendet wird
            messagebox.showwarning("Warnung", "Die Person kann nicht gelöscht werden, da sie in untergeordneten Tabellen noch verwendet wird.")

    def isPersonUsedInSubtables(self, personId):
    # Überprüfe, ob die Person in der Studenten- oder Dozententabelle vorhanden ist
        student = self.master.controller.readStudentByPersonId(personId)
        lecturer = self.master.controller.readLecturerByPersonId(personId)

        if student or lecturer:
            return True
        else:
            return False

    def confirmDeletePerson(self, selectedItem):
        # Extrahiere die Personendaten aus der ausgewählten Zeile
        personId = self.tree.item(selectedItem, "values")[0]

        # Lösche die ausgewählte Person aus der Datenbank
        self.master.controller.deletePerson(personId)

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refreshTable()

    def updateSelectedPerson(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Personendaten aus der ausgewählten Zeile
        personId = self.tree.item(selectedItem, "values")[0]

        # Öffne das Fenster zum Hinzufügen oder Ändern einer neuen Person
        addPersonWindow = OnePersonWindow(self.master,personId)
        addPersonWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addPersonWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
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
        #Logik zum Aktualisieren der Tabelle hinzu
        persons = self.master.controller.readAllPersons()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for person in persons:
            self.tree.insert("", tk.END, values=(person.personId, person.firstName, person.lastName, person.email, person.creationDate))

