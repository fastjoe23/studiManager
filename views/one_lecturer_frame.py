import tkinter as tk

class OneLecturerWindow(tk.Toplevel):
    def __init__(self, parent, lecturer=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Dozent bearbeiten" if lecturer else "Neuen Dozenten hinzufügen")

        # Eingabefelder für die neuen Dozentendaten
        self.first_name_label = tk.Label(self, text="Vorname:")
        self.first_name_entry = tk.Entry(self, width=30)

        self.last_name_label = tk.Label(self, text="Nachname:")
        self.last_name_entry = tk.Entry(self, width=30)

        self.email_label = tk.Label(self, text="E-Mail:")
        self.email_entry = tk.Entry(self, width=30)

        self.company_label = tk.Label(self, text="Firma:")
        self.company_entry = tk.Entry(self, width=30)

        # Knopf zum Hinzufügen oder Bearbeiten des Dozenten
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        button_text = "OK" if lecturer else "Dozent hinzufügen"
        add_button = tk.Button(button_frame, text=button_text, command=lambda: self.add_or_edit_lecturer(parent, lecturer))
        add_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)



        # Pack die Widgets
        self.first_name_label.pack(pady=5)
        self.first_name_entry.pack(pady=5)

        self.last_name_label.pack(pady=5)
        self.last_name_entry.pack(pady=5)

        self.email_label.pack(pady=5)
        self.email_entry.pack(pady=5)

        self.company_label.pack(pady=5)
        self.company_entry.pack(pady=5)


        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.add_or_edit_lecturer(parent, lecturer))
        self.focus_set()

        # Wenn Dozent vorhanden ist, fülle die Eingabefelder vor
        if lecturer:
            self.first_name_entry.insert(0, lecturer.first_name)
            self.last_name_entry.insert(0, lecturer.last_name)
            self.email_entry.insert(0, lecturer.email)
            self.company_entry.insert(0, lecturer.company)

    def add_or_edit_lecturer(self, parent, lecturer):
        try:
            # Hole die Daten aus den Eingabefeldern
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            email = self.email_entry.get()
            company = self.company_entry.get()

            if lecturer:
                # Bearbeite den vorhandenen Dozenten, wenn Lecturer_data vorhanden ist
                parent.controller.update_lecturer(lecturer.lecturer_id, lecturer.person_id, last_name, first_name, email, company)
            else:
                # Füge hier die Logik zum Hinzufügen des Dozenten hinzu
                parent.controller.add_lecturer(last_name, first_name, email, company)

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()

        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)
