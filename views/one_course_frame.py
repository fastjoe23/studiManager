import tkinter as tk

class OneCourseWindow(tk.Toplevel):
    def __init__(self, parent, course_id=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Kurs bearbeiten" if course_id else "Neuen Kurs hinzufügen")

        if course_id:
            # last_used_items aktualisieren
            parent.controller.add_element_to_last_used_items("course", course_id)

        # Eingabefelder für die neuen Kursdaten
        self.course_name_label = tk.Label(self, text="Kursname:")
        self.course_name_entry = tk.Entry(self, width=30)

        self.start_date_label = tk.Label(self, text="Startdatum:")
        self.start_date_entry = tk.Entry(self, width=30)

        # Knopf zum Hinzufügen oder Bearbeiten des Kurses
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        button_text = "OK" if course_id else "Kurs hinzufügen"
        add_button = tk.Button(button_frame, text=button_text, command=lambda: self.add_or_edit_course(parent, course_id))
        add_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)



        # Pack die Widgets
        self.course_name_label.pack(pady=5)
        self.course_name_entry.pack(pady=5)

        self.start_date_label.pack(pady=5)
        self.start_date_entry.pack(pady=5)

        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.add_or_edit_course(parent, course_id))
        self.focus_set()


        # Wenn course_id vorhanden ist, fülle die Eingabefelder vor
        if course_id:
            selected_course = parent.controller.read_course_by_id(course_id)
            self.course_name_entry.insert(0, selected_course.course_name)
            self.start_date_entry.insert(0, selected_course.start_date)

    def add_or_edit_course(self, parent, course_id):
        try:
            # Hole die Daten aus den Eingabefeldern
            course_name = self.course_name_entry.get()
            start_date = self.start_date_entry.get()

            if course_id:
                # Bearbeite den vorhandenen Kurs, wenn course_id vorhanden ist
                parent.controller.update_course(course_id, course_name, start_date)
            else:
                # Füge hier die Logik zum Hinzufügen des Kurses hinzu
                parent.controller.add_course(course_name, start_date)

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()

        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)
