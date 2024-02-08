import tkinter as tk
from tkinter import ttk

from views.one_assignment_frame import OneAssignmentWindow

class OneLecturerWindow(tk.Toplevel):
    def __init__(self, parent, lecturer=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Dozent bearbeiten" if lecturer else "Neuen Dozenten hinzufügen")

        # Frame für Eingabefelder und Notizfeld
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Eingabefelder für die neuen Dozentendaten
        personal_frame = tk.Frame(input_frame)
        personal_frame.pack(side=tk.LEFT, padx=10)
        self.first_name_label = tk.Label(personal_frame, text="Vorname:")
        self.first_name_entry = tk.Entry(personal_frame, width=30)

        self.last_name_label = tk.Label(personal_frame, text="Nachname:")
        self.last_name_entry = tk.Entry(personal_frame, width=30)

        self.email_label = tk.Label(personal_frame, text="E-Mail:")
        self.email_entry = tk.Entry(personal_frame, width=30)

        self.company_label = tk.Label(personal_frame, text="Firma:")
        self.company_entry = tk.Entry(personal_frame, width=30)

        self.first_name_label.grid(row=0, column=0, pady=5, sticky=tk.E)
        self.first_name_entry.grid(row=0, column=1, pady=5, padx=5)
        self.last_name_label.grid(row=1, column=0, pady=5, sticky=tk.E)
        self.last_name_entry.grid(row=1, column=1, pady=5, padx=5)
        self.email_label.grid(row=2, column=0, pady=5, sticky=tk.E)
        self.email_entry.grid(row=2, column=1, pady=5, padx=5)
        self.company_label.grid(row=3, column=0, pady=5, sticky=tk.E)
        self.company_entry.grid(row=3, column=1, pady=5, padx=5)

        # Notizfeld
        notes_label = tk.Label(input_frame, text="Notizen:")
        notes_label.pack(fill=tk.BOTH)
        self.notes_text  = tk.Text(input_frame, height=6, width=25)
        self.notes_text.pack(fill=tk.BOTH)

        # Wenn ein Dozent vorhanden ist, fülle die Eingabefelder und das Notizfeld vor
        if lecturer:
            self.first_name_entry.insert(0, lecturer.first_name)
            self.last_name_entry.insert(0, lecturer.last_name)
            self.email_entry.insert(0, lecturer.email)
            self.company_entry.insert(0, lecturer.company)

            # Notizfeld befüllen, falls vorhanden
            self.note = parent.controller.read_note_by_type_and_related_id("lecturer", lecturer.lecturer_id)
            if self.note:
                self.notes_text.insert("1.0", self.note.note)

            # Zeige die zugehörigen Assignments an
            # Frame für die Zuordnung der Dozentenarbeiten
            assignment_frame = tk.Frame(self)
            assignment_frame.pack(pady=10)

            # Label für die Tabelle
            assignments_label = tk.Label(assignment_frame, text="Betreute Arbeiten:")
            assignments_label.pack(fill=tk.X, padx=10, pady=5)

            # Treeview für die Zuordnung der Dozentenarbeiten
            self.tree = ttk.Treeview(assignment_frame, columns=("ID", "Typ", "Vorname Student", "Nachname Student"), show="headings", height=4)
            self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
            self.tree.column("ID", width=30)
            self.tree.heading("Typ", text="Typ", command=lambda: self.sort_column("Typ"))
            self.tree.column("Typ", width=90)
            self.tree.heading("Vorname Student", text="Vorname Student", command=lambda: self.sort_column("Vorname Student"))
            self.tree.heading("Nachname Student", text="Nachname Student", command=lambda: self.sort_column("Nachname Student"))
                        
            # Vertikale Scrollbar hinzufügen
            yscrollbar = ttk.Scrollbar(assignment_frame, orient='vertical', command=self.tree.yview)
            self.tree.configure(yscrollcommand=yscrollbar.set)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.tree.pack(fill=tk.BOTH, expand=True)

            # Doppelklick-Ereignis auf den Treeview binden
            self.tree.bind("<Double-1>", lambda event: self.on_double_click(parent, lecturer, event))            

            #tree view füllen
            self.refresh_table(parent, lecturer)


        # Knöpfe zum Hinzufügen oder Bearbeiten des Dozenten
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        button_text = "OK" if lecturer else "Dozent hinzufügen"
        add_button = tk.Button(button_frame, text=button_text, command=lambda: self.add_or_edit_lecturer(parent, lecturer))
        add_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

        # Bindung der Enter-Taste an die Funktion und Setzen des Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.add_or_edit_lecturer(parent, lecturer))
        self.focus_set()

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)


    def on_double_click(self, parent, lecturer, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.update_selected_assignment(parent, lecturer)            

    def add_or_edit_lecturer(self, parent, lecturer):
        try:
            # Daten aus den Eingabefeldern holen
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            email = self.email_entry.get()
            company = self.company_entry.get()
            actual_note_text = self.notes_text.get("1.0", "end-1c")

            if lecturer:
                # Dozent bearbeiten, wenn vorhanden
                parent.controller.update_lecturer(lecturer.lecturer_id, lecturer.person_id, last_name, first_name, email, company)
                # update der Notiztexte
                if self.note:
                    parent.controller.update_note_by_id(self.note.note_id, actual_note_text)
                else:
                    parent.controller.create_note("lecturer", lecturer.lecturer_id, actual_note_text)
            else:
                # Neuen Dozenten hinzufügen
                new_lecturer = parent.controller.add_lecturer(last_name, first_name, email, company)
                # ggf gleich neue Notiz hinzufügen
                if actual_note_text:
                    parent.controller.create_note("lecturer", new_lecturer.lecturer_id, actual_note_text)

            # Fenster nach dem Hinzufügen oder Bearbeiten schließen
            self.destroy()

        except ValueError as e:
            # Fehlermeldung anzeigen, wenn ein Fehler auftritt
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)

    def update_selected_assignment(self, parent, lecturer):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Daten aus der ausgewählten Zeile
        assignment_id = self.tree.item(selected_item, "values")[0]

        assignment = self.master.controller.read_assignment_by_id(assignment_id)


        # Öffne das Fenster zum Hinzufügen oder Ändern eines Assignments
        add_assignment_window = OneAssignmentWindow(self.master, assignment)
        add_assignment_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_assignment_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refresh_table(parent, lecturer)

    def refresh_table(self, parent, lecturer):
        # Logik zum Aktualisieren der Tabelle
        assignments = parent.controller.read_all_assignments_by_lecturer_id(lecturer.lecturer_id)
        for row in self.tree.get_children():
            self.tree.delete(row)

        for assignment in assignments:
            # zugehoerigen Studenten lesen
            student = parent.controller.read_student_by_id(assignment.student_id)

            #Zeile fuellen 
            self.tree.insert("", tk.END, values=(assignment.assignment_id, assignment.type, student.first_name, student.last_name))


        

