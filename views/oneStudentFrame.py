import tkinter as tk
from tkinter import ttk

from views.oneAssignmentFrame import OneAssignmentWindow

class OneStudentWindow(tk.Toplevel):
    def __init__(self, parent, student=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Student bearbeiten" if student else "Neue Student hinzufügen")

        if student:
            # lastUsedItems aktualisieren
            parent.controller.addElementToLastUsedItems("student", student.studentId)

        # Frame für Eingabefelder
        inputFrame = tk.Frame(self)
        inputFrame.pack(pady=10)

        # Gruppe 1: Personalinformationen
        personalFrame = tk.Frame(inputFrame)
        personalFrame.pack(side=tk.LEFT, padx=10)

        self.firstNameLabel = tk.Label(personalFrame, text="Vorname:")
        self.firstNameEntry = tk.Entry(personalFrame, width=30)

        self.lastNameLabel = tk.Label(personalFrame, text="Nachname:")
        self.lastNameEntry = tk.Entry(personalFrame, width=30)

        self.emailLabel = tk.Label(personalFrame, text="E-Mail:")
        self.emailEntry = tk.Entry(personalFrame, width=30)

        self.firstNameLabel.grid(row=0, column=0, pady=5, sticky=tk.E)
        self.firstNameEntry.grid(row=0, column=1, pady=5, padx=5)
        self.lastNameLabel.grid(row=1, column=0, pady=5, sticky=tk.E)
        self.lastNameEntry.grid(row=1, column=1, pady=5, padx=5)
        self.emailLabel.grid(row=2, column=0, pady=5, sticky=tk.E)
        self.emailEntry.grid(row=2, column=1, pady=5, padx=5)

        # Gruppe 2: Firmeninformationen
        companyFrame = tk.Frame(inputFrame)
        companyFrame.pack(side=tk.LEFT, padx=10)

        self.companyLabel = tk.Label(companyFrame, text="Firma:")
        self.companyEntry = tk.Entry(companyFrame, width=30)

        self.matNumberLabel = tk.Label(companyFrame, text="MatrikelNummer:")
        self.matNumberEntry = tk.Entry(companyFrame, width=30)

        self.enrolledLabel = tk.Label(companyFrame, text="Eingeschrieben:")
        self.enrolledVar = tk.BooleanVar()
        self.enrolledCheckbox = tk.Checkbutton(companyFrame, variable=self.enrolledVar)

        self.companyLabel.grid(row=0, column=0, pady=5, sticky=tk.E)
        self.companyEntry.grid(row=0, column=1, pady=5, padx=5)
        self.matNumberLabel.grid(row=1, column=0, pady=5, sticky=tk.E)
        self.matNumberEntry.grid(row=1, column=1, pady=5, padx=5)
        self.enrolledLabel.grid(row=2, column=0, pady=5, sticky=tk.E)
        self.enrolledCheckbox.grid(row=2, column=1, pady=5, padx=5)

        # wenn Student vorhanden, dann zeige Assignments-Tabelle an
        
        if student:
            #Frame für studentische Arbeiten
            assignmentFrame = tk.Frame(self)
            assignmentFrame.pack(pady=10)

            self.assignmentsLabel = tk.Label(assignmentFrame, text="Studentische Arbeiten:")
            self.assignmentsLabel.pack(fill=tk.X, side=tk.LEFT, padx=10, pady=5)
            self.addAssignmentButton = tk.Button(assignmentFrame, text= "+", command=lambda: self.addAssignment(parent, student))
            self.addAssignmentButton.pack(fill=tk.X, side=tk.RIGHT, padx=10, pady=5)
            # Tree für Arbeiten
            self.tree = ttk.Treeview(self, columns=("ID", "Typ", "Thema",  "Vorname Gutachter", "Nachname Gutachter", "Note", "Datum", "Uhrzeit"), show="headings", height=4)
            self.tree.heading("ID", text="ID", command=lambda: self.sortColumn("ID"))
            self.tree.column("ID", width=30)
            self.tree.heading("Typ", text="Typ", command=lambda: self.sortColumn("Typ"))
            self.tree.column("Typ", width=50)
            self.tree.heading("Thema", text="Thema", command=lambda: self.sortColumn("Thema"))
            self.tree.heading("Vorname Gutachter", text="Vorname Gutachter", command=lambda: self.sortColumn("Vorname Gutachter"))
            self.tree.heading("Nachname Gutachter", text="Nachname Gutachter", command=lambda: self.sortColumn("Nachname Gutachter"))
            self.tree.heading("Note", text="Note", command=lambda: self.sortColumn("Note"))
            self.tree.column("Note", width=35)
            self.tree.heading("Datum", text="Datum", command=lambda: self.sortColumn("Datum"))
            self.tree.column("Datum", width=60)
            self.tree.heading("Uhrzeit", text="Uhrzeit", command=lambda: self.sortColumn("Uhrzeit"))
            self.tree.column("Uhrzeit", width=80)
            # Treeview füllen
            self.refreshTable(parent, student)
            
            self.tree.pack(fill=tk.BOTH, expand=True)

            # Doppelklick-Ereignis auf den Treeview binden
            self.tree.bind("<Double-1>", lambda event: self.onDoubleClick(parent, student, event))

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        addButton = tk.Button(button_frame, text="OK" if student else "Student hinzufügen",
                              command=lambda: self.addOrEditStudent(parent, student))
        addButton.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.addOrEditStudent(parent, student))
        self.focus_set()

        # Wenn Student vorhanden ist, fülle die Eingabefelder vor
        if student:
            self.firstNameEntry.insert(0, student.firstName)
            self.lastNameEntry.insert(0, student.lastName)
            self.emailEntry.insert(0, student.email)
            self.companyEntry.insert(0, student.company)
            self.matNumberEntry.insert(0, student.matNumber)
            self.enrolledVar.set(bool(student.enrolled))

    def onDoubleClick(self, parent, student, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
            self.updateSelectedAssignment(parent, student)

    def addOrEditStudent(self, parent, student):
        try:
            # Hole die Daten aus den Eingabefeldern
            firstName = self.firstNameEntry.get()
            lastName = self.lastNameEntry.get()
            email = self.emailEntry.get()
            company = self.companyEntry.get()
            matNumber = self.matNumberEntry.get()
            enrolled = self.enrolledVar.get()

            if student:
                # Bearbeite den vorhandenen Student, wenn Student_data vorhanden ist
                parent.controller.updateStudent(student.studentId, student.personId, lastName, firstName, email,
                                                company, matNumber, enrolled)
            else:
                # Füge hier die Logik zum Hinzufügen der Student hinzu
                parent.controller.addStudent(lastName, firstName, email, company, matNumber, enrolled)

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()

        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)

    def updateSelectedAssignment(self, parent, student):
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
        self.refreshTable(parent, student)  

    def addAssignment(self, parent, student):
        # Öffne das Fenster zum Hinzufügen eines neuen Assignments
        addAssignmentWindow = OneAssignmentWindow(self.master, assignment=None, student=student)
        addAssignmentWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addAssignmentWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refreshTable(parent, student)          
 
    def refreshTable(self, parent, student):
        # Logik zum Aktualisieren der Tabelle
        assignments = parent.controller.readAllAssignmentsByStudentId(student.studentId)
        for row in self.tree.get_children():
            self.tree.delete(row)

        for assignment in assignments:
            # zugehoerigen Gutachter lesen
            lecturer = parent.controller.readLecturerById(assignment.lecturerId)

            #Zeile fuellen 
            self.tree.insert("", tk.END, values=(assignment.assignmentId, assignment.type, assignment.topic, lecturer.firstName, lecturer.lastName, assignment.grade, assignment.date, assignment.time))

