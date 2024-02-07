import tkinter as tk

class OnePersonWindow(tk.Toplevel):
    def __init__(self, parent,personId = None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Person bearbeiten" if personId else "Neue Person hinzufügen")


        # Eingabefelder für die neuen Personendaten
        self.firstNameLabel = tk.Label(self, text="Vorname:")
        self.firstNameEntry = tk.Entry(self, width=30)

        self.lastNameLabel = tk.Label(self, text="Nachname:")
        self.lastNameEntry = tk.Entry(self, width=30)

        self.emailLabel = tk.Label(self, text="E-Mail:")
        self.emailEntry = tk.Entry(self, width=30)

        # Knopf zum Hinzufügen oder Bearbeiten der Person
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        buttonText = "OK" if personId else "Person hinzufügen"
        addButton = tk.Button(button_frame, text=buttonText, command=lambda: self.addOrEditPerson(parent, personId))
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


        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.addOrEditPerson(parent, personId))
        self.focus_set()


        # Wenn personId vorhanden ist, fülle die Eingabefelder vor
        if personId:
            selectPerson = parent.controller.readPersonById(personId)
            self.firstNameEntry.insert(0, selectPerson.firstName)
            self.lastNameEntry.insert(0, selectPerson.lastName)
            self.emailEntry.insert(0, selectPerson.email)

    def addOrEditPerson(self, parent, personId):
        try:
            # Hole die Daten aus den Eingabefeldern
            firstName = self.firstNameEntry.get()
            lastName = self.lastNameEntry.get()
            email = self.emailEntry.get()

            if personId:
                # Bearbeite die vorhandene Person, wenn personId vorhanden ist
                parent.controller.updatePerson(personId, lastName, firstName, email)
            else:
                # Füge hier die Logik zum Hinzufügen der Person hinzu
                parent.controller.addPerson(lastName, firstName, email)

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()

        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)

