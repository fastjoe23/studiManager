import tkinter as tk

class OneLecturerWindow(tk.Toplevel):
    def __init__(self, parent, lecturer=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Dozent bearbeiten" if lecturer else "Neuen Dozenten hinzufügen")

        # Eingabefelder für die neuen Dozentendaten
        self.firstNameLabel = tk.Label(self, text="Vorname:")
        self.firstNameEntry = tk.Entry(self, width=30)

        self.lastNameLabel = tk.Label(self, text="Nachname:")
        self.lastNameEntry = tk.Entry(self, width=30)

        self.emailLabel = tk.Label(self, text="E-Mail:")
        self.emailEntry = tk.Entry(self, width=30)

        self.companyLabel = tk.Label(self, text="Firma:")
        self.companyEntry = tk.Entry(self, width=30)

        # Knopf zum Hinzufügen oder Bearbeiten des Dozenten
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        buttonText = "OK" if lecturer else "Dozent hinzufügen"
        addButton = tk.Button(button_frame, text=buttonText, command=lambda: self.addOrEditLecturer(parent, lecturer))
        addButton.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)



        # Pack die Widgets
        self.firstNameLabel.pack(pady=5)
        self.firstNameEntry.pack(pady=5)

        self.lastNameLabel.pack(pady=5)
        self.lastNameEntry.pack(pady=5)

        self.emailLabel.pack(pady=5)
        self.emailEntry.pack(pady=5)

        self.companyLabel.pack(pady=5)
        self.companyEntry.pack(pady=5)


        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.addOrEditLecturer(parent, lecturer))
        self.focus_set()

        # Wenn Dozent vorhanden ist, fülle die Eingabefelder vor
        if lecturer:
            self.firstNameEntry.insert(0, lecturer.firstName)
            self.lastNameEntry.insert(0, lecturer.lastName)
            self.emailEntry.insert(0, lecturer.email)
            self.companyEntry.insert(0, lecturer.company)

    def addOrEditLecturer(self, parent, lecturer):
        try:
            # Hole die Daten aus den Eingabefeldern
            firstName = self.firstNameEntry.get()
            lastName = self.lastNameEntry.get()
            email = self.emailEntry.get()
            company = self.companyEntry.get()

            if lecturer:
                # Bearbeite den vorhandenen Dozenten, wenn Lecturer_data vorhanden ist
                parent.controller.updateLecturer(lecturer.lecturerId, lecturer.personId, lastName, firstName, email, company)
            else:
                # Füge hier die Logik zum Hinzufügen des Dozenten hinzu
                parent.controller.addLecturer(lastName, firstName, email, company)

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()

        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)
