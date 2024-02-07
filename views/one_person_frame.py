import tkinter as tk

class OnePersonWindow(tk.Toplevel):
    def __init__(self, parent,person_id = None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Person bearbeiten" if person_id else "Neue Person hinzufügen")


        # Eingabefelder für die neuen Personendaten
        self.first_name_label = tk.Label(self, text="Vorname:")
        self.first_name_entry = tk.Entry(self, width=30)

        self.last_name_label = tk.Label(self, text="Nachname:")
        self.last_name_entry = tk.Entry(self, width=30)

        self.email_label = tk.Label(self, text="E-Mail:")
        self.email_entry = tk.Entry(self, width=30)

        # Knopf zum Hinzufügen oder Bearbeiten der Person
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        button_text = "OK" if person_id else "Person hinzufügen"
        add_button = tk.Button(button_frame, text=button_text, command=lambda: self.add_or_edit_person(parent, person_id))
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


        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.add_or_edit_person(parent, person_id))
        self.focus_set()


        # Wenn person_id vorhanden ist, fülle die Eingabefelder vor
        if person_id:
            select_person = parent.controller.read_person_by_id(person_id)
            self.first_name_entry.insert(0, select_person.first_name)
            self.last_name_entry.insert(0, select_person.last_name)
            self.email_entry.insert(0, select_person.email)

    def add_or_edit_person(self, parent, person_id):
        try:
            # Hole die Daten aus den Eingabefeldern
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            email = self.email_entry.get()

            if person_id:
                # Bearbeite die vorhandene Person, wenn person_id vorhanden ist
                parent.controller.update_person(person_id, last_name, first_name, email)
            else:
                # Füge hier die Logik zum Hinzufügen der Person hinzu
                parent.controller.add_person(last_name, first_name, email)

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()

        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)

